import json

from seek_agent.core.llm import LLMClient
from seek_agent.prompt.prompt_utils import load_system_prompt
from seek_agent.tools.tools import get_all_tools_schema, execute_tool


def _parse_tool_call_from_text(content: str) -> list:
    """从模型文本回复中解析 tool_call JSON 块，返回 tool_calls 列表。"""
    import re
    tool_calls = []

    # 匹配 ```tool_call ... ``` 代码块
    pattern = r'```tool_call\s*\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)

    for i, match in enumerate(matches):
        try:
            parsed = json.loads(match.strip())
            tool_calls.append({
                "id": f"call_{i}",
                "type": "function",
                "function": {
                    "name": parsed["name"],
                    "arguments": json.dumps(parsed.get("arguments", {}), ensure_ascii=False)
                }
            })
        except (json.JSONDecodeError, KeyError):
            continue

    return tool_calls


class ReActAgent:
    def __init__(self, client: LLMClient):
        self.client = client
        self.messages = []
        self.max_steps = 5
        self.system_prompt = load_system_prompt()
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]

    def run(self, user_message: str):
        self.messages.append({"role": "user", "content": user_message})
        step_messages = list(self.messages)
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"\n--- 第 {current_step} 步 ---")

            tools_schema = get_all_tools_schema()

            assistant_message = self.client.invoke(messages=step_messages, tools=tools_schema)

            if "tool_calls" not in assistant_message and assistant_message.get("content"):
                parsed_calls = _parse_tool_call_from_text(assistant_message["content"])
                if parsed_calls:
                    assistant_message["tool_calls"] = parsed_calls

            step_messages.append(assistant_message)

            if "tool_calls" not in assistant_message:
                final_content = assistant_message.get("content", "")
                self.messages.append({"role": "assistant", "content": final_content})
                print("Achieved Goal Successfully, return final content")
                return final_content

            print(f"Detected {len(assistant_message['tool_calls'])} tool request(s). Executing...")

            for tool_call in assistant_message["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                tool_args = tool_call["function"]["arguments"]
                tool_id = tool_call["id"]

                tool_result = execute_tool(tool_name, tool_args)

                print(f"全局工具执行返回: {tool_result}")

                step_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_id,
                    "name": tool_name,
                    "content": tool_result
                })
