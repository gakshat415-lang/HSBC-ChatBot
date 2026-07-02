# Project Context: Mutual Fund FAQ Assistant (Facts-Only Q&A)

---

## 1. Overview

The objective of this project is to build a **facts-only FAQ assistant** for mutual fund schemes, using **Groww** as the reference product context. The assistant will answer objective, verifiable queries related to mutual funds by retrieving information **exclusively from official public sources**, such as AMC (Asset Management Company) websites, AMFI, and SEBI.

The system must **strictly avoid** providing investment advice, opinions, or recommendations. Every response must include a single, clear source link and adhere to defined constraints around clarity, accuracy, and compliance.

> **Key Principle**: The system prioritizes **accuracy over intelligence** — it is a retrieval tool, not a financial advisor.

---

## 2. Technical Approach

The assistant is designed as a lightweight **Retrieval-Augmented Generation (RAG)** system that:

1. **Answers factual queries** about mutual fund schemes.
2. **Uses a curated corpus** of official documents scraped from Groww fund pages.
3. **Provides concise, source-backed responses** grounded only in the retrieved content.

### RAG Pipeline (High-Level)

```
User Query → Query Understanding → Retrieval (Vector Search over Corpus) → LLM Generation (Grounded Answer) → Response with Citation
```

- **Retrieval**: Searches a vector store of chunked, embedded documents from the corpus URLs.
- **Generation**: An LLM synthesizes a concise answer strictly from retrieved chunks, appending the source citation and last-updated footer.
- **Guardrails**: A classification layer detects advisory/opinion-seeking queries and triggers a polite refusal instead of a generated answer.

---

## 3. Target Users

| User Segment | Use Case |
|---|---|
| **Retail investors** | Comparing mutual fund schemes — expense ratios, exit loads, SIP minimums, risk levels, etc. |
| **Customer support / content teams** | Handling repetitive, factual mutual fund queries at scale. |

---

## 4. Corpus Definition

The knowledge base is built from the following **12 HSBC mutual fund scheme pages** on Groww. These are the **only** authoritative data sources for the assistant.

| # | Fund Name | Source URL |
|---|---|---|
| 1 | HSBC Midcap Fund Direct Growth | https://groww.in/mutual-funds/hsbc-midcap-fund-direct-growth |
| 2 | HSBC Multi Cap Fund Direct Growth | https://groww.in/mutual-funds/hsbc-multi-cap-fund-direct-growth |
| 3 | HSBC Small Cap Fund Direct Growth | https://groww.in/mutual-funds/hsbc-small-cap-fund-direct-growth |
| 4 | HSBC India Opportunities Fund Direct Growth | https://groww.in/mutual-funds/hsbc-india-opportunities-fund-direct-growth |
| 5 | HSBC Credit Risk Fund Direct Growth | https://groww.in/mutual-funds/hsbc-credit-risk-fund-direct-growth |
| 6 | HSBC Focused Fund Direct Growth | https://groww.in/mutual-funds/hsbc-focused-fund-direct-growth |
| 7 | HSBC Consumption Fund Direct Growth | https://groww.in/mutual-funds/hsbc-consumption-fund-direct-growth |
| 8 | HSBC Gold ETF FOF Direct Growth | https://groww.in/mutual-funds/hsbc-gold-etf-fof-direct-growth |
| 9 | HSBC ELSS Fund Direct Growth | https://groww.in/mutual-funds/hsbc-elss-fund-direct-growth |
| 10 | HSBC Infrastructure Fund Direct Growth | https://groww.in/mutual-funds/hsbc-infrastructure-fund-direct-growth |
| 11 | HSBC Equity Hybrid Fund Direct Growth | https://groww.in/mutual-funds/hsbc-equity-hybrid-fund-direct-growth |
| 12 | HSBC Liquid Fund Direct Growth | https://groww.in/mutual-funds/hsbc-liquid-fund-direct-growth |

> All 12 schemes belong to a single AMC: **HSBC Mutual Fund**.

---

## 5. FAQ Assistant — Functional Requirements

### 5.1 Supported Query Types (Facts-Only)

The assistant must answer objective, verifiable questions such as:

| Query Category | Example Questions |
|---|---|
| **Expense Ratio** | "What is the expense ratio of HSBC Small Cap Fund?" |
| **Exit Load** | "What is the exit load for HSBC Midcap Fund?" |
| **Minimum SIP Amount** | "What is the minimum SIP amount for HSBC ELSS Fund?" |
| **Lock-in Period** | "What is the lock-in period for HSBC ELSS Fund?" |
| **Riskometer Classification** | "What is the risk level of HSBC Liquid Fund?" |
| **Benchmark Index** | "What is the benchmark index for HSBC Multi Cap Fund?" |
| **Procedural / How-to** | "How do I download my capital gains report?" |

### 5.2 Response Format Rules

Every valid response **must** follow these rules:

1. **Maximum 3 sentences** — keep it concise and scannable.
2. **Exactly one citation link** — the source URL from the corpus.
3. **Footer line**: `"Last updated from sources: <date>"` — where `<date>` is the date the corpus was last scraped/refreshed.

#### Example Response

> The expense ratio of HSBC Small Cap Fund Direct Growth is 0.65% (as of June 2026). This is a direct plan expense ratio and may differ from the regular plan.
>
> Source: https://groww.in/mutual-funds/hsbc-small-cap-fund-direct-growth
>
> *Last updated from sources: 2026-07-01*

---

## 6. Refusal Handling

### 6.1 When to Refuse

The assistant **must refuse** any query that is:

- Asking for **investment advice** — e.g., "Should I invest in this fund?"
- Requesting **comparisons or opinions** — e.g., "Which fund is better?"
- Asking for **return predictions or calculations** — e.g., "How much will I earn if I invest ₹10,000?"

### 6.2 Refusal Response Rules

Refusal responses must:

1. Be **polite and clearly worded**.
2. **Reinforce** the facts-only limitation of the assistant.
3. Provide a **relevant educational link** (e.g., an AMFI or SEBI resource page).

#### Example Refusal

> I'm a facts-only assistant and cannot provide investment advice or fund comparisons. For guidance on choosing mutual funds, you can visit the AMFI investor education page: https://www.amfiindia.com/investor-corner/knowledge-center.html
>
> *Last updated from sources: 2026-07-01*

---

## 7. User Interface Specification

The UI should be **minimal and clean**, consisting of:

| UI Element | Details |
|---|---|
| **Welcome Message** | A brief greeting explaining what the assistant can do. |
| **Example Questions** | Display **3 clickable example questions** to guide new users (e.g., "What is the expense ratio of HSBC Midcap Fund?"). |
| **Disclaimer Banner** | Prominently displayed: **"Facts-only. No investment advice."** |
| **Chat Input** | A text input field for user queries. |
| **Response Area** | Displays the assistant's answer with citation and footer. |

---

## 8. Constraints

### 8.1 Data and Sources

- Use **only official public sources** — the 12 Groww URLs listed in the corpus above.
- No scraping of unofficial blogs, forums, or third-party aggregator sites.

### 8.2 Privacy and Security

The system must **never** collect, store, or process any of the following:

| Prohibited Data | Examples |
|---|---|
| Government IDs | PAN numbers, Aadhaar numbers |
| Financial Identifiers | Bank account numbers, folio numbers |
| Authentication Tokens | OTPs, passwords |
| Contact Information | Email addresses, phone numbers |

### 8.3 Content Restrictions

| Rule | Description |
|---|---|
| No investment advice | Never recommend buying, selling, or holding any fund. |
| No performance comparisons | Never compare returns across funds or time periods. |
| No return calculations | Never project or calculate future/past returns. |
| Performance queries → factsheet link | If a user asks about performance, respond with a link to the official factsheet only. |

### 8.4 Transparency

- Responses must be **short, factual, and verifiable**.
- Every answer must include a **source link** and a **last updated date**.

---

## 9. Expected Deliverables

| Deliverable | Details |
|---|---|
| **README Document** | Setup instructions, selected AMC and schemes, architecture overview (RAG approach), known limitations. |
| **Working Assistant** | A functional RAG-based chatbot meeting all requirements above. |
| **Disclaimer Snippet** | Embedded in the UI: `"Facts-only. No investment advice."` |

---

## 10. Success Criteria

The project will be considered successful if it meets **all** of the following:

| # | Criterion | Description |
|---|---|---|
| 1 | **Accurate Retrieval** | Correctly retrieves factual mutual fund information from the corpus. |
| 2 | **Facts-Only Adherence** | Never generates opinions, advice, or speculative content. |
| 3 | **Source Citations** | Every response includes a valid, relevant source link. |
| 4 | **Refusal of Advisory Queries** | Properly refuses non-factual queries with a polite, educational response. |
| 5 | **Clean UI** | Minimal, user-friendly interface with disclaimer, examples, and chat. |

---

## 11. Summary

The goal is to build a **trustworthy, transparent, and compliant** mutual fund FAQ assistant that prioritizes **accuracy over intelligence**. The system should ensure that users receive only **verified, source-backed financial information**, without any advisory bias or speculative content.

> *Source: [Problemstatement.txt](file:///c:/Chatbot%20FAQ%20Final/Docs/Problemstatement.txt)*
