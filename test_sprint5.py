from agents.router import route_question

questions = [
    "How many annual leave days do employees get?",
    "What are the top 3 best selling products?",
    "What is the password policy?",
    "Which employee has the highest salary?"
]

for q in questions:
    result = route_question(q)
    print("Question:", result["question"])
    print("Source used:", result["source_used"])
    print("Answer:", result["answer"])
    print("=" * 50)