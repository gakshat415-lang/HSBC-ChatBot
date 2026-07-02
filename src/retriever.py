from langchain_community.vectorstores import Chroma
from src.config import (
    CHROMA_PERSIST_DIR,
    CHROMA_COLLECTION_NAME,
    TOP_K,
    RELEVANCE_THRESHOLD,
)
from src.ingestion import get_embedding_model


def get_vectorstore():
    """Load the persisted ChromaDB vector store."""
    embeddings = get_embedding_model()
    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name=CHROMA_COLLECTION_NAME,
    )
    return vectorstore


def get_retriever():
    """Create a LangChain retriever from the vector store."""
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": TOP_K,
            "score_threshold": RELEVANCE_THRESHOLD,
        },
    )
    return retriever


def retrieve_with_scores(query, k=TOP_K):
    """Retrieve chunks with similarity scores for debugging/logging."""
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search_with_relevance_scores(query, k=k)
    return results
