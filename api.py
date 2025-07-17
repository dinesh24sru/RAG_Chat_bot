from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Connect to existing ChromaDB or create new
vectorstore = Chroma(
    embedding_function=embedding,
    persist_directory="techcrunch_chroma"
)

# Initialize Retriever
retriever = vectorstore.as_retriever()

# Initialize LLM (Ollama)
llm = OllamaLLM(model="llama3")

# Set up RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

# Define request body model
class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    response = qa_chain.invoke(query.question)
    return {"answer": response}
