import asyncio
from datetime import datetime
import functools
import json
import logging
from pathlib import Path
import stat
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    Set,
    Tuple,
)
import uuid

import aiofiles
import aiohttp
from aiohttp import web
import aiohttp_cors
import aiojobs
from aiojobs.aiohttp import atomic
import sqlalchemy as sa
import psycopg2
import trafaret as t

from ai.backend.common import validators as tx
from ai.backend.common.logging import BraceStyleAdapter
from ai.backend.common.utils import Fstab

from .auth import auth_required, superadmin_required
from .exceptions import (
    VFolderCreationFailed, VFolderNotFound, VFolderAlreadyExists, VFolderOperationFailed,
    GenericForbidden, GenericNotFound, InvalidAPIParameters, ServerMisconfiguredError,
    BackendAgentError, InternalServerError, GroupNotFound,
)
from .manager import (
    READ_ALLOWED, ALL_ALLOWED,
    server_status_required,
)
from .resource import get_watcher_info
from .utils import check_api_params
from ..manager.models import (
    agents,
    kernels,
    users, groups, keypairs,
    vfolders, vfolder_invitations, vfolder_permissions,
    AgentStatus,
    KernelStatus,
    VFolderInvitationState,
    VFolderOwnershipType,
    VFolderPermission,
    VFolderPermissionValidator,
    VFolderUsageMode,
    UserRole,
    query_accessible_vfolders,
    query_owned_dotfiles,
    get_allowed_vfolder_hosts_by_group,
    get_allowed_vfolder_hosts_by_user,
    verify_vfolder_name,
)
from ..manager.models.storage import StorageSessionManager

log = BraceStyleAdapter(logging.getLogger('ai.backend.gateway.vfolder'))

VFolderRow = Mapping[str, Any]


def vfolder_permission_required(perm: VFolderPermission):
    '''
    Checks if the target vfolder exists and is either:
    - owned by the current access key, or
    - allowed accesses by the access key under the specified permission.

    The decorated handler should accept an extra argument
    which contains a dict object describing the matched VirtualFolder table row.
    '''

    # FIXME: replace ... with [web.Request, VFolderRow, Any...] in the future mypy
    def _wrapper(handler: Callable[..., Awaitable[web.Response]]):

        @functools.wraps(handler)
        async def _wrapped(request: web.Request, *args, **kwargs) -> web.Response:
            dbpool = request.app['dbpool']
            domain_name = request['user']['domain_name']
            user_role = request['user']['role']
            user_uuid = request['user']['uuid']
            folder_name = request.match_info['name']
            allowed_vfolder_types = await request.app['shared_config'].get_vfolder_types()
            vf_user_cond = None
            vf_group_cond = None
            if perm == VFolderPermission.READ_ONLY:
                # if READ_ONLY is requested, any permission accepts.
                invited_perm_cond = vfolder_permissions.c.permission.in_([
                    VFolderPermission.READ_ONLY,
                    VFolderPermission.READ_WRITE,
                    VFolderPermission.RW_DELETE,
                ])
                if not request['is_admin']:
                    vf_group_cond = vfolders.c.permission.in_([
                        VFolderPermission.READ_ONLY,
                        VFolderPermission.READ_WRITE,
                        VFolderPermission.RW_DELETE,
                    ])
            elif perm == VFolderPermission.READ_WRITE:
                invited_perm_cond = vfolder_permissions.c.permission.in_([
                    VFolderPermission.READ_WRITE,
                    VFolderPermission.RW_DELETE,
                ])
                if not request['is_admin']:
                    vf_group_cond = vfolders.c.permission.in_([
                        VFolderPermission.READ_WRITE,
                        VFolderPermission.RW_DELETE,
                    ])
            elif perm == VFolderPermission.RW_DELETE:
                # If RW_DELETE is requested, only RW_DELETE accepts.
                invited_perm_cond = (
                    vfolder_permissions.c.permission == VFolderPermission.RW_DELETE
                )
                if not request['is_admin']:
                    vf_group_cond = (
                        vfolders.c.permission == VFolderPermission.RW_DELETE
                    )
            else:
                # Otherwise, just compare it as-is (for future compatibility).
                invited_perm_cond = (vfolder_permissions.c.permission == perm)
                if not request['is_admin']:
                    vf_group_cond = (vfolders.c.permission == perm)
            async with dbpool.acquire() as conn:
                entries = await query_accessible_vfolders(
                    conn, user_uuid,
                    user_role=user_role, domain_name=domain_name,
                    allowed_vfolder_types=allowed_vfolder_types,
                    extra_vf_conds=(vfolders.c.name == folder_name),
                    extra_vfperm_conds=invited_perm_cond,
                    extra_vf_user_conds=vf_user_cond,
                    extra_vf_group_conds=vf_group_cond,
                )
                if len(entries) == 0:
                    raise VFolderNotFound(
                        'Your operation may be permission denied.')
            return await handler(request, entries[0], *args, **kwargs)

        return _wrapped

    return _wrapper


# FIXME: replace ... with [web.Request, VFolderRow, Any...] in the future mypy
def vfolder_check_exists(handler: Callable[..., Awaitable[web.Response]]):
    '''
    Checks if the target vfolder exists and is owned by the current user.

    The decorated handler should accept an extra "row" argument
    which contains the matched VirtualFolder table row.
    '''

    @functools.wraps(handler)
    async def _wrapped(request: web.Request, *args, **kwargs) -> web.Response:
        dbpool = request.app['dbpool']
        user_uuid = request['user']['uuid']
        folder_name = request.match_info['name']
        async with dbpool.acquire() as conn:
            j = sa.join(
                vfolders, vfolder_permissions,
                vfolders.c.id == vfolder_permissions.c.vfolder, isouter=True)
            query = (
                sa.select('*')
                .select_from(j)
                .where(((vfolders.c.user == user_uuid) |
                        (vfolder_permissions.c.user == user_uuid)) &
                       (vfolders.c.name == folder_name)))
            try:
                result = await conn.execute(query)
            except psycopg2.DataError:
                raise InvalidAPIParameters
            row = await result.first()
            if row is None:
                raise VFolderNotFound()
        return await handler(request, row, *args, **kwargs)

    return _wrapped


@auth_required
@server_status_required(ALL_ALLOWED)
@check_api_params(
    t.Dict({
        t.Key('name'): tx.Slug(allow_dot=True),
        t.Key('host', default=None) >> 'folder_host': t.String | t.Null,
        t.Key('usage_mode', default='general'): tx.Enum(VFolderUsageMode) | t.Null,
        t.Key('permission', default='rw'): tx.Enum(VFolderPermission) | t.Null,
        tx.AliasedKey(['unmanaged_path', 'unmanagedPath'], default=None): t.String | t.Null,
        tx.AliasedKey(['group', 'groupId', 'group_id'], default=None): tx.UUID | t.String | t.Null,
        t.Key('quota', default=None): tx.BinarySize | t.Null,
        t.Key('cloneable', default=False): t.Bool
    }),
)
async def create(request: web.Request, params: Any) -> web.Response:
    resp: Dict[str, Any] = {}
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    user_role = request['user']['role']
    user_uuid = request['user']['uuid']
    resource_policy = request['keypair']['resource_policy']
    domain_name = request['user']['domain_name']
    group_id_or_name = params['group']
    log.info('VFOLDER.CREATE (ak:{}, vf:{}, vfh:{}, umod:{}, perm:{})',
             access_key, params['name'], params['folder_host'],
             params['usage_mode'].value, params['permission'].value)
    folder_host = params['folder_host']
    unmanaged_path = params['unmanaged_path']
    # Check if user is trying to created unmanaged vFolder
    if unmanaged_path:
        # Approve only if user is Admin or Superadmin
        if user_role not in (UserRole.ADMIN, UserRole.SUPERADMIN):
            raise GenericForbidden('Insufficient permission')
    else:
        # Resolve host for the new virtual folder.
        if not folder_host:
            folder_host = \
                await request.app['shared_config'].etcd.get('volumes/default_host')
            if not folder_host:
                raise InvalidAPIParameters(
                    'You must specify the vfolder host '
                    'because the default host is not configured.')
    allowed_vfolder_types = await request.app['shared_config'].get_vfolder_types()
    for vf_type in allowed_vfolder_types:
        if vf_type not in ('user', 'group'):
            raise ServerMisconfiguredError(
                f'Invalid vfolder type(s): {str(allowed_vfolder_types)}.'
                ' Only "user" or "group" is allowed.')

    if not verify_vfolder_name(params['name']):
        raise InvalidAPIParameters(f'{params["name"]} is reserved for internal operations.')
    if params['name'].startswith('.') and params['name'] != '.local':
        if params['group'] is not None:
            raise InvalidAPIParameters('dot-prefixed vfolders cannot be a group folder.')

    async with dbpool.acquire() as conn:
        # Convert group name to uuid if group name is given.
        if isinstance(group_id_or_name, str):
            query = (sa.select([groups.c.id])
                     .select_from(groups)
                     .where(groups.c.domain_name == domain_name)
                     .where(groups.c.name == group_id_or_name))
            group_id = await conn.scalar(query)
        else:
            group_id = group_id_or_name
        if not unmanaged_path:
            # Check resource policy's allowed_vfolder_hosts
            if group_id is not None:
                allowed_hosts = await get_allowed_vfolder_hosts_by_group(conn, resource_policy,
                                                                         domain_name, group_id)
            else:
                allowed_hosts = await get_allowed_vfolder_hosts_by_user(conn, resource_policy,
                                                                        domain_name, user_uuid)
            # TODO: handle legacy host lists assuming that volume names don't overlap?
            if folder_host not in allowed_hosts:
                raise InvalidAPIParameters('You are not allowed to use this vfolder host.')

        # Check resource policy's max_vfolder_count
        if resource_policy['max_vfolder_count'] > 0:
            query = (sa.select([sa.func.count()])
                       .where(vfolders.c.user == user_uuid))
            result = await conn.scalar(query)
            if result >= resource_policy['max_vfolder_count']:
                raise InvalidAPIParameters('You cannot create more vfolders.')

        # Prevent creation of vfolder with duplicated name.
        extra_vf_conds = [vfolders.c.name == params['name']]
        if not unmanaged_path:
            extra_vf_conds.append(vfolders.c.host == folder_host)
        entries = await query_accessible_vfolders(
            conn, user_uuid,
            user_role=user_role, domain_name=domain_name,
            allowed_vfolder_types=allowed_vfolder_types,
            extra_vf_conds=(sa.and_(*extra_vf_conds))
        )
        if len(entries) > 0:
            raise VFolderAlreadyExists

        # Check if group exists.
        if group_id_or_name and group_id is None:
            raise GroupNotFound
        if group_id is not None:
            if 'group' not in allowed_vfolder_types:
                raise InvalidAPIParameters('group vfolder cannot be created in this host')
            if not request['is_admin']:
                raise GenericForbidden('no permission')
            query = (sa.select([groups.c.id])
                       .select_from(groups)
                       .where(groups.c.domain_name == domain_name)
                       .where(groups.c.id == group_id))
            _gid = await conn.scalar(query)
            if str(_gid) != str(group_id):
                raise InvalidAPIParameters('No such group.')
        else:
            if 'user' not in allowed_vfolder_types:
                raise InvalidAPIParameters('user vfolder cannot be created in this host')
        try:
            folder_id = uuid.uuid4()
            if not unmanaged_path:
                # Try to create actual only if vFolder is managed one
                storage_manager = request.app['storage_manager']
                async with storage_manager.request(
                    folder_host, 'POST', 'folder/create',
                    json={
                        'volume': storage_manager.split_host(folder_host)[1],
                        'vfid': str(folder_id),
                        'options': {'quota': params['quota']},
                    },
                    raise_for_status=True,
                ):
                    pass
        except aiohttp.ClientResponseError:
            raise VFolderCreationFailed
        user_uuid = str(user_uuid) if group_id is None else None
        group_uuid = str(group_id) if group_id is not None else None
        ownership_type = 'group' if group_uuid is not None else 'user'
        insert_values = {
            'id': folder_id.hex,
            'name': params['name'],
            'usage_mode': params['usage_mode'],
            'permission': params['permission'],
            'last_used': None,
            'host': folder_host,
            'creator': request['user']['email'],
            'ownership_type': VFolderOwnershipType(ownership_type),
            'user': user_uuid,
            'group': group_uuid,
            'unmanaged_path': '',
            'cloneable': params['cloneable'],
        }
        resp = {
            'id': folder_id.hex,
            'name': params['name'],
            'host': folder_host,
            'usage_mode': params['usage_mode'].value,
            'permission': params['permission'].value,
            'creator': request['user']['email'],
            'ownership_type': ownership_type,
            'user': user_uuid,
            'group': group_uuid,
            'cloneable': params['cloneable'],
        }
        if unmanaged_path:
            insert_values.update({
                'host': '',
                'unmanaged_path': unmanaged_path
            })
            resp['unmanaged_path'] = unmanaged_path
        query = (vfolders.insert().values(insert_values))
        try:
            result = await conn.execute(query)
        except psycopg2.DataError:
            raise InvalidAPIParameters
        assert result.rowcount == 1
    return web.json_response(resp, status=201)


@auth_required
@server_status_required(READ_ALLOWED)
@check_api_params(
    t.Dict({
        t.Key('all', default=False): t.ToBool,
        tx.AliasedKey(['group_id', 'groupId'], default=None): tx.UUID | t.String | t.Null,
    }),
)
async def list_folders(request: web.Request, params: Any) -> web.Response:
    resp = []
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    domain_name = request['user']['domain_name']
    user_role = request['user']['role']
    user_uuid = request['user']['uuid']

    log.info('VFOLDER.LIST (ak:{})', access_key)
    async with dbpool.acquire() as conn:
        allowed_vfolder_types = await request.app['shared_config'].get_vfolder_types()
        if request['is_superadmin'] and params['all']:
            # List all folders for superadmin if all is specified
            j = (vfolders.join(users, vfolders.c.user == users.c.uuid, isouter=True)
                         .join(groups, vfolders.c.group == groups.c.id, isouter=True))
            query = (sa.select([vfolders, users.c.email, groups.c.name], use_labels=True)
                       .select_from(j))
            result = await conn.execute(query)
            entries = []
            async for row in result:
                is_owner = True if row.vfolders_user == user_uuid else False
                entries.append({
                    'name': row.vfolders_name,
                    'id': row.vfolders_id,
                    'host': row.vfolders_host,
                    'usage_mode': row.vfolders_usage_mode,
                    'created_at': row.vfolders_created_at,
                    'is_owner': is_owner,
                    'permission': row.vfolders_permission,
                    'user': str(row.vfolders_user) if row.vfolders_user else None,
                    'group': str(row.vfolders_group) if row.vfolders_group else None,
                    'creator': row.vfolders_creator,
                    'user_email': row.users_email,
                    'group_name': row.groups_name,
                    'ownership_type': row.vfolders_ownership_type,
                    'type': row.vfolders_ownership_type,  # legacy
                    'unmanaged_path': row.vfolders_unmanaged_path
                })
        else:
            extra_vf_conds = None
            if params['group_id'] is not None:
                # Note: user folders should be returned even when group_id is specified.
                extra_vf_conds = ((vfolders.c.group == params['group_id']) |
                                  (vfolders.c.user.isnot(None)))
            entries = await query_accessible_vfolders(
                conn, user_uuid,
                user_role=user_role, domain_name=domain_name,
                allowed_vfolder_types=allowed_vfolder_types,
                extra_vf_conds=extra_vf_conds,
            )
        for entry in entries:
            resp.append({
                'name': entry['name'],
                'id': entry['id'].hex,
                'host': entry['host'],
                'usage_mode': entry['usage_mode'].value,
                'created_at': str(entry['created_at']),
                'is_owner': entry['is_owner'],
                'permission': entry['permission'].value,
                'user': str(entry['user']) if entry['user'] else None,
                'group': str(entry['group']) if entry['group'] else None,
                'creator': entry['creator'],
                'user_email': entry['user_email'],
                'group_name': entry['group_name'],
                'ownership_type': entry['ownership_type'].value,
                'type': entry['ownership_type'].value,  # legacy
            })
    return web.json_response(resp, status=200)


@superadmin_required
@server_status_required(ALL_ALLOWED)
@check_api_params(
    t.Dict({
        t.Key('id'): t.String,
    }),
)
async def delete_by_id(request: web.Request, params: Any) -> web.Response:
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.DELETE_BY_ID (ak:{}, vf:{})', access_key, params['id'])
    async with dbpool.acquire() as conn, conn.begin():
        query = (
            sa.select([vfolders.c.host])
            .select_from(vfolders)
            .where(vfolders.c.id == params['id'])
        )
        folder_host = await conn.scalar(query)
        folder_id = uuid.UUID(params['id'])
        query = (vfolders.delete().where(vfolders.c.id == folder_id))
        await conn.execute(query)
    # fs-level deletion may fail or take longer time
    # but let's complete the db transaction to reflect that it's deleted.
    storage_manager = request.app['storage_manager']
    try:
        async with storage_manager.request(
            folder_host, 'POST', 'folder/delete',
            json={
                'volume': storage_manager.split_host(folder_host)[1],
                'vfid': str(folder_id),
            },
            raise_for_status=True,
        ):
            pass
    except aiohttp.ClientResponseError:
        raise VFolderOperationFailed
    return web.Response(status=204)


@atomic
@auth_required
@server_status_required(READ_ALLOWED)
async def list_hosts(request: web.Request) -> web.Response:
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.LIST_HOSTS (ak:{})', access_key)
    config = request.app['shared_config']
    dbpool = request.app['dbpool']
    domain_name = request['user']['domain_name']
    domain_admin = request['user']['role'] == UserRole.ADMIN
    resource_policy = request['keypair']['resource_policy']
    allowed_vfolder_types = await request.app['shared_config'].get_vfolder_types()
    async with dbpool.acquire() as conn:
        allowed_hosts: Set[str] = set()
        if 'user' in allowed_vfolder_types:
            allowed_hosts_by_user = await get_allowed_vfolder_hosts_by_user(
                conn, resource_policy, domain_name, request['user']['uuid'])
            allowed_hosts = allowed_hosts | allowed_hosts_by_user
        if 'group' in allowed_vfolder_types:
            allowed_hosts_by_group = await get_allowed_vfolder_hosts_by_group(
                conn, resource_policy, domain_name, group_id=None, domain_admin=domain_admin)
            allowed_hosts = allowed_hosts | allowed_hosts_by_group
    all_volumes = await request.app['storage_manager'].get_all_volumes()
    all_hosts = {f"{proxy_name}:{volume_data['name']}" for proxy_name, volume_data in all_volumes}
    allowed_hosts = allowed_hosts & all_hosts
    default_host = await config.get_raw('volumes/default_host')
    if default_host not in allowed_hosts:
        default_host = None
    resp = {
        'default': default_host,
        'allowed': sorted(allowed_hosts),
    }
    return web.json_response(resp, status=200)


@atomic
@superadmin_required
@server_status_required(READ_ALLOWED)
async def list_all_hosts(request: web.Request) -> web.Response:
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.LIST_ALL_HOSTS (ak:{})', access_key)
    all_volumes = await request.app['storage_manager'].get_all_volumes()
    all_hosts = {f"{proxy_name}:{volume_data['name']}" for proxy_name, volume_data in all_volumes}
    config = request.app['shared_config']
    default_host = await config.get_raw('volumes/default_host')
    if default_host not in all_hosts:
        default_host = None
    resp = {
        'default': default_host,
        'allowed': sorted(all_hosts),
    }
    return web.json_response(resp, status=200)


@atomic
@superadmin_required
@server_status_required(READ_ALLOWED)
@check_api_params(
    t.Dict({
        t.Key('folder_host'): t.String,
    }))
async def get_volume_perf_metric(request: web.Request, params: Any) -> web.Response:
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.VOLUME_PERF_METRIC (ak:{})', access_key)
    storage_manager = request.app['storage_manager']
    proxy_name, volume_name = storage_manager.split_host(params['folder_host'])
    try:
        async with storage_manager.request(
            proxy_name, 'GET', 'volume/performance-metric',
            json={
                'volume': volume_name,
            },
            raise_for_status=True,
        ) as (_, storage_resp):
            storage_reply = await storage_resp.json()
    except aiohttp.ClientResponseError:
        raise VFolderOperationFailed
    return web.json_response(storage_reply, status=200)


@atomic
@auth_required
@server_status_required(READ_ALLOWED)
async def list_allowed_types(request: web.Request) -> web.Response:
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.LIST_ALLOWED_TYPES (ak:{})', access_key)
    allowed_vfolder_types = await request.app['shared_config'].get_vfolder_types()
    return web.json_response(allowed_vfolder_types, status=200)


@atomic
@auth_required
@server_status_required(READ_ALLOWED)
@vfolder_permission_required(VFolderPermission.READ_ONLY)
async def get_info(request: web.Request, row: VFolderRow) -> web.Response:
    resp: Dict[str, Any] = {}
    folder_name = request.match_info['name']
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.GETINFO (ak:{}, vf:{})', access_key, folder_name)
    if row['permission'] is None:
        is_owner = True
        permission = VFolderPermission.OWNER_PERM
    else:
        is_owner = row['is_owner']
        permission = row['permission']
    storage_manager = request.app['storage_manager']
    proxy_name, volume_name = storage_manager.split_host(row['host'])
    try:
        async with storage_manager.request(
            proxy_name, 'GET', 'folder/usage',
            json={
                'volume': volume_name,
                'vfid': str(row['id']),
            },
            raise_for_status=True,
        ) as (_, storage_resp):
            usage = await storage_resp.json()
        resp = {
            'name': row['name'],
            'id': row['id'].hex,
            'host': row['host'],
            'numFiles': usage['file_count'],  # legacy
            'num_files': usage['file_count'],
            'used_bytes': usage['used_bytes'],  # added in v20.09
            'created': str(row['created_at']),  # legacy
            'created_at': str(row['created_at']),
            'last_used': str(row['created_at']),
            'user': str(row['user']),
            'group': str(row['group']),
            'type': 'user' if row['user'] is not None else 'group',
            'is_owner': is_owner,
            'permission': permission,
            'usage_mode': row['usage_mode'],
            'cloneable': row['cloneable']
        }
    except aiohttp.ClientResponseError:
        raise VFolderOperationFailed
    return web.json_response(resp, status=200)


@atomic
@auth_required
@server_status_required(ALL_ALLOWED)
@vfolder_permission_required(VFolderPermission.OWNER_PERM)
@check_api_params(
    t.Dict({
        t.Key('new_name'): tx.Slug(allow_dot=True),
    }))
async def rename_vfolder(request: web.Request, params: Any, row: VFolderRow) -> web.Response:
    dbpool = request.app['dbpool']
    old_name = request.match_info['name']
    access_key = request['keypair']['access_key']
    domain_name = request['user']['domain_name']
    user_role = request['user']['role']
    user_uuid = request['user']['uuid']
    new_name = params['new_name']
    allowed_vfolder_types = await request.app['shared_config'].get_vfolder_types()
    log.info('VFOLDER.RENAME (ak:{}, vf.old:{}, vf.new:{})',
             access_key, old_name, new_name)
    async with dbpool.acquire() as conn:
        entries = await query_accessible_vfolders(
            conn, user_uuid,
            user_role=user_role, domain_name=domain_name,
            allowed_vfolder_types=allowed_vfolder_types)
        for entry in entries:
            if entry['name'] == new_name:
                raise InvalidAPIParameters(
                    'One of your accessible vfolders already has '
                    'the name you requested.')
        for entry in entries:
            if entry['name'] == old_name:
                if not entry['is_owner']:
                    raise InvalidAPIParameters(
                        'Cannot change the name of a vfolder '
                        'that is not owned by myself.')
                query = (
                    vfolders.update()
                    .values(name=new_name)
                    .where(vfolders.c.id == entry['id']))
                await conn.execute(query)
                break
    return web.Response(status=201)


@atomic
@auth_required
@server_status_required(ALL_ALLOWED)
@vfolder_permission_required(VFolderPermission.OWNER_PERM)
@check_api_params(
    t.Dict({
        t.Key('cloneable', default=None): t.Bool | t.Null,
        t.Key('permission', default=None): tx.Enum(VFolderPermission) | t.Null
    }))
async def update_vfolder_options(request: web.Request, params: Any, row: VFolderRow) -> web.Response:
    updated_fields = {}
    if params['cloneable'] is not None and params['cloneable'] != row['cloneable']:
        updated_fields['cloneable'] = params['cloneable']
    if params['permission'] is not None and params['permission'] != row['permission']:
        updated_fields['permission'] = params['permission']
    if not row['is_owner']:
        raise InvalidAPIParameters(
            'Cannot change the options of a vfolder '
            'that is not owned by myself.')

    dbpool = request.app['dbpool']
    if len(updated_fields) > 0:
        async with dbpool.acquire() as conn:
            query = (
                sa.update(vfolders)
                .values(**updated_fields)
                .where(vfolders.c.id == row['id']))
            await conn.execute(query)
    return web.Response(status=201)


@auth_required
@server_status_required(READ_ALLOWED)
@vfolder_permission_required(VFolderPermission.READ_WRITE)
@check_api_params(
    t.Dict({
        t.Key('path'): t.String,
        t.Key('parents', default=True): t.ToBool,
        t.Key('exist_ok', default=False): t.ToBool,
    }))
async def mkdir(request: web.Request, params: Any, row: VFolderRow) -> web.Response:
    folder_name = request.match_info['name']
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.MKDIR (ak:{}, vf:{}, path:{})', access_key, folder_name, params['path'])
    storage_manager = request.app['storage_manager']
    proxy_name, volume_name = storage_manager.split_host(row['host'])
    try:
        async with storage_manager.request(
            proxy_name, 'POST', 'folder/file/mkdir',
            json={
                'volume': volume_name,
                'vfid': str(row['id']),
                'relpath': params['path'],
                'parents': params['parents'],
                'exist_ok': params['exist_ok'],
            },
            raise_for_status=True,
        ):
            pass
    except aiohttp.ClientResponseError:
        raise VFolderCreationFailed
    return web.Response(status=201)


@atomic
@auth_required
@server_status_required(READ_ALLOWED)
@vfolder_permission_required(VFolderPermission.READ_ONLY)
@check_api_params(
    t.Dict({
        tx.AliasedKey(['path', 'file']): t.String,
        t.Key('archive', default=False): t.ToBool,
    }))
async def create_download_session(request: web.Request, params: Any, row: VFolderRow) -> web.Response:
    log_fmt = 'VFOLDER.CREATE_DOWNLOAD_SESSION(ak:{}, vf:{}, path:{})'
    log_args = (request['keypair']['access_key'], row['name'], params['path'])
    log.info(log_fmt, *log_args)
    unmanaged_path = row['unmanaged_path']
    storage_manager = request.app['storage_manager']
    proxy_name, volume_name = storage_manager.split_host(row['host'])
    try:
        async with storage_manager.request(
            proxy_name, 'POST', 'folder/file/download',
            json={
                'volume': volume_name,
                'vfid': str(row['id']),
                'relpath': params['path'],
                'archive': params['archive'],
                'unmanaged_path': unmanaged_path if unmanaged_path else None,
            },
            raise_for_status=True,
        ) as (client_api_url, storage_resp):
            storage_reply = await storage_resp.json()
            resp = {
                'token': storage_reply['token'],
                'url': str(client_api_url / 'download'),
            }
    except aiohttp.ClientResponseError:
        raise VFolderOperationFailed
    return web.json_response(resp, status=200)


@auth_required
@server_status_required(READ_ALLOWED)
@vfolder_permission_required(VFolderPermission.READ_WRITE)
@check_api_params(
    t.Dict({
        t.Key('path'): t.String,
        t.Key('size'): t.ToInt,
    }))
async def create_upload_session(request: web.Request, params: Any, row: VFolderRow) -> web.Response:
    folder_name = request.match_info['name']
    access_key = request['keypair']['access_key']
    log_fmt = 'VFOLDER.CREATE_UPLOAD_SESSION (ak:{}, vf:{})'
    log_args = (access_key, folder_name)
    log.info(log_fmt, *log_args)
    storage_manager = request.app['storage_manager']
    proxy_name, volume_name = storage_manager.split_host(row['host'])
    try:
        async with storage_manager.request(
            proxy_name, 'POST', 'folder/file/upload',
            json={
                'volume': volume_name,
                'vfid': str(row['id']),
                'relpath': params['path'],
                'size': params['size'],
            },
            raise_for_status=True,
        ) as (client_api_url, storage_resp):
            storage_reply = await storage_resp.json()
            resp = {
                'token': storage_reply['token'],
                'url': str(client_api_url / 'upload'),
            }
    except aiohttp.ClientResponseError:
        raise VFolderOperationFailed
    return web.json_response(resp, status=200)


@auth_required
@server_status_required(READ_ALLOWED)
@vfolder_permission_required(VFolderPermission.READ_WRITE)
@check_api_params(
    t.Dict({
        t.Key('target_path'): t.String,
        t.Key('new_name'): t.String,
    }))
async def rename_file(request: web.Request, params: Any, row: VFolderRow) -> web.Response:
    folder_name = request.match_info['name']
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.RENAME_FILE (ak:{}, vf:{}, target_path:{}, new_name:{})',
             access_key, folder_name, params['target_path'], params['new_name'])
    storage_manager = request.app['storage_manager']
    proxy_name, volume_name = storage_manager.split_host(row['host'])
    try:
        async with storage_manager.request(
            proxy_name, 'POST', 'folder/file/rename',
            json={
                'volume': volume_name,
                'vfid': str(row['id']),
                'relpath': params['target_path'],
                'new_name': params['new_name'],
            },
            raise_for_status=True,
        ):
            pass
    except aiohttp.ClientResponseError:
        raise VFolderOperationFailed
    return web.json_response({}, status=200)


@auth_required
@server_status_required(READ_ALLOWED)
@vfolder_permission_required(VFolderPermission.READ_WRITE)
@check_api_params(
    t.Dict({
        t.Key('files'): t.List[t.String],
        t.Key('recursive', default=False): t.ToBool,
    }))
async def delete_files(request: web.Request, params: Any, row: VFolderRow) -> web.Response:
    folder_name = request.match_info['name']
    access_key = request['keypair']['access_key']
    recursive = params['recursive']
    log.info('VFOLDER.DELETE_FILES (ak:{}, vf:{}, path:{}, recursive:{})',
             access_key, folder_name, folder_name, recursive)
    storage_manager = request.app['storage_manager']
    proxy_name, volume_name = storage_manager.split_host(row['host'])
    try:
        async with storage_manager.request(
            proxy_name, 'POST', 'folder/file/delete',
            json={
                'volume': volume_name,
                'vfid': str(row['id']),
                'relpaths': params['files'],
                'recursive': recursive,
            },
            raise_for_status=True,
        ):
            pass
    except aiohttp.ClientResponseError:
        raise VFolderOperationFailed
    return web.json_response({}, status=200)


@auth_required
@server_status_required(READ_ALLOWED)
@vfolder_permission_required(VFolderPermission.READ_ONLY)
@check_api_params(
    t.Dict({
        t.Key('path', default=''): t.String(allow_blank=True),
    }))
async def list_files(request: web.Request, params: Any, row: VFolderRow) -> web.Response:
    folder_name = request.match_info['name']
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.LIST_FILES (ak:{}, vf:{}, path:{})',
             access_key, folder_name, params['path'])
    storage_manager = request.app['storage_manager']
    proxy_name, volume_name = storage_manager.split_host(row['host'])
    try:
        async with storage_manager.request(
            proxy_name, 'POST', 'folder/file/list',
            json={
                'volume': volume_name,
                'vfid': str(row['id']),
                'relpath': params['path'],
            },
            raise_for_status=True,
        ) as (_, storage_resp):
            result = await storage_resp.json()
            resp = {
                'items': [
                    {
                        'name': item['name'],
                        'type': item['type'],
                        'size': item['stat']['size'],  # humanize?
                        'mode': oct(item['stat']['mode'])[2:][-3:],
                        'created': item['stat']['created'],
                        'modified': item['stat']['modified'],
                    }
                    for item in result['items']
                ],
                'files': json.dumps([  # for legacy (to be removed in 21.03)
                    {
                        'filename': item['name'],
                        'size': item['stat']['size'],
                        'mode': stat.filemode(item['stat']['mode']),
                        'ctime': datetime.fromisoformat(item['stat']['created']).timestamp(),
                        'atime': 0,
                        'mtime': datetime.fromisoformat(item['stat']['modified']).timestamp(),
                    }
                    for item in result['items']
                ]),
            }
    except aiohttp.ClientResponseError:
        raise VFolderOperationFailed
    return web.json_response(resp, status=200)


@atomic
@auth_required
@server_status_required(READ_ALLOWED)
async def list_sent_invitations(request: web.Request) -> web.Response:
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.LIST_SENT_INVITATIONS (ak:{})', access_key)
    async with dbpool.acquire() as conn:
        j = sa.join(vfolders, vfolder_invitations,
                    vfolders.c.id == vfolder_invitations.c.vfolder)
        query = (sa.select([vfolder_invitations, vfolders.c.name])
                   .select_from(j)
                   .where((vfolder_invitations.c.inviter == request['user']['email']) &
                          (vfolder_invitations.c.state == VFolderInvitationState.PENDING)))
        result = await conn.execute(query)
        invitations = await result.fetchall()
    invs_info = []
    for inv in invitations:
        invs_info.append({
            'id': str(inv.id),
            'inviter': inv.inviter,
            'invitee': inv.invitee,
            'perm': inv.permission,
            'state': inv.state.value,
            'created_at': str(inv.created_at),
            'modified_at': str(inv.modified_at),
            'vfolder_id': str(inv.vfolder),
            'vfolder_name': inv.name,
        })
    resp = {'invitations': invs_info}
    return web.json_response(resp, status=200)


@atomic
@auth_required
@server_status_required(ALL_ALLOWED)
@check_api_params(
    t.Dict({
        tx.AliasedKey(['perm', 'permission']): VFolderPermissionValidator,
    })
)
async def update_invitation(request: web.Request, params: Any) -> web.Response:
    '''
    Update sent invitation's permission. Other fields are not allowed to be updated.
    '''
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    inv_id = request.match_info['inv_id']
    perm = params['perm']
    log.info('VFOLDER.UPDATE_INVITATION (ak:{}, inv:{})', access_key, inv_id)
    async with dbpool.acquire() as conn:
        query = (sa.update(vfolder_invitations)
                   .values(permission=perm)
                   .where(vfolder_invitations.c.id == inv_id)
                   .where(vfolder_invitations.c.inviter == request['user']['email'])
                   .where(vfolder_invitations.c.state == VFolderInvitationState.PENDING))
        await conn.execute(query)
    resp = {'msg': f'vfolder invitation updated: {inv_id}.'}
    return web.json_response(resp, status=200)


@atomic
@auth_required
@server_status_required(ALL_ALLOWED)
@check_api_params(
    t.Dict({
        tx.AliasedKey(['perm', 'permission'], default='rw'): VFolderPermissionValidator,
        tx.AliasedKey(['emails', 'user_ids', 'userIDs']): t.List(t.String),
    })
)
async def invite(request: web.Request, params: Any) -> web.Response:
    dbpool = request.app['dbpool']
    folder_name = request.match_info['name']
    access_key = request['keypair']['access_key']
    user_uuid = request['user']['uuid']
    perm = params['perm']
    invitee_emails = params['emails']
    log.info('VFOLDER.INVITE (ak:{}, vf:{}, inv.users:{})',
             access_key, folder_name, ','.join(invitee_emails))
    if folder_name.startswith('.'):
        raise GenericForbidden('Cannot share private dot-prefixed vfolders.')
    async with dbpool.acquire() as conn:
        # Get virtual folder.
        query = (sa.select('*')
                   .select_from(vfolders)
                   .where((vfolders.c.user == user_uuid) &
                          (vfolders.c.name == folder_name)))
        try:
            result = await conn.execute(query)
        except psycopg2.DataError:
            raise InvalidAPIParameters
        vf = await result.first()
        if vf is None:
            raise VFolderNotFound()

        # Get invited user's keypairs except vfolder owner.
        query = (sa.select([keypairs.c.user_id, keypairs.c.user])
                   .select_from(keypairs)
                   .where(keypairs.c.user_id.in_(invitee_emails))
                   .where(keypairs.c.user_id != request['user']['email']))
        try:
            result = await conn.execute(query)
        except psycopg2.DataError:
            raise InvalidAPIParameters
        if result.rowcount < 1:
            raise GenericNotFound('No such vfolder invitation')
        kps = await result.fetchall()

        # Prevent inviting user who already share the target folder.
        invitee_uuids = [kp.user for kp in kps]
        j = sa.join(vfolders, vfolder_permissions,
                    vfolders.c.id == vfolder_permissions.c.vfolder)
        query = (sa.select([vfolders.c.id])
                   .select_from(j)
                   .where((vfolders.c.user.in_(invitee_uuids) |
                           vfolder_permissions.c.user.in_(invitee_uuids)) &
                          (vfolders.c.name == folder_name)))
        result = await conn.execute(query)
        if result.rowcount > 0:
            raise VFolderAlreadyExists

        # Create invitation.
        invitees = [kp.user_id for kp in kps]
        invited_ids = []
        for invitee in set(invitees):
            inviter = request['user']['id']
            # Do not create invitation if already exists.
            query = (sa.select('*')
                       .select_from(vfolder_invitations)
                       .where((vfolder_invitations.c.inviter == inviter) &
                              (vfolder_invitations.c.invitee == invitee) &
                              (vfolder_invitations.c.vfolder == vf.id) &
                              (vfolder_invitations.c.state == VFolderInvitationState.PENDING)))
            result = await conn.execute(query)
            if result.rowcount > 0:
                continue

            # TODO: insert multiple values with one query.
            #       insert().values([{}, {}, ...]) does not work:
            #       sqlalchemy.exc.CompileError: The 'default' dialect with current
            #       database version settings does not support in-place multirow
            #       inserts.
            query = (vfolder_invitations.insert().values({
                'id': uuid.uuid4().hex,
                'permission': perm,
                'vfolder': vf.id,
                'inviter': inviter,
                'invitee': invitee,
                'state': VFolderInvitationState.PENDING,
            }))
            try:
                await conn.execute(query)
                invited_ids.append(invitee)
            except psycopg2.DataError:
                pass
    resp = {'invited_ids': invited_ids}
    return web.json_response(resp, status=201)


@atomic
@auth_required
@server_status_required(READ_ALLOWED)
async def invitations(request: web.Request) -> web.Response:
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.INVITATIONS (ak:{})', access_key)
    async with dbpool.acquire() as conn:
        j = sa.join(vfolders, vfolder_invitations,
                    vfolders.c.id == vfolder_invitations.c.vfolder)
        query = (sa.select([vfolder_invitations, vfolders.c.name])
                   .select_from(j)
                   .where((vfolder_invitations.c.invitee == request['user']['id']) &
                          (vfolder_invitations.c.state == VFolderInvitationState.PENDING)))
        result = await conn.execute(query)
        invitations = await result.fetchall()
    invs_info = []
    for inv in invitations:
        invs_info.append({
            'id': str(inv.id),
            'inviter': inv.inviter,
            'invitee': inv.invitee,
            'perm': inv.permission,
            'state': inv.state,
            'created_at': str(inv.created_at),
            'modified_at': str(inv.modified_at),
            'vfolder_id': str(inv.vfolder),
            'vfolder_name': inv.name,
        })
    resp = {'invitations': invs_info}
    return web.json_response(resp, status=200)


@atomic
@auth_required
@server_status_required(ALL_ALLOWED)
@check_api_params(
    t.Dict({
        t.Key('inv_id'): t.String,
    })
)
async def accept_invitation(request: web.Request, params: Any) -> web.Response:
    '''Accept invitation by invitee.

    * `inv_ak` parameter is removed from 19.06 since virtual folder's ownership is
    moved from keypair to a user or a group.

    :param inv_id: ID of vfolder_invitations row.
    '''
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    user_uuid = request['user']['uuid']
    inv_id = params['inv_id']
    log.info('VFOLDER.ACCEPT_INVITATION (ak:{}, inv:{})', access_key, inv_id)
    async with dbpool.acquire() as conn:
        # Get invitation.
        query = (sa.select([vfolder_invitations])
                   .select_from(vfolder_invitations)
                   .where((vfolder_invitations.c.id == inv_id) &
                          (vfolder_invitations.c.state == VFolderInvitationState.PENDING)))
        result = await conn.execute(query)
        invitation = await result.first()
        if invitation is None:
            raise GenericNotFound('No such vfolder invitation')

        # Get target virtual folder.
        query = (sa.select([vfolders.c.name])
                   .select_from(vfolders)
                   .where(vfolders.c.id == invitation.vfolder))
        result = await conn.execute(query)
        target_vfolder = await result.first()
        if target_vfolder is None:
            raise VFolderNotFound

        # Prevent accepting vfolder with duplicated name.
        j = sa.join(vfolders, vfolder_permissions,
                    vfolders.c.id == vfolder_permissions.c.vfolder, isouter=True)
        query = (sa.select([vfolders.c.id])
                   .select_from(j)
                   .where(((vfolders.c.user == user_uuid) |
                           (vfolder_permissions.c.user == user_uuid)) &
                          (vfolders.c.name == target_vfolder.name)))
        result = await conn.execute(query)
        if result.rowcount > 0:
            raise VFolderAlreadyExists

        # Create permission relation between the vfolder and the invitee.
        query = (vfolder_permissions.insert().values({
            'permission': VFolderPermission(invitation.permission),
            'vfolder': invitation.vfolder,
            'user': user_uuid,
        }))
        await conn.execute(query)

        # Clear used invitation.
        query = (vfolder_invitations.update()
                                    .where(vfolder_invitations.c.id == inv_id)
                                    .values(state=VFolderInvitationState.ACCEPTED))
        await conn.execute(query)
    return web.json_response({})


@atomic
@auth_required
@server_status_required(ALL_ALLOWED)
@check_api_params(
    t.Dict({
        t.Key('inv_id'): t.String,
    }))
async def delete_invitation(request: web.Request, params: Any) -> web.Response:
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    request_email = request['user']['email']
    inv_id = params['inv_id']
    log.info('VFOLDER.DELETE_INVITATION (ak:{}, inv:{})', access_key, inv_id)
    try:
        async with dbpool.acquire() as conn:
            query = (sa.select([vfolder_invitations.c.inviter,
                                vfolder_invitations.c.invitee])
                       .select_from(vfolder_invitations)
                       .where((vfolder_invitations.c.id == inv_id) &
                              (vfolder_invitations.c.state == VFolderInvitationState.PENDING)))
            result = await conn.execute(query)
            row = await result.first()
            if row is None:
                raise GenericNotFound('No such vfolder invitation')
            if request_email == row.inviter:
                state = VFolderInvitationState.CANCELED
            elif request_email == row.invitee:
                state = VFolderInvitationState.REJECTED
            else:
                raise GenericForbidden('Cannot change other user\'s invitaiton')
            query = (vfolder_invitations
                     .update()
                     .where(vfolder_invitations.c.id == inv_id)
                     .values(state=state))
            await conn.execute(query)
    except (psycopg2.IntegrityError, sa.exc.IntegrityError) as e:
        raise InternalServerError(f'integrity error: {e}')
    except (asyncio.CancelledError, asyncio.TimeoutError):
        raise
    except Exception as e:
        raise InternalServerError(f'unexpected error: {e}')
    return web.json_response({})


@auth_required
@server_status_required(ALL_ALLOWED)
async def delete(request: web.Request) -> web.Response:
    dbpool = request.app['dbpool']
    folder_name = request.match_info['name']
    access_key = request['keypair']['access_key']
    domain_name = request['user']['domain_name']
    user_role = request['user']['role']
    user_uuid = request['user']['uuid']
    allowed_vfolder_types = await request.app['shared_config'].get_vfolder_types()
    log.info('VFOLDER.DELETE (ak:{}, vf:{})', access_key, folder_name)
    async with dbpool.acquire() as conn, conn.begin():
        entries = await query_accessible_vfolders(
            conn, user_uuid,
            user_role=user_role, domain_name=domain_name,
            allowed_vfolder_types=allowed_vfolder_types)
        for entry in entries:
            if entry['name'] == folder_name:
                # Folder owner OR user who have DELETE permission can delete folder.
                if (
                    not entry['is_owner']
                    and entry['permission'] != VFolderPermission.RW_DELETE
                ):
                    raise InvalidAPIParameters(
                        'Cannot delete the vfolder '
                        'that is not owned by myself.')
                break
        else:
            raise InvalidAPIParameters('No such vfolder.')
        folder_host = entry['host']
        folder_id = entry['id']
        query = (vfolders.delete().where(vfolders.c.id == folder_id))
        await conn.execute(query)
    # fs-level deletion may fail or take longer time
    # but let's complete the db transaction to reflect that it's deleted.
    storage_manager = request.app['storage_manager']
    proxy_name, volume_name = storage_manager.split_host(folder_host)
    try:
        async with storage_manager.request(
            proxy_name, 'POST', 'folder/delete',
            json={
                'volume': volume_name,
                'vfid': str(folder_id),
            },
            raise_for_status=True,
        ):
            pass
    except aiohttp.ClientResponseError:
        raise VFolderOperationFailed
    return web.Response(status=204)


@atomic
@auth_required
@server_status_required(ALL_ALLOWED)
@vfolder_permission_required(VFolderPermission.READ_ONLY)
async def leave(request: web.Request, row: VFolderRow) -> web.Response:
    '''
    Leave a shared vfolder.

    Cannot leave a group vfolder or a vfolder that the requesting user owns.
    '''
    if row['ownership_type'] == VFolderOwnershipType.GROUP:
        raise InvalidAPIParameters('Cannot leave a group vfolder.')
    if row['is_owner']:
        raise InvalidAPIParameters('Cannot leave a vfolder owned by the requesting user.')

    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    user_uuid = request['user']['uuid']
    vfolder_id = row['id']
    perm = None
    log.info('VFOLDER.LEAVE(ak:{}, vfid:{}, uid:{}, perm:{})',
             access_key, vfolder_id, user_uuid, perm)
    async with dbpool.acquire() as conn:
        query = (
            vfolder_permissions
            .delete()
            .where(vfolder_permissions.c.vfolder == vfolder_id)
            .where(vfolder_permissions.c.user == user_uuid)
        )
        await conn.execute(query)
    resp = {'msg': 'left the shared vfolder'}
    return web.json_response(resp, status=200)


@atomic
@auth_required
@server_status_required(ALL_ALLOWED)
@vfolder_permission_required(VFolderPermission.READ_ONLY)
@check_api_params(
    t.Dict({
        t.Key('target_name'): tx.Slug(allow_dot=True),
        t.Key('target_host', default=None) >> 'folder_host': t.String | t.Null,
        t.Key('usage_mode', default='general'): tx.Enum(VFolderUsageMode) | t.Null,
        t.Key('permission', default='rw'): tx.Enum(VFolderPermission) | t.Null
    })
)
async def clone(request: web.Request, params: Any, row: VFolderRow) -> web.Response:
    resp: Dict[str, Any] = {}
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    user_role = request['user']['role']
    user_uuid = request['user']['uuid']
    resource_policy = request['keypair']['resource_policy']
    domain_name = request['user']['domain_name']
    log.info('VFOLDER.CLONE (ak:{}, vf:{}, vft:{}, vfh:{}, umod:{}, perm:{})',
             access_key, row['name'], params['target_name'], params['folder_host'],
             params['usage_mode'].value, params['permission'].value)
    source_folder_host = row['host']
    target_folder_host = params['folder_host']

    # check if the source vfolder is allowed to be cloned
    if not row['cloneable']:
        raise GenericForbidden('The source vfolder is not permitted to be cloned.')

    if not target_folder_host:
        target_folder_host = \
            await request.app['shared_config'].etcd.get('volumes/default_host')
        if not target_folder_host:
            raise InvalidAPIParameters(
                'You must specify the vfolder host '
                'because the default host is not configured.')

    allowed_vfolder_types = await request.app['shared_config'].get_vfolder_types()
    for vf_type in allowed_vfolder_types:
        if vf_type not in ('user', 'group'):
            raise ServerMisconfiguredError(
                f'Invalid vfolder type(s): {str(allowed_vfolder_types)}.'
                ' Only "user" or "group" is allowed.')

    if not verify_vfolder_name(params['target_name']):
        raise InvalidAPIParameters(f'{params["target_name"]} is reserved for internal operations.')

    async with dbpool.acquire() as conn:
        allowed_hosts = await get_allowed_vfolder_hosts_by_user(conn, resource_policy,
                                                                domain_name, user_uuid)
        # TODO: handle legacy host lists assuming that volume names don't overlap?
        if target_folder_host not in allowed_hosts:
            raise InvalidAPIParameters('You are not allowed to use this vfolder host.')

        # Check resource policy's max_vfolder_count
        if resource_policy['max_vfolder_count'] > 0:
            query = (sa.select([sa.func.count()])
                        .where(vfolders.c.user == user_uuid))
            result = await conn.scalar(query)
            if result >= resource_policy['max_vfolder_count']:
                raise InvalidAPIParameters('You cannot create more vfolders.')

        # Prevent creation of vfolder with duplicated name.
        extra_vf_conds = [vfolders.c.name == params['target_name']]
        extra_vf_conds.append(vfolders.c.host == target_folder_host)
        entries = await query_accessible_vfolders(
            conn, user_uuid,
            user_role=user_role, domain_name=domain_name,
            allowed_vfolder_types=allowed_vfolder_types,
            extra_vf_conds=(sa.and_(*extra_vf_conds))
        )
        if len(entries) > 0:
            raise VFolderAlreadyExists
        if params['target_name'].startswith('.'):
            dotfiles, _ = await query_owned_dotfiles(conn, access_key)
            for dotfile in dotfiles:
                if params['target_name'] == dotfile['path']:
                    raise InvalidAPIParameters('vFolder name conflicts with your dotfile.')

        if 'user' not in allowed_vfolder_types:
            raise InvalidAPIParameters('user vfolder cannot be created in this host')

        storage_manager = request.app['storage_manager']
        source_proxy_name, source_volume_name = storage_manager.split_host(source_folder_host)
        target_proxy_name, target_volume_name = storage_manager.split_host(target_folder_host)
        if source_proxy_name != target_proxy_name:
            raise InvalidAPIParameters('proxy name of source and target vfolders must be equal.')

        # TODO: accept quota as input parameter and pass as argument options
        try:
            folder_id = uuid.uuid4()
            async with storage_manager.request(
                source_folder_host, 'POST', 'folder/clone',
                json={
                    'src_volume': source_volume_name,
                    'src_vfid': str(row['id']),
                    'dst_volume': target_volume_name,
                    'dst_vfid': str(folder_id),
                },
                raise_for_status=True,
            ):
                pass
        except aiohttp.ClientResponseError:
            raise VFolderOperationFailed

        user_uuid = str(user_uuid)
        group_uuid = None
        ownership_type = 'user'
        insert_values = {
            'id': folder_id.hex,
            'name': params['target_name'],
            'usage_mode': params['usage_mode'],
            'permission': params['permission'],
            'last_used': None,
            'host': target_folder_host,
            'creator': request['user']['email'],
            'ownership_type': VFolderOwnershipType(ownership_type),
            'user': user_uuid,
            'group': group_uuid,
            'unmanaged_path': '',
            'cloneable': False
        }
        resp = {
            'id': folder_id.hex,
            'name': params['target_name'],
            'host': target_folder_host,
            'usage_mode': params['usage_mode'].value,
            'permission': params['permission'].value,
            'creator': request['user']['email'],
            'ownership_type': ownership_type,
            'user': user_uuid,
            'group': group_uuid,
        }
        query = (vfolders.insert().values(insert_values))
        try:
            result = await conn.execute(query)
        except psycopg2.DataError:
            raise InvalidAPIParameters
        assert result.rowcount == 1
    return web.json_response(resp, status=201)


@atomic
@auth_required
@server_status_required(READ_ALLOWED)
@check_api_params(
    t.Dict({
        tx.AliasedKey(['vfolder_id', 'vfolderId']): tx.UUID,
    })
)
async def list_shared_vfolders(request: web.Request, params: Any) -> web.Response:
    '''
    List shared vfolders.

    Not available for group vfolders.
    '''
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    target_vfid = params['vfolder_id']
    log.info('VFOLDER.LIST_SHARED_VFOLDERS (ak:{})', access_key)
    async with dbpool.acquire() as conn:
        j = (vfolder_permissions
             .join(vfolders, vfolders.c.id == vfolder_permissions.c.vfolder)
             .join(users, users.c.uuid == vfolder_permissions.c.user))
        query = (sa.select([vfolder_permissions,
                            vfolders.c.id, vfolders.c.name,
                            users.c.email])
                   .select_from(j)
                   .where((vfolders.c.user == request['user']['uuid'])))
        if target_vfid is not None:
            query = query.where(vfolders.c.id == target_vfid)
        result = await conn.execute(query)
        shared_list = await result.fetchall()
    shared_info = []
    for shared in shared_list:
        shared_info.append({
            'vfolder_id': str(shared.id),
            'vfolder_name': str(shared.name),
            'shared_by': request['user']['email'],
            'shared_to': {
                'uuid': str(shared.user),
                'email': shared.email,
            },
            'perm': shared.permission.value,
        })
    resp = {'shared': shared_info}
    return web.json_response(resp, status=200)


@atomic
@auth_required
@server_status_required(ALL_ALLOWED)
@check_api_params(
    t.Dict({
        t.Key('vfolder'): tx.UUID,
        t.Key('user'): tx.UUID,
        tx.AliasedKey(['perm', 'permission']): VFolderPermissionValidator | t.Null,
    })
)
async def update_shared_vfolder(request: web.Request, params: Any) -> web.Response:
    '''
    Update permission for shared vfolders.

    If params['perm'] is None, remove user's permission for the vfolder.
    '''
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    vfolder_id = params['vfolder']
    user_uuid = params['user']
    perm = params['perm']
    log.info('VFOLDER.UPDATE_SHARED_VFOLDER(ak:{}, vfid:{}, uid:{}, perm:{})',
             access_key, vfolder_id, user_uuid, perm)
    async with dbpool.acquire() as conn:
        if perm is not None:
            query = (
                sa.update(vfolder_permissions)
                .values(permission=perm)
                .where(vfolder_permissions.c.vfolder == vfolder_id)
                .where(vfolder_permissions.c.user == user_uuid)
            )
        else:
            query = (
                vfolder_permissions
                .delete()
                .where(vfolder_permissions.c.vfolder == vfolder_id)
                .where(vfolder_permissions.c.user == user_uuid)
            )
        await conn.execute(query)
    resp = {'msg': 'shared vfolder permission updated'}
    return web.json_response(resp, status=200)


@superadmin_required
@server_status_required(READ_ALLOWED)
@check_api_params(
    t.Dict({
        t.Key('fstab_path', default=None): t.String | t.Null,
        t.Key('agent_id', default=None): t.String | t.Null,
    }),
)
async def get_fstab_contents(request: web.Request, params: Any) -> web.Response:
    '''
    Return the contents of `/etc/fstab` file.
    '''
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.GET_FSTAB_CONTENTS(ak:{}, ag:{})', access_key, params['agent_id'])
    if params['fstab_path'] is None:
        params['fstab_path'] = '/etc/fstab'
    if params['agent_id'] is not None:
        # Return specific agent's fstab.
        watcher_info = await get_watcher_info(request, params['agent_id'])
        try:
            client_timeout = aiohttp.ClientTimeout(total=10.0)
            async with aiohttp.ClientSession(timeout=client_timeout) as sess:
                headers = {'X-BackendAI-Watcher-Token': watcher_info['token']}
                url = watcher_info['addr'] / 'fstab'
                async with sess.get(url, headers=headers, params=params) as watcher_resp:
                    if watcher_resp.status == 200:
                        content = await watcher_resp.text()
                        resp = {
                            'content': content,
                            'node': 'agent',
                            'node_id': params['agent_id'],
                        }
                        return web.json_response(resp)
                    else:
                        message = await watcher_resp.text()
                        raise BackendAgentError(
                            'FAILURE', f'({watcher_resp.status}: {watcher_resp.reason}) {message}')
        except asyncio.CancelledError:
            raise
        except asyncio.TimeoutError:
            log.error('VFOLDER.GET_FSTAB_CONTENTS(u:{}): timeout from watcher (agent:{})',
                      access_key, params['agent_id'])
            raise BackendAgentError('TIMEOUT', 'Could not fetch fstab data from agent')
        except Exception:
            log.exception('VFOLDER.GET_FSTAB_CONTENTS(u:{}): '
                          'unexpected error while reading from watcher (agent:{})',
                          access_key, params['agent_id'])
            raise InternalServerError
    else:
        resp = {
            'content':
                "# Since Backend.AI 20.09, reading the manager fstab is no longer supported.",
            'node': 'manager',
            'node_id': 'manager',
        }
        return web.json_response(resp)


@superadmin_required
@server_status_required(READ_ALLOWED)
async def list_mounts(request: web.Request) -> web.Response:
    '''
    List all mounted vfolder hosts in vfroot.

    All mounted hosts from connected (ALIVE) agents are also gathered.
    Generally, agents should be configured to have same hosts structure,
    but newly introduced one may not.
    '''
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    log.info('VFOLDER.LIST_MOUNTS(ak:{})', access_key)
    config = request.app['shared_config']
    mount_prefix = await config.get_raw('volumes/_mount')
    if mount_prefix is None:
        mount_prefix = '/mnt'

    # NOTE: Changed in 20.09: the manager instances no longer have mountpoints.
    storage_manager: StorageSessionManager = request.app['storage_manager']
    all_volumes = [*await storage_manager.get_all_volumes()]
    all_mounts = [
        volume_data['path']
        for proxy_name, volume_data in all_volumes
    ]
    all_vfolder_hosts = [
        f"{proxy_name}:{volume_data['name']}"
        for proxy_name, volume_data in all_volumes
    ]
    resp: MutableMapping[str, Any] = {
        'manager': {
            'success': True,
            'mounts': all_mounts,
            'message': '(legacy)',
        },
        'storage-proxy': {
            'success': True,
            'mounts': [*zip(all_vfolder_hosts, all_mounts)],
            'message': '',
        },
        'agents': {},
    }

    # Scan mounted vfolder hosts for connected agents.
    async def _fetch_mounts(sess: aiohttp.ClientSession, agent_id: str) -> Tuple[str, Mapping]:
        watcher_info = await get_watcher_info(request, agent_id)
        headers = {'X-BackendAI-Watcher-Token': watcher_info['token']}
        url = watcher_info['addr'] / 'mounts'
        try:
            async with sess.get(url, headers=headers) as watcher_resp:
                if watcher_resp.status == 200:
                    data = {
                        'success': True,
                        'mounts': await watcher_resp.json(),
                        'message': '',
                    }
                else:
                    data = {
                        'success': False,
                        'mounts': [],
                        'message': await watcher_resp.text(),
                    }
                return (agent_id, data,)
        except asyncio.CancelledError:
            raise
        except asyncio.TimeoutError:
            log.error('VFOLDER.LIST_MOUNTS(u:{}): timeout from watcher (agent:{})',
                      access_key, agent_id)
            raise
        except Exception:
            log.exception('VFOLDER.LIST_MOUNTS(u:{}): '
                          'unexpected error while reading from watcher (agent:{})',
                          access_key, agent_id)
            raise

    async with dbpool.acquire() as conn:
        query = (sa.select([agents.c.id])
                   .select_from(agents)
                   .where(agents.c.status == AgentStatus.ALIVE))
        result = await conn.execute(query)
        rows = await result.fetchall()

    client_timeout = aiohttp.ClientTimeout(total=10.0)
    async with aiohttp.ClientSession(timeout=client_timeout) as sess:
        scheduler = await aiojobs.create_scheduler(limit=8)
        try:
            jobs = await asyncio.gather(*[
                scheduler.spawn(_fetch_mounts(sess, row.id)) for row in rows
            ])
            mounts = await asyncio.gather(*[job.wait() for job in jobs],
                                          return_exceptions=True)
            for mount in mounts:
                if isinstance(mount, Exception):
                    # exceptions are already logged.
                    continue
                resp['agents'][mount[0]] = mount[1]
        finally:
            await scheduler.close()

    return web.json_response(resp, status=200)


@superadmin_required
@server_status_required(ALL_ALLOWED)
@check_api_params(
    t.Dict({
        t.Key('fs_location'): t.String,
        t.Key('name'): t.String,
        t.Key('fs_type', default='nfs'): t.String,
        t.Key('options', default=None): t.String | t.Null,
        t.Key('scaling_group', default=None): t.String | t.Null,
        t.Key('fstab_path', default=None): t.String | t.Null,
        t.Key('edit_fstab', default=False): t.ToBool,
    }),
)
async def mount_host(request: web.Request, params: Any) -> web.Response:
    '''
    Mount device into vfolder host.

    Mount a device (eg: nfs) located at `fs_location` into `<vfroot>/name` in the
    host machines (manager and all agents). `fs_type` can be specified by requester,
    which fallbaks to 'nfs'.

    If `scaling_group` is specified, try to mount for agents in the scaling group.
    '''
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    log_fmt = 'VFOLDER.MOUNT_HOST(ak:{}, name:{}, fs:{}, sg:{})'
    log_args = (access_key, params['name'], params['fs_location'], params['scaling_group'])
    log.info(log_fmt, *log_args)
    config = request.app['shared_config']
    mount_prefix = await config.get_raw('volumes/_mount')
    if mount_prefix is None:
        mount_prefix = '/mnt'

    # NOTE: Changed in 20.09: the manager instances no longer have mountpoints.
    resp: MutableMapping[str, Any] = {
        'manager': {
            'success': True,
            'message': 'Managers do not have mountpoints since v20.09.',
        },
        'agents': {},
    }

    # Mount on running agents.
    async with dbpool.acquire() as conn:
        query = (sa.select([agents.c.id])
                   .select_from(agents)
                   .where(agents.c.status == AgentStatus.ALIVE))
        if params['scaling_group'] is not None:
            query = query.where(agents.c.scaling == params['scaling_group'])
        result = await conn.execute(query)
        rows = await result.fetchall()

    async def _mount(sess: aiohttp.ClientSession, agent_id: str) -> Tuple[str, Mapping]:
        watcher_info = await get_watcher_info(request, agent_id)
        try:
            headers = {'X-BackendAI-Watcher-Token': watcher_info['token']}
            url = watcher_info['addr'] / 'mounts'
            async with sess.post(url, json=params, headers=headers) as resp:
                if resp.status == 200:
                    data = {
                        'success': True,
                        'message': await resp.text(),
                    }
                else:
                    data = {
                        'success': False,
                        'message': await resp.text(),
                    }
                return (agent_id, data,)
        except asyncio.CancelledError:
            raise
        except asyncio.TimeoutError:
            log.error(log_fmt + ': timeout from watcher (ag:{})',
                      *log_args, agent_id)
            raise
        except Exception:
            log.exception(log_fmt + ': unexpected error while reading from watcher (ag:{})',
                          *log_args, agent_id)
            raise

    client_timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=client_timeout) as sess:
        scheduler = await aiojobs.create_scheduler(limit=8)
        try:
            jobs = await asyncio.gather(*[
                scheduler.spawn(_mount(sess, row.id)) for row in rows
            ])
            results = await asyncio.gather(*[job.wait() for job in jobs],
                                           return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    # exceptions are already logged.
                    continue
                resp['agents'][result[0]] = result[1]
        finally:
            await scheduler.close()

    return web.json_response(resp, status=200)


@superadmin_required
@server_status_required(ALL_ALLOWED)
@check_api_params(
    t.Dict({
        t.Key('name'): t.String,
        t.Key('scaling_group', default=None): t.String | t.Null,
        t.Key('fstab_path', default=None): t.String | t.Null,
        t.Key('edit_fstab', default=False): t.ToBool,
    }),
)
async def umount_host(request: web.Request, params: Any) -> web.Response:
    '''
    Unmount device from vfolder host.

    Unmount a device (eg: nfs) located at `<vfroot>/name` from the host machines
    (manager and all agents).

    If `scaling_group` is specified, try to unmount for agents in the scaling group.
    '''
    dbpool = request.app['dbpool']
    access_key = request['keypair']['access_key']
    log_fmt = 'VFOLDER.UMOUNT_HOST(ak:{}, name:{}, sg:{})'
    log_args = (access_key, params['name'], params['scaling_group'])
    log.info(log_fmt, *log_args)
    config = request.app['shared_config']
    mount_prefix = await config.get_raw('volumes/_mount')
    if mount_prefix is None:
        mount_prefix = '/mnt'
    mountpoint = Path(mount_prefix) / params['name']
    assert Path(mount_prefix) != mountpoint

    async with dbpool.acquire() as conn, conn.begin():
        # Prevent unmount if target host is mounted to running kernels.
        query = (sa.select([kernels.c.mounts])
                   .select_from(kernels)
                   .where(kernels.c.status != KernelStatus.TERMINATED))
        result = await conn.execute(query)
        _kernels = await result.fetchall()
        _mounted = set()
        for kern in _kernels:
            if kern.mounts:
                _mounted.update([m[1] for m in kern.mounts])
        if params['name'] in _mounted:
            return web.json_response({
                'title': 'Target host is used in sessions',
                'message': 'Target host is used in sessions',
            }, status=409)

        query = (sa.select([agents.c.id])
                   .select_from(agents)
                   .where(agents.c.status == AgentStatus.ALIVE))
        if params['scaling_group'] is not None:
            query = query.where(agents.c.scaling == params['scaling_group'])
        result = await conn.execute(query)
        _agents = await result.fetchall()

    # Unmount from manager.
    resp: MutableMapping[str, Any] = {
        'manager': {
            'success': True,
            'message': 'Managers do not have mountpoints since v20.09.',
        },
        'agents': {},
    }
    if params['edit_fstab'] and resp['manager']['success']:
        fstab_path = params['fstab_path'] if params['fstab_path'] else '/etc/fstab'
        # NOTE: ignoring type error due to a regression in mypy 0.790, maybe typeshed version mismatch
        async with aiofiles.open(fstab_path, mode='r+') as fp:  # type: ignore
            fstab = Fstab(fp)
            await fstab.remove_by_mountpoint(str(mountpoint))

    # Unmount from running agents.
    async def _umount(sess: aiohttp.ClientSession, agent_id: str) -> Tuple[str, Mapping]:
        watcher_info = await get_watcher_info(request, agent_id)
        try:
            headers = {'X-BackendAI-Watcher-Token': watcher_info['token']}
            url = watcher_info['addr'] / 'mounts'
            async with sess.delete(url, json=params, headers=headers) as resp:
                if resp.status == 200:
                    data = {
                        'success': True,
                        'message': await resp.text(),
                    }
                else:
                    data = {
                        'success': False,
                        'message': await resp.text(),
                    }
                return (agent_id, data,)
        except asyncio.CancelledError:
            raise
        except asyncio.TimeoutError:
            log.error(log_fmt + ': timeout from watcher (agent:{})',
                      *log_args, agent_id)
            raise
        except Exception:
            log.exception(log_fmt + ': unexpected error while reading from watcher (agent:{})',
                          *log_args, agent_id)
            raise

    client_timeout = aiohttp.ClientTimeout(total=10.0)
    async with aiohttp.ClientSession(timeout=client_timeout) as sess:
        scheduler = await aiojobs.create_scheduler(limit=8)
        try:
            jobs = await asyncio.gather(*[
                scheduler.spawn(_umount(sess, _agent.id)) for _agent in _agents
            ])
            results = await asyncio.gather(*[job.wait() for job in jobs],
                                           return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    # exceptions are already logged.
                    continue
                resp['agents'][result[0]] = result[1]
        finally:
            await scheduler.close()

    return web.json_response(resp, status=200)


async def init(app: web.Application) -> None:
    pass


async def shutdown(app: web.Application) -> None:
    pass


def create_app(default_cors_options):
    app = web.Application()
    app['prefix'] = 'folders'
    app['api_versions'] = (2, 3, 4)
    app.on_startup.append(init)
    app.on_shutdown.append(shutdown)
    cors = aiohttp_cors.setup(app, defaults=default_cors_options)
    add_route = app.router.add_route
    root_resource = cors.add(app.router.add_resource(r''))
    cors.add(root_resource.add_route('POST', create))
    cors.add(root_resource.add_route('GET',  list_folders))
    cors.add(root_resource.add_route('DELETE',  delete_by_id))
    vfolder_resource = cors.add(app.router.add_resource(r'/{name}'))
    cors.add(vfolder_resource.add_route('GET',    get_info))
    cors.add(vfolder_resource.add_route('DELETE', delete))
    cors.add(add_route('GET',    r'/_/hosts', list_hosts))
    cors.add(add_route('GET',    r'/_/all-hosts', list_all_hosts))
    cors.add(add_route('GET',    r'/_/allowed-types', list_allowed_types))
    cors.add(add_route('GET',    r'/_/all_hosts', list_all_hosts))          # legacy underbar
    cors.add(add_route('GET',    r'/_/allowed_types', list_allowed_types))  # legacy underbar
    cors.add(add_route('GET',    r'/_/perf-metric', get_volume_perf_metric))
    cors.add(add_route('POST',   r'/{name}/rename', rename_vfolder))
    cors.add(add_route('POST',   r'/{name}/update-options', update_vfolder_options))
    cors.add(add_route('POST',   r'/{name}/mkdir', mkdir))
    cors.add(add_route('POST',   r'/{name}/request-upload', create_upload_session))
    cors.add(add_route('POST',   r'/{name}/request-download', create_download_session))
    cors.add(add_route('POST',   r'/{name}/rename-file', rename_file))
    cors.add(add_route('DELETE', r'/{name}/delete-files', delete_files))
    cors.add(add_route('POST',   r'/{name}/rename_file', rename_file))    # legacy underbar
    cors.add(add_route('DELETE', r'/{name}/delete_files', delete_files))  # legacy underbar
    cors.add(add_route('GET',    r'/{name}/files', list_files))
    cors.add(add_route('POST',   r'/{name}/invite', invite))
    cors.add(add_route('POST',   r'/{name}/leave', leave))
    cors.add(add_route('POST',   r'/{name}/clone', clone))
    cors.add(add_route('GET',    r'/invitations/list-sent', list_sent_invitations))
    cors.add(add_route('GET',    r'/invitations/list_sent', list_sent_invitations))  # legacy underbar
    cors.add(add_route('POST',   r'/invitations/update/{inv_id}', update_invitation))
    cors.add(add_route('GET',    r'/invitations/list', invitations))
    cors.add(add_route('POST',   r'/invitations/accept', accept_invitation))
    cors.add(add_route('DELETE', r'/invitations/delete', delete_invitation))
    cors.add(add_route('GET',    r'/_/shared', list_shared_vfolders))
    cors.add(add_route('POST',   r'/_/shared', update_shared_vfolder))
    cors.add(add_route('GET',    r'/_/fstab', get_fstab_contents))
    cors.add(add_route('GET',    r'/_/mounts', list_mounts))
    cors.add(add_route('POST',   r'/_/mounts', mount_host))
    cors.add(add_route('DELETE', r'/_/mounts', umount_host))
    return app, []
