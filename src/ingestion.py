import os
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import (
    CHUNK_SIZE, CHUNK_OVERLAP, CHUNK_SEPARATORS,
    EMBEDDING_MODEL, CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME
)

def load_scraped_documents(scraped_dir="./data/scraped"):
    """Load all scraped text files and extract metadata."""
    documents = []

    for filename in sorted(os.listdir(scraped_dir)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(scraped_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract metadata from first 3 lines
        lines = content.split("\n")
        fund_name = lines[0].replace("Fund Name: ", "").strip()
        source_url = lines[1].replace("Source URL: ", "").strip()
        scrape_date = lines[2].replace("Scrape Date: ", "").strip()

        documents.append({
            "content": content,
            "metadata": {
                "fund_name": fund_name,
                "source_url": source_url,
                "scrape_date": scrape_date,
                "filename": filename,
            }
        })

    print(f"Loaded {len(documents)} documents")
    return documents

def chunk_documents(documents):
    """Split documents into chunks, preserving metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=CHUNK_SEPARATORS,
        length_function=len,
    )

    all_chunks = []
    for doc in documents:
        chunks = splitter.split_text(doc["content"])
        for i, chunk_text in enumerate(chunks):
            all_chunks.append({
                "text": chunk_text,
                "metadata": {
                    **doc["metadata"],
                    "chunk_id": f"{doc['metadata']['filename']}_{i}",
                }
            })

    print(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
    return all_chunks

def get_embedding_model():
    """Initialize BAAI/bge-small-en-v1.5 embedding model (runs locally)."""
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}

    embeddings = HuggingFaceBgeEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
        query_instruction="Represent this sentence for searching relevant passages: ",
    )

    print(f"Embedding model loaded: {EMBEDDING_MODEL}")
    return embeddings

def create_vector_store(chunks, embeddings):
    """Embed all chunks and store in ChromaDB (persistent)."""
    texts = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=CHROMA_PERSIST_DIR,
        collection_name=CHROMA_COLLECTION_NAME,
    )

    print(f"Stored {len(texts)} chunks in ChromaDB at {CHROMA_PERSIST_DIR}")
    return vectorstore

def run_ingestion():
    """Full ingestion pipeline: load → chunk → embed → store."""
    print("=" * 50)
    print("Starting Data Ingestion Pipeline")
    print("=" * 50)

    # Step 1: Load
    documents = load_scraped_documents()

    # Step 2: Chunk
    chunks = chunk_documents(documents)

    # Step 3: Embedding model
    embeddings = get_embedding_model()

    # Step 4: Store
    vectorstore = create_vector_store(chunks, embeddings)

    print("\n✅ Ingestion complete!")
    return vectorstore

if __name__ == "__main__":
    run_ingestion()
