from agents.schema_linking_agent import schema_linking
from agents.intent_classifier_agent import classify_intent
from agents.query_planning_agent import generate_logical_plan
from agents.sql_generator_agent import generate_sql_from_plan
from agents.sql_execution_agent import execute_sql
from agents.error_correction_agent import correction_plan_from_runtime, apply_correction_to_sql
# from agents.correction_sql_agent import 
from pprint import pprint


model_name = "gpt-5-nano"
def run_full_pipeline(question: str, max_iterations: int = 5):
    """
    Full SQL pipeline with reasoning and correction loop.

    Returns:
    {
        "final_sql": str,
        "result": list[dict] | None,
        "success": bool,
        "iterations": int
    }
    """

    # Step 1: Schema Linking
    linked_schema = schema_linking(question, model_name)
    print("\nSchema:",linked_schema)

    # Step 2: Subproblems Classification
    sub_problems = classify_intent(question, linked_schema, model_name)
    print("\nSubproblems:",sub_problems)

    # Step 3: Query Planning
    logical_plan = generate_logical_plan(question, linked_schema, sub_problems, model_name)
    print("\nQuery plan:", logical_plan, sep="\n")

    # Step 4: SQL Generation
    first_sql = sql = "SELECT FROM orders country = 'Vietnam';"
    # sql = generate_sql_from_plan(logical_plan, model_name)
    print(f'\nFirst SQL: "{first_sql}"')

    iterations = 0
    
    correction_loop = {}
    while iterations < max_iterations:
        iterations += 1

        # Step 5: Execute SQL
        result = execute_sql(sql)
        # print(result)

        # if success == False:

        success = result.get('success')
        error_message = result.get('error')
        
        # Step 6: Correction Plan        
        correction = correction_plan_from_runtime(question, linked_schema, sql, error_message, model_name)

        category = correction.get("category", "")
        error_code = correction.get("error_code", "")
        reason = correction.get("reason", "")
        fix_plan = correction.get("fix_plan", "")

        correction_loop[f'{iterations}'] = {}
    
        correction_loop[f'{iterations}']['error_message'] = error_message
        correction_loop[f'{iterations}']['category'] = category
        correction_loop[f'{iterations}']['error_code'] = error_code
        correction_loop[f'{iterations}']['reason'] = reason
        correction_loop[f'{iterations}']['fix_plan'] = fix_plan

        if success:
            if correction.get('error_code') == None:
                return {
                    "schema": linked_schema,
                    "subproblems": sub_problems,
                    "query_plan": logical_plan,
                    "initial_sql": first_sql,
                    "correction_loop": correction_loop,
                    "final_sql": sql,
                    "result": result,
                    "success": success,
                    "iterations": iterations
                }

        # fix_plan = correction.get("fix_plan", "")

        print(f"\n----Iteration {iterations}----")
        print(f'Error message: "{error_message}"')
        print(f"Classified error: {category}.{error_code}")
        print(f"Reason: {reason}")
        print(f"Fix plan: {fix_plan}")

        # Step 7: Apply Correction
        sql = apply_correction_to_sql(sql, fix_plan, model_name)
        print("Corrected SQL:",sql)
        correction_loop[f'{iterations}']['corrected_sql'] = sql

    # Max iterations reached without success
    return {
        "schema": linked_schema,
        "subproblems": sub_problems,
        "query_plan":logical_plan,
        "initial_sql": first_sql,
        "correction_loop": correction_loop,
        "final_sql": sql,
        "result": None,
        "success": success,
        "iterations": iterations
    }

if __name__ == "__main__":
    question = "Show me users in the USA."
    print("Question:", question)

    result = run_full_pipeline(question)

    print("\nCorrection loop:") 
    pprint(result["correction_loop"])
    print("\nIterations", result["iterations"])
    print("Success:", result["success"])

    print(f'\nFinal SQL: "{result["final_sql"]}"')
    print("Result:", result["result"])
