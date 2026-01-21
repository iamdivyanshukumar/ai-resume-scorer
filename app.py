import os
import shutil
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from rag_pipeline.ingestion import prepared_data
from rag_pipeline.generation_chain import resume_chat

app = FastAPI()

# Create a temporary folder to save uploaded files before processing
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "AI Resume Scorer API is running!"}

# --- ENDPOINT 1: Upload & Ingest ---
@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        # 1. Save the file locally so PyPDFLoader can read it
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Call your ingestion logic (from ingestion.py)
        # This returns the unique DB_ID
        db_id = prepared_data(file_path)

        # 3. Clean up (delete the temp file)
        os.remove(file_path)

        return {
            "message": "File processed successfully",
            "filename": file.filename,
            "db_id": db_id  # <--- CRITICAL: Frontend needs this ID
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- ENDPOINT 2: Chat & Analysis ---
@app.post("/analyze")
async def analyze_resume(
    db_id: str = Form(...), 
    query: str = Form(...)
):
    try:
        # Call your generation logic (from generation.py)
        # This returns the JSON string from the LLM
        response = resume_chat(db_id, query)
        
        return {"response": response}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Database ID not found. Please upload the resume first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)