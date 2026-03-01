## Read-Watch-Eat is a minimal multi-agent AI assistant that intelligently routes your question to specialized subagents:

📖 Book Expert

🎬 Film Expert

🍳 Food Expert

The main agent analyzes your question, delegates it to the correct specialist, and returns a concise final answer.

---

## 🧠 How It Works
- The Main Agent decides which domain your question belongs to.
- The relevant Subagent performs research using live internet search.
- The final response is summarized and returned cleanly.
- This architecture reduces hallucinations and improves factual reliability.

---

## Architecture 

![Architecture](/Architecture.png)

Why use subagents?
- Subagents solve the context bloat problem. When agents use tools with large outputs (web search, file reads, database queries), the context window fills up quickly with intermediate results. Subagents isolate this detailed work—the main agent receives only the final result, not the dozens of tool calls that produced it.

---

🚀 Features

- 🔍 Internet-backed answers (via Tavily search)
- 🧩 Multi-agent delegation system
- 🎯 Concise, no-extra-text responses
- 🖥 Minimal Gradio UI
- 🧠 Clean orchestration logic
- ⚡ Single-turn interaction (stateless)

---

🛠 Tech Stack

- deepagents — agent orchestration
- langchain — model integration
- tavily — web search
- gradio — UI
- mistral-large — LLM backend

---


## 🚀 Live Demo

Try it out:

[👉 Launch on Hugging Face Spaces](https://huggingface.co/spaces/nharshavardhana/Read-Watch-Eat)

---
## 📺 Demo Video

🎥 [Watch the Demo on YouTube](https://youtu.be/s3Bv1rRQYSw?si=3x4_83iZjIpvsIpw)

---
## Demo Screen
![Demo](/Demo-Screen.png)
