# AI Resume Scorer

A web-based application that leverages artificial intelligence to analyze, score, and provide detailed feedback on resumes. The system uses Retrieval-Augmented Generation (RAG) to understand resume content and compare it against job requirements or general quality metrics.

## Overview

This project combines modern AI techniques with a user-friendly interface to help job seekers and recruiters evaluate resumes effectively. By processing PDF resumes and storing them in a vector database, the application can answer complex queries about resume quality, identify grammatical issues, and assess skills alignment.

## How It Works

The application follows a three-stage pipeline:

### Stage 1: Resume Ingestion
When you upload a resume, the system:
- Reads the PDF file using LangChain's PDF loader
- Breaks down the content into manageable chunks (500 characters with 100-character overlap)
- Converts each chunk into a numerical embedding using OpenAI's embedding model
- Stores these embeddings in a local Chroma vector database for fast retrieval

### Stage 2: Query Processing
When you submit a question or job description:
- The system retrieves the most relevant resume sections using vector similarity search
- These sections are combined with your query into a structured prompt
- The prompt is sent to GPT-3.5-turbo for intelligent analysis

### Stage 3: Response Generation
The AI model analyzes the resume in context and returns:
- Structured JSON responses with specific recommendations
- Numerical scores with detailed justifications
- Lists of grammatical issues with corrections
- Identified strengths and areas for improvement

## Architecture

The project is built with a frontend-backend separation:

```
Streamlit Frontend (Web UI)
        |
        | HTTP Requests
        |
    FastAPI Backend
        |
    ----+----
    |       |
Ingestion  Generation
Pipeline   Chain
    |       |
    +---+---+
        |
   Chroma Vector DB
   + OpenAI API
```

## Project Structure

```
ai-resume-scorer/
├── app.py                          # FastAPI backend server
├── frontend.py                     # Streamlit user interface
├── config.py                       # Configuration file (currently empty)
├── requirements.txt                # Python dependencies
├── rag_pipeline/                   # RAG implementation
│   ├── __init__.py
│   ├── ingestion.py               # Document ingestion logic
│   └── generation_chain.py         # LLM chain for analysis
├── vector_stores/                  # Persistent storage for embeddings
└── temp_uploads/                   # Temporary file storage during processing
```

## Installation

### Prerequisites
- Python 3.9 or higher
- An OpenAI API key
- pip or conda for package management

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/iamdivyanshukumar/ai-resume-scorer.git
cd ai-resume-scorer
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
Create a `.env` file in the project root with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application

The application consists of two components that need to run simultaneously:

### Start the Backend Server
```bash
python app.py
```
The FastAPI server will start on `http://127.0.0.1:8000`

### Start the Frontend (in a new terminal)
```bash
streamlit run frontend.py
```
The Streamlit interface will open in your default browser at `http://localhost:8501`

## Usage Guide

### Uploading a Resume

1. Navigate to the "Upload Resume" section in the web interface
2. Click the file uploader and select a PDF resume
3. Click the "Process Resume" button
4. Wait for the system to ingest and index the resume
5. Once complete, you will see a success message with a database ID

### Analyzing a Resume

After uploading a resume, you can perform various analyses:

1. In the "Analyze Resume" section, you will see your active Resume ID
2. Enter a query in the text area:
   - To get an overall score: "Rate my resume"
   - To check grammar: "What are the grammatical mistakes in my resume"
   - To assess skills: "Does this resume match a data scientist role"
   - To get specific feedback: Ask any question about the resume content

3. Click the "Analyze" button
4. The system will retrieve relevant resume sections and generate analysis
5. Results are displayed as formatted JSON for easy reading

## API Endpoints

### POST /upload
Uploads and processes a resume PDF.

Request:
- Method: POST
- Content-Type: multipart/form-data
- Body: PDF file

Response:
```json
{
    "message": "File processed successfully",
    "filename": "resume.pdf",
    "db_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### POST /analyze
Analyzes a resume based on a query.

Request:
- Method: POST
- Content-Type: application/x-www-form-urlencoded
- Body:
  - `db_id`: UUID of the processed resume
  - `query`: Analysis question or job description

Response:
```json
{
    "response": "{\"score\": 8, \"justification\": \"...\", \"improvements\": [...]}"
}
```

## Dependencies

Key packages used in this project:

- **LangChain**: Framework for building language model applications
- **LangChain-OpenAI**: Integration with OpenAI's API
- **Chroma**: Vector database for embeddings storage
- **FastAPI**: Modern web framework for building APIs
- **Streamlit**: Framework for building data applications with Python
- **python-dotenv**: Environment variable management

For a complete list, see `requirements.txt`

## Key Features

- Secure resume processing with automatic cleanup of temporary files
- Persistent vector database for efficient retrieval across sessions
- Support for complex analytical queries about resume content
- Structured JSON responses for easy integration with other tools
- Session state management to maintain resume context during analysis
- Error handling for common issues like missing files or API failures

## Configuration

The `config.py` file is currently empty but can be expanded to include:
- Custom chunk sizes for text splitting
- Vector database paths
- API endpoints and timeouts
- Model selection and parameters

## Development Notes

### Known Limitations

- The system requires an active internet connection for OpenAI API calls
- Vector databases are stored locally and not synced across machines
- The application processes one resume at a time in the frontend
- Large PDFs may take several minutes to process and index

## Troubleshooting

### API Connection Error
If you see "Connection Error" messages, ensure:
- FastAPI backend is running on port 8000
- Firewall is not blocking local connections
- Both services are in the same network

### OpenAI API Key Error
If embeddings or analysis fails:
- Verify your OpenAI API key is correct and active
- Check that your account has sufficient credits
- Ensure the `.env` file is in the project root

### Database Not Found Error
If you see "Database ID not found":
- Upload a new resume first
- Check that the database ID is correct
- Verify that the `vector_stores` directory exists

## Contributing

For contributions, improvements, or bug reports, please follow standard Git workflow practices and test your changes before submitting.

## License

This project is open source and available under the MIT License.

## Contact

For questions or feedback about this project, please reach out to the project maintainer.

## Acknowledgments

This project uses several powerful open-source libraries and APIs:
- OpenAI for language models and embeddings
- LangChain for building language model applications
- Chroma for efficient vector storage and retrieval
- Streamlit and FastAPI for the user interface and backend infrastructure
