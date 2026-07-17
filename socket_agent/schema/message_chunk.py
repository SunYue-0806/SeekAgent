from typing import Any

from socket_agent.schema.message import BaseMessage, AssistantMessage
from socket_agent.schema.tool_call import ToolCall


class BaseMessageChunk(BaseMessage):

    def __add__(self, other: "BaseMessageChunk") -> "BaseMessageChunk":
        if not isinstance(other, BaseMessageChunk):
            raise TypeError(f"Cannot add {self.__class__.__name__} to {type(other)}")

        if isinstance(self.content, str) and isinstance(other.content, str):
            combined_content = self.content + other.content
        elif isinstance(self.content, list) and isinstance(other.content, list):
            combined_content = self.content + other.content
        else:
            combined_content = other.content

        return self.__class__(role=self.role, content=combined_content, name=self.name or other.name)


class AssistantMessageChunk(AssistantMessage, BaseMessageChunk):
    def __add__(self, other: Any) -> "AssistantMessageChunk":
        if not isinstance(other, AssistantMessageChunk):
            raise TypeError(f"Cannot add AssistantMessageChunk to {type(other)}")

        if isinstance(self.content, str) and isinstance(other.content, str):
            combined_content = self.content + other.content
        elif isinstance(self.content, list) and isinstance(other.content, list):
            combined_content = self.content + other.content
        else:
            combined_content = other.content

        merged_tool_calls = []

        if self.tool_calls:
            for tool_call in self.tool_calls:
                merged_tool_calls.append(ToolCall(
                    id=tool_call.id,
                    name=tool_call.name,
                    arguments=tool_call.arguments,
                    index=tool_call.index
                ))