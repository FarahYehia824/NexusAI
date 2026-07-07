from services.database_service import run_query
from services.llm_service import ask_llm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCHEMA_DESCRIPTION = """
You have access to a SQLite database with these tables:

Table: employees
Columns: id (integer), name (text), department (text), salary (integer)

Table: products
Columns: id (integer), product_name (text), price (integer), total_sales (integer)
"""


def generate_sql(question: str) -> str:
    
    prompt = f"""{SCHEMA_DESCRIPTION}

Given the question below, write ONLY a valid SQLite SQL query that answers it.
Do not include any explanation, markdown, or code fences. Return only the raw SQL query.

Question: {question}

SQL Query:"""

    sql = ask_llm(prompt)
    sql = sql.strip().strip("```sql").strip("```").strip()
    logger.info(f"Generated SQL: {sql}")
    return sql


def answer_from_database(question: str) -> dict:
    """
    الدالة الرئيسية: بتحول السؤال لـ SQL، تشغله، وترجع النتيجة
    """
    sql_query = generate_sql(question)
    result = run_query(sql_query)
    return {"question": question, "sql": sql_query, "result": result}