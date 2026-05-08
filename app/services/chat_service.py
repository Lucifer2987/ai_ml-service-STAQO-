import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Uncomment when ready to connect real knowledge base
# from langchain_groq import ChatGroq
# from langchain.chains import RetrievalQA
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# vectordb = Chroma(persist_directory="./data/knowledge_base", embedding_function=embeddings)
# llm = ChatGroq(
#     model="llama-3.1-8b-instant",   # free, very fast
#     api_key=os.getenv("GROQ_API_KEY")
# )
# qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())

from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert retail store audit assistant. 
You help store champions (managers and staff) understand:
- Grooming and appearance standards
- In-store branding compliance requirements  
- Champion action plans and how to complete them
- Store hygiene and display guidelines

Give clear, practical, short answers. If unsure, say so honestly."""

# Simple in-memory session history (resets when server restarts)
# TODO: Replace with Redis for persistent sessions
session_history: dict[str, list] = {}

def get_chat_response(question: str, session_id: str) -> dict:
    """
    Uses Groq (free) with llama-3.1-8b-instant model to answer champion questions.
    Maintains conversation history per session.
    """
    # Initialize history for new session
    if session_id not in session_history:
        session_history[session_id] = []

    # Add user message to history
    session_history[session_id].append({
        "role": "user",
        "content": question
    })

    # Keep only last 10 messages to avoid token limits
    recent_history = session_history[session_id][-10:]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # free Groq model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *recent_history
            ],
            max_tokens=512,
            temperature=0.7,
        )

        answer = response.choices[0].message.content

        # Save assistant reply to history
        session_history[session_id].append({
            "role": "assistant",
            "content": answer
        })

        return {
            "answer": answer,
            "session_id": session_id,
            "source": "groq_llama3"
        }

    except Exception as e:
        return {
            "answer": f"Sorry, I could not process your question right now. Error: {str(e)}",
            "session_id": session_id,
            "source": "error"
        }