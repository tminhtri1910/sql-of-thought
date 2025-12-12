from utils.openai_client import client 

def classify_intent(question: str, model: str = "gpt-4.1-mini") -> str:
    """
    Use LLM to classify a natural language question into a basic SQL intent:
    select, aggregation, join, filter, set_operation
    """
    prompt = f"""
You are an expert SQL assistant.

Question: "{question}"

Task: Classify this question into one of the following intents:
select, aggregation, join, filter, set_operation
Only return the intent as a single word.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    intent = response.choices[0].message.content.strip().lower()
    valid_intents = ["select", "aggregation", "join", "filter", "set_operation"]
    if intent not in valid_intents:
        intent = "select"
    return intent

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
