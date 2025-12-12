import json
from typing import Dict, Any
from utils.openai_client import client

# Load taxonomy once
with open("config/error_taxonomy.json", "r") as f:
    ERROR_TAXONOMY = json.load(f)

def correction_plan_from_runtime(question:str, linked_schema: Dict[str, Any], sql: str, error_message: str, model: str = "gpt-4.1-mini") -> dict:
    """
    Combines:
    1) Runtime error classification (category + error_code)
    2) Generates a correction plan (reason + fix_plan)
    
    Returns:
    {
      "category": str | None,
      "error_code": str | None,
      "reason": str,
      "fix_plan": str
    }
    """
    taxonomy_str = json.dumps(ERROR_TAXONOMY, indent=2)

    prompt = f"""
You are an expert SQL debugging assistant.

Question:
{question}

Linked schema: 
{linked_schema}

SQL Query:
{sql}

Database Runtime Error:
{error_message}

Error Taxonomy (JSON):
{taxonomy_str}

You must identify and correct only ONE error in the given SQL.

TASK:
1. Detect the single most relevant error and label it with its taxonomy category.
2. Explain in 1–2 sentences why this error makes the SQL incorrect.
3. Provide a short, high-level plan to fix only this one error (do not fix anything else).

Return ONLY JSON like this:
{{
  "category": "<category_name or null>",
  "error_code": "<error_code or null>",
  "reason": "<reason explaining the error>",
  "fix_plan": "<short high-level plan to fix the SQL>"
}}
Do NOT include code fences such as ```json.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text = response.choices[0].message.content.strip()

    try:
        data = json.loads(text)
        # ensure all keys exist
        return {
            "category": data.get("category"),
            "error_code": data.get("error_code"),
            "reason": data.get("reason", ""),
            "fix_plan": data.get("fix_plan", "")
        }
    except:
        return {
            "category": None,
            "error_code": None,
            "reason": "LLM failed to produce a valid plan.",
            "fix_plan": ""
        }


def apply_correction_to_sql(sql: str, fix_plan: str, model: str = "gpt-4.1-mini") -> str:
    """
    Applies a fix plan to the current SQL query using LLM.

    Inputs:
        sql: str           - Current SQL query
        fix_plan: str      - High-level instruction to fix the SQL
        model: str         - LLM model to use

    Returns:
        corrected_sql: str - Modified SQL query
    """

    prompt = f"""
You are an expert SQL assistant.

Current SQL:
{sql}

Instruction to fix the SQL:
{fix_plan}

TASK:
1. Apply the fix plan exactly to the SQL and modify ONLY the parts explicitly mentioned in {fix_plan}. 
2. Do NOT remove, reorder, or alter any other clauses or content of the original SQL.
3. Preserve all structure, formatting, tables, columns, joins, filters, and logic not referenced in {fix_plan}.
4. Return ONLY the corrected SQL query without any extra text or explanation.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    corrected_sql = response.choices[0].message.content.strip()

    # Optional: fallback to original SQL if LLM fails
    if not corrected_sql:
        corrected_sql = sql

    return corrected_sql

