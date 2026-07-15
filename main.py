"""HelloAgents LLM 运行示例"""

from dotenv import load_dotenv

from seek_agent.agents.react_agent import ReActAgent
from seek_agent.core.llm import LLMClient
from seek_agent.tools import weather_tool

load_dotenv()


def main():
    llm_client = LLMClient()

    react_agent = ReActAgent(llm_client)

    while True:
        try:
            user_input = input("User ＞ ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("Agent ＞ 再见！")
                break

            response = react_agent.run(user_input)
            print(f"\nAgent ＞ {response}\n" + "=" * 40)

        except KeyboardInterrupt:
            print("\nAgent ＞ 检测到强行中断，退出。")
            break


if __name__ == "__main__":
    main()
