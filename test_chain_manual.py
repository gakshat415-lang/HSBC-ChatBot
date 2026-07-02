from src.chain import ask

print("Testing RAG Chain with Groq...\n")

# Factual query
query1 = "What is the expense ratio of HSBC Midcap Fund?"
print(f"Q: {query1}")
print(ask(query1))
print("\n" + "="*50 + "\n")

# Should still answer (but we haven't built guardrails yet)
query2 = "What is the exit load for HSBC Small Cap Fund?"
print(f"Q: {query2}")
print(ask(query2))
