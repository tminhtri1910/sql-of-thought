from agents.schema_linking_agent import schema_linking
from agents.intent_classifier_agent import classify_intent
from agents.query_planning_agent import generate_logical_plan
from agents.sql_generator_agent import generate_sql_from_plan
from agents.sql_execution_agent import execute_sql
from agents.error_correction_agent import correction_plan_from_runtime, apply_correction_to_sql
# from agents.correction_sql_agent import 

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
    linked_schema = schema_linking(question)
    print("\nSchema:",linked_schema)

    # Step 2: Intent Classification
    intent = classify_intent(question)
    print("Intent:",intent)

    # Step 3: Query Planning
    logical_plan = generate_logical_plan(question, linked_schema, intent)
    print("Query plan:",logical_plan)

    # Step 4: SQL Generation
    sql = "SELECT FROM WHERE;"
    # sql = generate_sql_from_plan(logical_plan)
    print("\nFirst SQL:",sql)

    iterations = 0

    while iterations < max_iterations:
        iterations += 1

        # Step 5: Execute SQL
        success, result_or_error = execute_sql(sql)
        # print(success,'\n',result_or_error)
        if success:
            return {
                "final_sql": sql,
                "result": result_or_error,
                "success": success,
                "iterations": iterations
            }

        # Step 6: Correction Plan
        correction = correction_plan_from_runtime(question, linked_schema, sql, result_or_error)
        fix_plan = correction.get("fix_plan", "")

        print(f"\nIteration {iterations} \nDetected error: {correction.get('category')}.{correction.get('error_code')}")
        print(f"Reason: {correction.get('reason')}")
        print(f"Fix plan: {fix_plan}")

        # Step 7: Apply Correction
        sql = apply_correction_to_sql(sql, fix_plan)
        print("Corrected SQL:",sql)

    # Max iterations reached without success
    return {
        "final_sql": sql,
        "result": None,
        "success": success,
        "iterations": iterations
    }

question = "Show me the users in the USA."
print("Question:", question)

result = run_full_pipeline(question)

print("\nIterations", result["iterations"])
print("Success:", result["success"])

print("\nFinal SQL:", result["final_sql"])
print("Result:", result["result"])
