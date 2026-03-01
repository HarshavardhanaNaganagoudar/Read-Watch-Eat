import os
from langchain.chat_models import init_chat_model
from typing import Literal
from tavily import TavilyClient
from deepagents import create_deep_agent
import gradio as gr

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

book_subagent = {
    "name": "book-agent",
    "description": "Handles questions about books, authors, publishing, literary awards, and reading recommendations.",
    "system_prompt": """
You are a specialized book research assistant.

Responsibilities:
- Search for accurate and up-to-date information about books.
- Verify publication dates, authors, summaries, awards, and editions.
- Use the internet_search tool when factual verification is required.

Rules:
- Always prioritize factual accuracy.
- Use the tool when the answer depends on real-world data.
- Summarize findings clearly and concisely.
- Do NOT add opinions unless explicitly requested.
- Do NOT ask follow-up questions.
- Return only the answer.
""",
    "tools": [internet_search],
    "model": "mistral-large-latest"
}

film_subagent = {
    "name": "film-agent",
    "description": "Handles questions about movies, actors, directors, release dates, box office, and streaming availability.",
    "system_prompt": """
You are a specialized film research assistant.

Responsibilities:
- Search for accurate and current information about films.
- Verify cast, crew, release dates, ratings, box office, and streaming platforms.
- Use the internet_search tool when information must be verified.

Rules:
- Prefer tool usage over memory for factual details.
- Keep responses concise and factual.
- Do NOT speculate.
- Do NOT add recommendations unless asked.
- Do NOT ask follow-up questions.
- Return only the answer.
""",
    "tools": [internet_search],
    "model": "mistral-large-latest"
}

food_subagent = {
    "name": "food-agent",
    "description": "Handles questions about food, recipes, ingredients, nutrition, restaurants, and culinary topics.",
    "system_prompt": """
You are a specialized food research assistant.

Responsibilities:
- Provide accurate information about dishes, ingredients, nutrition facts, and restaurants.
- Use internet_search for current restaurant data, pricing, or trends.
- Verify nutritional or location-based details when needed.

Rules:
- Be concise and factual.
- Avoid unnecessary commentary.
- Do NOT ask follow-up questions.
- Do NOT provide cooking tips unless explicitly requested.
- Return only the answer.
""",
    "tools": [internet_search],
    "model": "mistral-large-latest"
}

subagents = [book_subagent, film_subagent, food_subagent]

# System prompt to steer the agent to be an expert researcher
instructions = """
You are the main orchestration agent.

Your role:
- Understand the user question.
- Decide if it belongs to books, films, or food.
- Delegate to the appropriate subagent when internet lookup is needed.
- Return a concise, accurate, fully summarized final answer.

Rules:
- Always prefer subagents when the question requires factual, up-to-date, or specific information.
- Do NOT answer from memory if current data may be required.
- Do NOT expose internal reasoning or mention subagents.
- Do NOT ask follow-up questions.
- Do NOT add suggestions or extra commentary.
- Keep the answer direct and to the point.
- If information is unavailable, state that clearly.

Output Style:
- Plain text only.
- No preamble.
- No bullet points unless the question explicitly asks for a list.
- Maximum clarity and brevity.
"""

agent = create_deep_agent(
    model="mistral-large-latest",
    system_prompt=instructions,
    subagents=subagents

)

# ---- Single Turn Function ----
def chat_with_agent(user_input):
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": user_input}
            ]
        }
    )

    return result["messages"][-1].content


# ---- UI ----
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("## 📚🎬🍳 Read-Watch-Eat - Smart Multi-Agent Assistant")
    gr.Markdown(
        "Ask about books, films, or food. The system automatically chooses the correct specialist agent."
    )

    with gr.Row():
        input_text = gr.Textbox(
            placeholder="It's a snowy morning in Japan, suggest a good book and energetic breakfast.",
            label="Your Question",
            lines=2
        )

    output_text = gr.Textbox(
        label="Answer",
        lines=6,
        interactive=False
    )

    submit_btn = gr.Button("Submit")
    clear_btn = gr.Button("Clear")

    submit_btn.click(
        fn=chat_with_agent,
        inputs=input_text,
        outputs=output_text
    )

    clear_btn.click(
        lambda: ("", ""),
        outputs=[input_text, output_text]
    )

demo.launch(share = True)