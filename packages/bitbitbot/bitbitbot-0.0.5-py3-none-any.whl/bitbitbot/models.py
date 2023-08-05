from typing import Optional

from pydantic import BaseModel


class TwitchTags(BaseModel):
    display_name: str
    color: Optional[str]
    user_id: str
    mod: str
    subscriber: str
