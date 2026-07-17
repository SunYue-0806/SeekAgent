from dataclasses import Field

from pydantic import BaseModel
from typing import Union, List, Dict, Optional, Any

from socket_agent.schema.tool_call import ToolCall


class BaseMessage(BaseModel):
    role: str
    content: Union[str, List[Union[str, dict]]] = ""
    name: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AssistantMessage(BaseMessage):
    role: str = "assistant"
    tool_calls: Optional[List[ToolCall]]
    finish_reason: str = "null"
    parser_content: Optional[Any] = None
    reasoning_content: Optional[str] = None


class UserMessage(BaseMessage):
    role: str = "user"


class SystemMessage(BaseMessage):
    role: str = "system"


class ToolMessage(BaseMessage):
    role: str = "tool"
