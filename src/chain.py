from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config import (
    GROQ_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    SYSTEM_PROMPT,
)
from src.retriever import get_retriever


def get_llm():
    """Initialize the Groq LLM."""
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
    )
    return llm


def format_context(docs):
    """Format retrieved documents into a context string for the prompt."""
    context_parts = []
    for doc in docs:
        meta = doc.metadata
        context_parts.append(
            f"[Source: {meta.get('source_url', 'N/A')} | "
            f"Fund: {meta.get('fund_name', 'N/A')} | "
            f"Scraped: {meta.get('scrape_date', 'N/A')}]\n"
            f"{doc.page_content}"
        )
    return "\n\n---\n\n".join(context_parts)


def build_rag_chain():
    """Build the full RAG chain: retriever → prompt → LLM → output."""
    retriever = get_retriever()
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

    chain = (
        {
            "context": retriever | format_context,
            "question": RunnablePassthrough(),
            "scrape_date": lambda _: get_scrape_date(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def get_scrape_date():
    """Get the scrape date from the most recent ingestion."""
    # Read from any scraped file's metadata, or use a default
    import os
    scraped_dir = "./data/scraped"
    for f in os.listdir(scraped_dir):
        if f.endswith(".txt"):
            with open(os.path.join(scraped_dir, f), "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("Scrape Date:"):
                        return line.replace("Scrape Date: ", "").strip()
    return "N/A"


def ask(question: str) -> str:
    """Ask a question and get the RAG-generated answer."""
    chain = build_rag_chain()
    response = chain.invoke(question)
    return response
