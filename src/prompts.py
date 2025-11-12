# prompts.py
PROMPT_TEMPLATES = {
    "default": 
    """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    """,
    "explanatory": "...",
    "step_by_step": "..."
}