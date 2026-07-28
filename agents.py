import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from state import SMEState

load_dotenv()

groq_router = ChatOpenAI(
    model="llama-3.1-8b-instant", 
    api_key=os.getenv("GROQ_API_KEY"), 
    base_url="https://api.groq.com/openai/v1"
)

openrouter_llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct", 
    api_key=os.getenv("OPENROUTER_API_KEY"), 
    base_url="https://openrouter.ai/api/v1"
)

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vectorstore = PineconeVectorStore(index_name="sme-advisor", embedding=embeddings)

def orchestrator_router_agent(state: SMEState) -> SMEState:
    prompt = f"Categorize the intent of this Sri Lankan SME query into one word [TAX, REGISTRATION, LOANS, GENERAL]: {state['user_query']}"
    res = groq_router.invoke([("user", prompt)])
    state["intent"] = res.content.strip().upper()
    state["messages"] = [f"[Orchestrator]: Detected intent -> {state['intent']}"]
    return state

def regulation_search_agent(state: SMEState) -> SMEState:
    results = vectorstore.similarity_search(state["user_query"], k=4)
    docs_text = [f"Source: {doc.metadata.get('source', 'Doc')}\n{doc.page_content}" for doc in results]
    state["retrieved_docs"] = docs_text
    state["messages"] = [f"[RAG Agent]: Retrieved {len(docs_text)} legal clauses from Pinecone Cloud."]
    return state

def financial_suggestion_agent(state: SMEState) -> SMEState:
    context = "\n\n".join(state["retrieved_docs"])
    prompt = f"Context: {context}\nQuery: {state['user_query']}\nTask: Calculate applicable tax liabilities and provide CBSL loan advice."
    res = openrouter_llm.invoke([("user", prompt)])
    
    critique_prompt = f"Critique and refine this financial advice for compliance with Sri Lankan IRD regulations:\n{res.content}"
    refined_res = openrouter_llm.invoke([("user", critique_prompt)])
    
    state["financial_analysis"] = refined_res.content
    state["messages"] = ["[Financial Agent]: Generated and self-critiqued financial advisory."]
    return state

def report_generator_agent(state: SMEState) -> SMEState:
    prompt = f"Compile a formal Sri Lankan SME Advisory Report in Markdown using this context: {state['retrieved_docs']} and advice: {state['financial_analysis']} for query: {state['user_query']}."
    res = openrouter_llm.invoke([("user", prompt)])
    state["final_report"] = res.content
    state["messages"] = ["[Report Generator]: Final report formatted."]
    return state