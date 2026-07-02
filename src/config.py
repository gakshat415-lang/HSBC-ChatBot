"""Centralized configuration for the Mutual Fund FAQ Assistant."""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── API Keys ───────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ─── LLM Configuration ─────────────────────────────────────
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.1  # Low temperature for factual accuracy
LLM_MAX_TOKENS = 300

# ─── Embedding Model ───────────────────────────────────────
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIMENSIONS = 384

# ─── ChromaDB ──────────────────────────────────────────────
CHROMA_PERSIST_DIR = "./chroma_db"
CHROMA_COLLECTION_NAME = "mutual_fund_faq"

# ─── Retrieval ─────────────────────────────────────────────
TOP_K = 3
RELEVANCE_THRESHOLD = 0.5  # Cosine similarity

# ─── Text Chunking ─────────────────────────────────────────
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
CHUNK_SEPARATORS = ["\n\n", "\n", ". ", " "]

# ─── Corpus URLs ───────────────────────────────────────────
FUND_URLS = [
    "https://groww.in/mutual-funds/hsbc-midcap-fund-direct-growth",
    "https://groww.in/mutual-funds/hsbc-multi-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/hsbc-small-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/hsbc-india-opportunities-fund-direct-growth",
    "https://groww.in/mutual-funds/hsbc-credit-risk-fund-direct-growth",
    "https://groww.in/mutual-funds/hsbc-focused-fund-direct-growth",
    "https://groww.in/mutual-funds/hsbc-consumption-fund-direct-growth",
    "https://groww.in/mutual-funds/hsbc-gold-etf-fof-direct-growth",
    "https://groww.in/mutual-funds/hsbc-elss-fund-direct-growth",
    "https://groww.in/mutual-funds/hsbc-infrastructure-fund-direct-growth",
    "https://groww.in/mutual-funds/hsbc-equity-hybrid-fund-direct-growth",
    "https://groww.in/mutual-funds/hsbc-liquid-fund-direct-growth",
]

# ─── Scraped Data Cache ───────────────────────────────────
SCRAPED_DATA_DIR = "./data/scraped"

# ─── Guardrails — Advisory Keywords ───────────────────────
ADVISORY_KEYWORDS = [
    "should i", "recommend", "better", "best", "worth it",
    "suggest", "advice", "opinion", "which fund", "compare",
    "invest in", "buy", "sell", "hold", "good fund", "bad fund",
    "profitable", "returns will", "predict", "forecast",
]

# ─── System Prompt ─────────────────────────────────────────
SYSTEM_PROMPT = """You are a facts-only mutual fund FAQ assistant. You answer questions using ONLY the provided context. Follow these rules strictly:

1. Answer in a maximum of 3 sentences.
2. Include exactly ONE source citation link from the context metadata.
3. End every response with: "Last updated from sources: {scrape_date}"
4. NEVER provide investment advice, opinions, or recommendations.
5. NEVER compare funds or calculate returns.
6. If the context does not contain the answer, say: "I don't have this information in my current sources."
7. For performance-related queries, provide only the official factsheet link.
8. Be concise, accurate, and professional.

CONTEXT:
{context}

USER QUESTION:
{question}"""

# ─── Refusal Templates ─────────────────────────────────────
ADVISORY_REFUSAL = (
    "I'm a facts-only assistant and cannot provide investment advice, "
    "opinions, or fund comparisons. For guidance on choosing mutual funds, "
    "you can visit the AMFI investor education page: "
    "https://www.amfiindia.com/investor-corner/knowledge-center.html\n\n"
    "*Last updated from sources: {scrape_date}*"
)

OFF_TOPIC_REFUSAL = (
    "I can only answer factual questions about HSBC mutual fund schemes "
    "available on Groww. Please ask about expense ratios, exit loads, "
    "SIP amounts, risk levels, or other fund details.\n\n"
    "*Last updated from sources: {scrape_date}*"
)

PII_WARNING = (
    "⚠️ Please do not share personal information such as PAN, Aadhaar, "
    "account numbers, phone numbers, or email addresses. "
    "I do not collect or process personal data."
)

NO_RESULTS_RESPONSE = (
    "I don't have information on this topic in my current sources. "
    "Please try rephrasing your question or ask about a specific "
    "HSBC mutual fund scheme.\n\n"
    "*Last updated from sources: {scrape_date}*"
)
