"""HelloAgents LLM 运行示例"""

from dotenv import load_dotenv

from socket_agent.agents.react_agent import ReActAgent
from socket_agent.llm.openai_model_client import OpenAIModelClient

load_dotenv()


def main():
    llm_client = OpenAIModelClient()

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
