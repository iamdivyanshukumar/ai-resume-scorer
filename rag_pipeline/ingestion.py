from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import uuid
from pathlib import Path

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_stores")

def model_embed():
    model_embed = OpenAIEmbeddings(model="text-embedding-3-small")
    return model_embed

def get_db_path(db_id:str):
    return os.path.join(VECTOR_DB_DIR,db_id)

def prepared_data(file_path:str):

    # 1. Create unique ID and persistent path
    db_id = str(uuid.uuid4())
    persist_path = get_db_path(db_id)
    os.makedirs(persist_path, exist_ok=True)

    loader = PyPDFLoader(file_path=file_path)
    doc = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500 , chunk_overlap = 100)
    text_chunk = splitter.split_documents(documents=doc)
    embedding_model = model_embed()
    vector_store = Chroma.from_documents(
        documents=text_chunk,
        embedding=embedding_model,
        persist_directory=get_db_path(db_id=db_id)
    )

    return db_id