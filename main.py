from bs4 import BeautifulSoup
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

def scrape_techcrunch_articles(base_url="https://techcrunch.com/"):
    print(f"🔍 Scraping base URL: {base_url}")
    response = requests.get(base_url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    article_links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith("https://techcrunch.com/") and "/20" in href:  # likely article
            article_links.add(href.split("?")[0])

    print(f"✅ Found {len(article_links)} article URLs")
    return list(article_links)

def extract_article_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove scripts/styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        # Extract content
        content = ""
        article = soup.find("article")
        if article:
            content = article.get_text(separator=' ', strip=True)
        else:
            content = soup.get_text(separator=' ', strip=True)

        return content
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return ""

if __name__ == "__main__":
    # Step 1: Scrape URLs
    urls = scrape_techcrunch_articles()
    docs = []
    for u in urls[:10]:  # limit to 10 articles
        content = extract_article_text(u)
        if content and len(content.split()) > 50:  # avoid short pages
            docs.append({"url": u, "content": content})
    print(f"📄 Fetched {len(docs)} valid articles")

    if not docs:
        print("⚠️ No articles to process, exiting.")
        exit()

    # Step 2: Text Splitting & Embedding
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    sample_vector = embedding.embed_query("TechCrunch sample check")
    print(f"🧠 Sample vector length: {len(sample_vector)}")

    chunks, metas = [], []
    for doc in docs:
        parts = splitter.split_text(doc["content"])
        chunks.extend(parts)
        metas.extend([{"source": doc["url"]}] * len(parts))

    print(f"✂️ Total chunks: {len(chunks)}")
    if not chunks:
        print("⚠️ No text chunks to embed, exiting.")
        exit()

    # Step 3: Save to ChromaDB
    db = Chroma.from_texts(
        chunks,
        embedding=embedding,
        metadatas=metas,
        persist_directory="techcrunch_chroma"
    )
    db.persist()
    print("✅ ChromaDB created and saved at 'techcrunch_chroma'")
