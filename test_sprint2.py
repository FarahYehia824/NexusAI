from services.llm_service import ask_llm

question = "إيه هي عاصمة مصر؟"
answer = ask_llm(question)
print("السؤال:", question)
print("الرد:", answer)