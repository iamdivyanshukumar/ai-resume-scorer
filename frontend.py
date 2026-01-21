import streamlit as st
import requests
import json

# FastAPI Base URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Resume Scorer", page_icon="📄")
st.title("📄 AI Resume Scorer & Analyzer")

# --- SESSION STATE ---
# This keeps the DB_ID in memory so we don't lose it when the page reloads
if "db_id" not in st.session_state:
    st.session_state["db_id"] = None

# ==========================================
# SECTION 1: UPLOAD RESUME
# ==========================================
st.header("1. Upload Resume")
uploaded_file = st.file_uploader("Upload a PDF Resume", type=["pdf"])

if uploaded_file is not None:
    if st.button("Process Resume"):
        with st.spinner("Ingesting and Indexing Resume..."):
            try:
                # Prepare the file for the API request
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                
                # Send to FastAPI
                response = requests.post(f"{API_URL}/upload", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    # SAVE THE ID TO SESSION STATE
                    st.session_state["db_id"] = data["db_id"]
                    st.success(f"Resume Processed! ID: {data['db_id']}")
                else:
                    st.error(f"Error: {response.text}")
                    
            except Exception as e:
                st.error(f"Connection Error: {e}")

# ==========================================
# SECTION 2: ANALYZE / ASK QUESTIONS
# ==========================================
st.divider()
st.header("2. Analyze Resume")

if st.session_state["db_id"] is None:
    st.info("Please upload a resume first to enable analysis.")

else:
    st.write(f"Active Resume ID: `{st.session_state['db_id']}`")
    
    # Text Area for Job Description or Question
    user_query = st.text_area("Enter Job Description or Question:", height=150, placeholder="Paste Job Description here or ask: 'Rate this resume'")

    if st.button("Analyze"):
        if not user_query:
            st.warning("Please enter a query.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    # Send Form Data (db_id and query) to FastAPI
                    payload = {
                        "db_id": st.session_state["db_id"],
                        "query": user_query
                    }
                    
                    response = requests.post(f"{API_URL}/analyze", data=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        llm_response_text = result["response"]

                        # Try to parse the JSON string into a Python Dictionary for pretty printing
                        try:
                            json_data = json.loads(llm_response_text)
                            st.subheader("Analysis Result")
                            st.json(json_data) # Pretty Print JSON
                        except json.JSONDecodeError:
                            # Fallback if LLM didn't output perfect JSON
                            st.write(llm_response_text)
                            
                    else:
                        st.error(f"Error: {response.text}")
                        
                except Exception as e:
                    st.error(f"Connection Error: {e}")