def load_system_prompt() -> str:
    with open("seek_agent/prompt/SYSTEM_PROMPT.md", "r", encoding="utf-8") as f:
        return f.read().strip()
