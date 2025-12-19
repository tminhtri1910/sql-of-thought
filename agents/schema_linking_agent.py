import json
from typing import Dict, List, Any
from utils.openai_client import client 

# Load schema
with open("config/schema.json", "r") as f:
    SCHEMA: Dict[str, Dict[str, str]] = json.load(f)

def schema_linking(question: str, model: str) -> Dict[str, Any]:
    schema_str = json.dumps(SCHEMA, indent=2)
    prompt = f"""
You are an expert SQL assistant.

Schema:
{schema_str}

Question: "{question}"

Task: Identify which tables and columns are relevant to answer this question.
Return output as a JSON object like:
{{
  "tables": '{'"table_name": ["column1", "column2"]'}',
  "foreign_keys": ['{'"from": "table1.fk_column", "to": "table2.pk_column"'}'],
  "reasoning": "<Explain in 1–2 sentences why these tables and columns are needed>"
}}

Do NOT include code fences such as ```json.
Only include relevant columns.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        # temperature=0
    )

    text_output = response.choices[0].message.content.strip()

    try:
        linked_schema = json.loads(text_output)
    except json.JSONDecodeError:
        print("Schema error")
        linked_schema = {t: list(cols.keys()) for t, cols in SCHEMA.items()}

    return linked_schema

# Example usage
if __name__ == "__main__":
    q = "Get the total amount of orders per user after 2023-01-01"
    print(schema_linking(q))
