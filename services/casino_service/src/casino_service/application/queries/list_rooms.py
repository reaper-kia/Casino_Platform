from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ListRoomsQuery:
    game_type: Optional[str] = None
    visibility: Optional[str] = None
    status: Optional[str] = None
    limit: int = 20
    cursor: Optional[str] = None