# 🏦 HSBC Mutual Fund FAQ Assistant

A sophisticated Retrieval-Augmented Generation (RAG) chatbot designed to answer facts-only questions about HSBC mutual fund schemes listed on Groww. Built entirely on a **zero-cost** stack, this assistant retrieves verified data, provides source citations, and strictly refuses to give financial advice.

---

## ✨ Key Features
- **Facts-Only Responses**: Powered by a heavily constrained System Prompt that forces the LLM to only use the retrieved context.
- **Compliance Guardrails**: Custom regex and LLM-based intent classifiers that automatically block PII, advisory questions, and off-topic queries.
- **Automated Daily Ingestion**: A built-in GitHub Actions workflow runs every midnight to scrape Groww URLs, embed the new data, and push the updated ChromaDB back to the repo.
- **Local Embeddings**: Uses the highly efficient `BAAI/bge-small-en-v1.5` model entirely locally, preventing any data leakage and saving API costs.
- **Modern UI**: A sleek 1:3 layout Streamlit interface featuring active-state chat histories and distinct amber warning banners for blocked queries.

---

## 🛠️ Architecture Stack
| Component | Technology | Cost |
|---|---|---|
| **Web UI** | [Streamlit](https://streamlit.io/) | Free |
| **Orchestration** | [LangChain](https://www.langchain.com/) | Free |
| **Vector DB** | [ChromaDB](https://www.trychroma.com/) (Persistent) | Free |
| **LLM Inference** | [Groq API](https://groq.com/) (`llama-3.3-70b-versatile`) | Free Tier |
| **Embeddings** | [HuggingFace](https://huggingface.co/) (`BAAI/bge-small-en-v1.5`) | Free (Local) |
| **Data Scraping** | BeautifulSoup4 + Requests | Free |
| **Automation** | GitHub Actions Scheduler | Free |

---

## 🚀 Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/mutual-fund-faq-assistant.git
cd mutual-fund-faq-assistant
```

### 2. Set up the Environment
Ensure you have Python 3.10+ installed.
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Set your Groq API Key
Copy the example environment file and add your key:
```bash
cp .env.example .env
# Edit .env and paste your Groq API Key
```

### 4. Run the Streamlit UI
Because the `chroma_db` is included in the repository, you do not need to scrape the data yourself. Just run the app!
```bash
streamlit run app.py
```
The UI will be available at `http://localhost:8501`.

---

## ☁️ Deployment (Streamlit Community Cloud)
This repository is designed to be instantly deployable on Streamlit Community Cloud:
1. Connect this GitHub repository to [share.streamlit.io](https://share.streamlit.io).
2. Set the main file path to `app.py`.
3. In the Advanced Settings, add your `GROQ_API_KEY` to the **Secrets** section.
4. Deploy! The GitHub action will automatically keep your database fresh every day.
