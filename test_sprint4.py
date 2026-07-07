from services.database_service import create_tables_and_seed_data
from agents.sql_agent import answer_from_database

create_tables_and_seed_data()

result = answer_from_database("What are the top 3 best selling products?")
print("Question:", result["question"])
print("SQL:", result["sql"])
print("Result:", result["result"])