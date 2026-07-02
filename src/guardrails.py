import re
from src.config import (
    ADVISORY_KEYWORDS,
    ADVISORY_REFUSAL,
    OFF_TOPIC_REFUSAL,
    PII_WARNING,
)


# ─── PII Detection ─────────────────────────────────────────

PII_PATTERNS = {
    "pan": re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]"),
    "aadhaar": re.compile(r"\b[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}\b"),
    "phone": re.compile(r"(\+91[\s-]?)?[6-9][0-9]{9}\b"),
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "account": re.compile(r"\b[0-9]{10,18}\b"),
}


def detect_pii(query: str) -> bool:
    """Check if the query contains any PII patterns."""
    for pii_type, pattern in PII_PATTERNS.items():
        if pattern.search(query):
            return True
    return False


# ─── Intent Classification ─────────────────────────────────

def is_advisory_query(query: str) -> bool:
    """Check if the query seeks investment advice or opinions."""
    query_lower = query.lower().strip()
    for keyword in ADVISORY_KEYWORDS:
        if keyword in query_lower:
            return True
    return False


def is_mutual_fund_related(query: str) -> bool:
    """Check if the query is related to mutual funds."""
    mf_keywords = [
        "mutual fund", "fund", "sip", "nav", "expense ratio",
        "exit load", "aum", "hsbc", "elss", "riskometer",
        "benchmark", "scheme", "lumpsum", "groww", "midcap",
        "small cap", "multi cap", "liquid", "hybrid", "debt",
        "equity", "etf", "fof", "lock-in", "lock in",
        "minimum investment", "fund manager", "capital gains",
    ]
    query_lower = query.lower()
    return any(kw in query_lower for kw in mf_keywords)


# ─── Main Guardrail Function ───────────────────────────────

def check_guardrails(query: str, scrape_date: str = "N/A") -> dict:
    """
    Run all guardrail checks on the user query.

    Returns:
        {
            "allowed": bool,        # True if query can proceed to RAG
            "response": str | None, # Pre-built refusal response (if blocked)
            "reason": str,          # "pii" | "advisory" | "off_topic" | "ok"
        }
    """
    # Check 1: PII detection (highest priority)
    if detect_pii(query):
        return {
            "allowed": False,
            "response": PII_WARNING,
            "reason": "pii",
        }

    # Check 2: Advisory/opinion query
    if is_advisory_query(query):
        return {
            "allowed": False,
            "response": ADVISORY_REFUSAL.format(scrape_date=scrape_date),
            "reason": "advisory",
        }

    # Check 3: Off-topic (not related to mutual funds at all)
    if not is_mutual_fund_related(query):
        return {
            "allowed": False,
            "response": OFF_TOPIC_REFUSAL.format(scrape_date=scrape_date),
            "reason": "off_topic",
        }

    # All checks passed
    return {
        "allowed": True,
        "response": None,
        "reason": "ok",
    }
