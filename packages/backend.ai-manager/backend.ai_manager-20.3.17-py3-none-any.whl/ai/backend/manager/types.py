import enum
from typing import (
    Optional, Union,
)

import attr


@attr.s(auto_attribs=True, slots=True, frozen=True)
class BackgroundTaskEventArgs:
    task_id: str
    message: Optional[str] = None
    current_progress: Optional[Union[int, float]] = None
    total_progress: Optional[Union[int, float]] = None


# Sentinel is a special object that indicates a special status instead of a value
# where the user expects a value.
# According to the discussion in https://github.com/python/typing/issues/236,
# we define our Sentinel type as an enum with only one special value.
# This enables passing of type checks by "value is sentinel" (or "value is Sentinel.token")
# instead of more expensive "isinstance(value, Sentinel)" because we can assure type checkers
# to think there is no other possible instances of the Sentinel type.

class Sentinel(enum.Enum):
    token = 0
