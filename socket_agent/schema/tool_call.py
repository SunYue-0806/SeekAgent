from typing import Optional

from pydantic import BaseModel


class ToolCall(BaseModel):
    id: Optional[str]
    name: str
    type: str
    arguments: str
    index: Optional[int] = None
