from typing import Dict
from utils.openai_client import client 

def generate_sql_from_plan(logical_plan: Dict, model: str = "gpt-4.1-mini") -> str:
    """
    Use LLM to convert logical plan to SQL string.
    """
    prompt = f"""
You are an expert SQL assistant.

Logical plan (JSON): {logical_plan}

Task: Convert this logical plan into a valid SQL query.
Return ONLY the SQL query.
Do NOT include code fences such as ```sql.
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    sql = response.choices[0].message.content.strip()
    return sql
