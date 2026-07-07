from groq import Groq
from config.settings import GROQ_API_KEY
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)

def ask_llm(question: str) -> str:
    logger.info(f"Question received: {question}")
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    
    answer = response.choices[0].message.content
    logger.info(f"Answer generated: {answer[:100]}...")
    
    return answer