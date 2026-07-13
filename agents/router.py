from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from services.llm_service import ask_llm
from agents.rag_agent import answer_from_documents
from agents.sql_agent import answer_from_database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    question: str
    decision: Optional[str]
    raw_result: Optional[str]
    final_answer: Optional[str]


def router_node(state: AgentState) -> AgentState:
   
    prompt = f"""You are a routing classifier. Decide whether the question below should be answered using:
- "documents" (company policies like HR, IT, Leave policies - text-based information)
- "database" (structured data about employees, salaries, products, sales, numbers)

Reply with ONLY one word: documents or database.

Question: {state['question']}

Answer:"""

    decision = ask_llm(prompt).strip().lower()
    decision = "database" if "database" in decision else "documents"

    logger.info(f"[Router Node] Decision: {decision}")
    state["decision"] = decision
    return state


def sql_node(state: AgentState) -> AgentState:
   
    result = answer_from_database(state["question"])
    logger.info(f"[SQL Node] Raw result: {result['result']}")
    state["raw_result"] = str(result["result"])
    return state


def rag_node(state: AgentState) -> AgentState:
    
    result = answer_from_documents(state["question"])
    logger.info(f"[RAG Node] Raw result: {result}")
    state["raw_result"] = result
    return state


def response_generator_node(state: AgentState) -> AgentState:
    prompt = f"""Based on the following raw result, write a clear, natural, well-formatted answer to the user's question.

Question: {state['question']}
Raw Result: {state['raw_result']}

Final Answer:"""

    final_answer = ask_llm(prompt)
    
    is_grounded = state['raw_result'] is not None and len(str(state['raw_result']).strip()) > 0
    
    logger.info(f"[Response Generator Node] Final answer generated | Grounded: {is_grounded}")
    state["final_answer"] = final_answer
    return state

def decide_next_node(state: AgentState) -> str:
   
    return state["decision"]


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("sql_agent", sql_node)
    graph.add_node("rag_agent", rag_node)
    graph.add_node("response_generator", response_generator_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        decide_next_node,
        {
            "database": "sql_agent",
            "documents": "rag_agent"
        }
    )

    graph.add_edge("sql_agent", "response_generator")
    graph.add_edge("rag_agent", "response_generator")
    graph.add_edge("response_generator", END)

    return graph.compile()


compiled_graph = build_graph()

import time

def route_question(question: str) -> dict:
    
    start_time = time.time()

    initial_state: AgentState = {
        "question": question,
        "decision": None,
        "raw_result": None,
        "final_answer": None
    }

    result = compiled_graph.invoke(initial_state)

    latency = round(time.time() - start_time, 2)
    logger.info(f"[Evaluation] Latency: {latency}s | Source: {result['decision']}")

    return {
        "question": result["question"],
        "source_used": result["decision"],
        "answer": result["final_answer"],
        "latency_seconds": latency
    }