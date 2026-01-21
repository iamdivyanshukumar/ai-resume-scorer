from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
import uuid
from pathlib import Path

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_stores")

def get_llm():
    model = ChatOpenAI(model="gpt-3.5-turbo",temperature=0)
    return model

def load_db(db_id):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    persist_path = os.path.join(VECTOR_DB_DIR,db_id)
    if not os.path.exists(persist_path):
        raise FileNotFoundError(f"Database folder not found at: {persist_path}")
    
    return Chroma(persist_directory=persist_path, embedding_function=embeddings)


def resume_chat(db_id,query):

    vector_store = load_db(db_id)
    retriever = vector_store.as_retriever(search_kwargs={"k":3})
    llm = get_llm()
    template = """
        You are a meticulous and strict Resume Analyzer AI.

        Your task is to analyze the Candidate’s Resume (CONTEXT) strictly in relation to the user’s query (QUESTION).
        Evaluate the resume based on:
        - Skills relevance and completeness
        - Project quality, impact, and clarity
        - Education relevance
        - Grammar, spelling, and formatting
        - Missing or weak sections
        - or any information related to resume

        Do NOT make assumptions.
        ONLY answer if the requested information is clearly present in the resume or related to resume.
        If information is missing, explicitly state that it is missing.

        You MUST return your response as a VALID JSON object.
        Do NOT include any text outside the JSON.

        --------------------
        CONTEXT (Candidate Resume):
        {context}

        QUESTION (User Query):
        {question}
        --------------------

        RESPONSE RULES:

        1. If QUESTION = "rate my resume":
        - Return a score from 1 to 10
        - Clearly justify the score
        - List improvement areas under:
            - grammar_issues
            - missing_skills
            - project_strength
            - formatting_issues

        2. If QUESTION = "what are the grammatical mistakes in my resume":
        - Identify ALL grammatical and spelling mistakes
        - Provide:
            - original_text
            - corrected_text
            - explanation

        """
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = ({"context": retriever | format_docs, "question": RunnablePassthrough()}
             | prompt | llm | StrOutputParser()
            )
    return chain.invoke(query)
