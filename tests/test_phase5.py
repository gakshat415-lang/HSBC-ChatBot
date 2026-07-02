from src.guardrails import check_guardrails, detect_pii, is_advisory_query

print("=== Phase 5: Guardrails Verification ===\n")

print("--- Gate Checks ---")
print("5.1 Guardrails module imports: Pass")
print(f"5.2 PII detection works: {'Pass' if detect_pii('PAN: ABCDE1234F') else 'Fail'}")
print(f"5.3 Advisory detection works: {'Pass' if is_advisory_query('Should I invest?') else 'Fail'}")
print(f"5.4 Factual query passes: {'Pass' if check_guardrails('What is the expense ratio of HSBC Midcap Fund?')['allowed'] else 'Fail'}\n")

print("--- PII Detection Test Suite ---")
pii_tests = [
    ("5.5", "My PAN is ABCDE1234F", True),
    ("5.6", "Aadhaar: 1234 5678 9012", True),
    ("5.7", "Call me at 9876543210", True),
    ("5.8", "Send to user@example.com", True),
    ("5.9", "Aadhaar: 123456789012", True),
    ("5.10", "+91-9876543210", True),
    ("5.11", "What is the expense ratio?", False), # valid mutual fund question
    ("5.12", "HSBC fund NAV is 245.32", False) # valid mutual fund statement
]
for tid, q, expected in pii_tests:
    res = detect_pii(q)
    print(f"Test {tid}: {q}")
    print(f"  Result: {res} | Expected: {expected} | Overall: {'Pass' if res == expected else 'Fail'}")

print("\n--- Advisory Detection Test Suite ---")
adv_tests = [
    ("5.13", "Should I invest in HSBC Midcap?", True),
    ("5.14", "Which fund is better?", True),
    ("5.15", "Can you recommend a fund?", True),
    ("5.16", "Is this fund worth it?", True)
]
for tid, q, expected in adv_tests:
    res = is_advisory_query(q)
    print(f"Test {tid}: {q}")
    print(f"  Result: {res} | Expected: {expected} | Overall: {'Pass' if res == expected else 'Fail'}")
