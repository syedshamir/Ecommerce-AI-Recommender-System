import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")
    HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = "text-embedding-3-small"
    RAG_MODEL="llama-3.1-8b-instant"

