# 📰 TechCrunch Scraper & ChromaDB Vector Store

This Python script scrapes recent TechCrunch articles, extracts their content, generates embeddings using Hugging Face models, and stores them in a local Chroma vector database. This setup is ideal for building search, Q&A, or chatbot applications on top of real-time news data.

---

## 🚀 Features

- 🔗 Scrapes article links from [TechCrunch](https://techcrunch.com)
- 🧹 Cleans and extracts meaningful article content
- ✂️ Splits text into manageable chunks using `RecursiveCharacterTextSplitter`
- 🧠 Embeds text using Hugging Face’s `all-MiniLM-L6-v2` model
- 💾 Stores chunks and metadata in ChromaDB (`techcrunch_chroma/`)

---

## 📂 Project Structure

```
.
├── main.py                # Entry point for scraping and embedding
├── techcrunch_chroma/    # Generated ChromaDB directory (after running)
├── README.md              # You're reading it!
```

---

## 📦 Requirements

Install dependencies using `pip`:

```bash
pip install requests beautifulsoup4 langchain chromadb langchain-huggingface
```

---

## ▶️ Usage

Run the script:

```bash
python main.py
```

The script will:

1. Scrape article URLs from TechCrunch homepage
2. Download and clean up to 10 article contents
3. Split content into overlapping chunks
4. Embed chunks using Hugging Face model
5. Save results in a local ChromaDB (`techcrunch_chroma/`)

---

## 🔍 Output Example

```bash
🔍 Scraping base URL: https://techcrunch.com/
✅ Found 38 article URLs
📄 Fetched 10 valid articles
🧠 Sample vector length: 384
✂️ Total chunks: 312
✅ ChromaDB created and saved at 'techcrunch_chroma'
```

---

## 🧠 Vector Store Details

- Embeddings Model: `all-MiniLM-L6-v2`
- Vector DB: [Chroma](https://www.trychroma.com/)
- Metadata stored: Article URLs (`source`)
- Persistent path: `techcrunch_chroma/`

---

## 📌 Notes

- You can adjust the number of articles by modifying `urls[:10]` in `main.py`
- It's recommended to **add `techcrunch_chroma/` to `.gitignore`**

```gitignore
techcrunch_chroma/
```

---

## 🔧 Next Steps

You can query this vector store using:

```python
results = db.similarity_search("What is AI?", k=3)
for r in results:
    print(r.page_content, r.metadata)
```

Or build a chatbot/RAG pipeline using LangChain.

---

## ⚠️ Legal Notice

This script is for educational and non-commercial use. Always check a website’s `robots.txt` and terms of service before scraping.

---

## 📜 License

MIT License or Public Domain — feel free to adapt.
