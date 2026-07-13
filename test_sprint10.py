from agents.router import route_question

#RAG (documents)
result1 = route_question("What is the password policy?")
print("Question:", result1["question"])
print("Source:", result1["source_used"])
print("Latency:", result1["latency_seconds"])
print("Answer:", result1["answer"])
print("=" * 50)

# SQL (database)
result2 = route_question("Which employee has the highest salary?")
print("Question:", result2["question"])
print("Source:", result2["source_used"])
print("Latency:", result2["latency_seconds"])
print("Answer:", result2["answer"])