import streamlit as st
import utils as u


st.set_page_config(page_title="PL/SQL Analyzer", layout="wide")

st.title("PL/SQL Job Analyzer")

# Upload the file
uploaded_file = st.file_uploader("Upload a PL/SQL file", type=["sql", "txt"])

# Read the file contents
if uploaded_file is not None:
    # Decode to string
    plsql_code = uploaded_file.read().decode("utf-8")

    # Show file contents in an expandable section
    with st.expander("📄 View Uploaded PL/SQL Code"):
        st.code(plsql_code, language="sql")

    # Store for downstream use (e.g., chunking or RAG)
    st.session_state["plsql_code"] = plsql_code

chunks = u.chunk_plsql_all(plsql_code)
# Display the chunks in an expandable section
if chunks:
    with st.expander("📦 View PL/SQL Code Chunks"):
        for i, chunk in enumerate(chunks):
            st.subheader(f"Chunk {i + 1}")
            st.code(chunk, language="sql")