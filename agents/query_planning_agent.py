import json
from typing import Dict, Any
from utils.openai_client import client 

def generate_logical_plan(
    question: str,
    linked_schema: Dict[str, Any],
    sub_problems: Dict[str, Any],
    model: str
) -> str:
    """
    Generate a logical plan from linked schema and question.
    Returns a JSON dict representing query plan.
    """
    prompt = f"""
You are an expert SQL planner.

Question: '{question}'
Subproblems: '{sub_problems}'
Linked schema: {linked_schema}

Task: 
Generate a short, high-level plan, step by step with step number.
Explain what to do and the reason each step.
Return ONLY plan to build SQL query.
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        # temperature=0
    )

    logical_plan = response.choices[0].message.content.strip()
    # try:
    #     logical_plan = json.loads(text_output)
    # except json.JSONDecodeError:
    #     print("Plan error")
    #     logical_plan = {}
    return logical_plan
