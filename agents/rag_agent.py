from services.embedding_service import search
from services.llm_service import ask_llm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def answer_from_documents(question: str) -> str:
    """
    بتدور على أقرب chunks للسؤال، وبعدين تدّيهم للـ LLM
    عشان يجاوب بشكل طبيعي بناءً عليهم
    """
    results = search(question, top_k=3)
    context = "\n\n".join([r["chunk"] for r in results])

    prompt = f"""Answer the following question based only on the information below.
If the answer is not in the text, say you don't have enough information.

Context:
{context}

Question: {question}

Answer:"""

    logger.info(f"RAG question: {question}")
    answer = ask_llm(prompt)
    logger.info("RAG answer generated")

    return answer