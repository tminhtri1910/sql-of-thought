from utils.openai_client import client 
from typing import Dict, Any
import json

def classify_intent(question: str, linked_schema: Dict[str, Any], model: str) -> Dict[str, Any]:
    """
    Use LLM to classify a natural language question into a basic SQL sub_problems:
    select, aggregation, join, filter, set_operation
    """
    prompt = f"""
You are an expert SQL assistant.

Question: "{question}"
Linked schema: {linked_schema}

Task: Generate a JSON clause-level subproblems with keys like:
select, from, join, where, group_by, order_by, limit,...
Each identified clause is expressed as a key–value pair in a structured JSON object, where the key is the clause type and the value is the partially completed clause expression.

Do NOT include code fences such as ```json.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        # temperature=0
    )

    sub_problems = response.choices[0].message.content.strip()
    text_output = response.choices[0].message.content.strip()
    try:
        sub_problems = json.loads(text_output)
    except json.JSONDecodeError:
        print("Plan error")
        sub_problems = {}
    # valid_intents = ["select", "aggregation", "join", "filter", "set_operation"]
    # if sub_problems not in valid_intents:
    #     sub_problems = "select"
    return sub_problems

# Example usage
if __name__ == "__main__":
    questions = [
        "Get total amount of orders per user",
        "List all users who made orders after 2023-01-01",
        "Combine users and orders using join",
        "Get all orders UNION cancelled_orders"
    ]
    for q in questions:
        print(f"Question: {q} -> Intent: {classify_intent(q)}")
