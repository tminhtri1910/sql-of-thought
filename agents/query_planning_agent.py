import json
from typing import Dict, Any
from utils.openai_client import client 

def generate_logical_plan(
    question: str,
    linked_schema: Dict[str, Any],
    intent: str,
    model: str = "gpt-4.1-mini"
) -> Dict[str, Any]:
    """
    Generate a logical plan from linked schema and intent.
    Returns a JSON dict representing query plan.
    """
    prompt = f"""
You are an expert SQL planner.

Question: '{question}'
Intent: '{intent}'
Linked schema: {linked_schema}

Task: Generate a JSON logical plan with keys like:
select, from, join, where, group_by, order_by, limit,...

Do NOT include code fences such as ```json.
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text_output = response.choices[0].message.content.strip()
    try:
        logical_plan = json.loads(text_output)
    except json.JSONDecodeError:
        print("Plan error")
        logical_plan = {}
    return logical_plan
