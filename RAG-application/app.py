import streamlit as st
import utils as u
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI


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
st.session_state["chunks"] = chunks

# Display the chunks in an expandable section
if chunks:
    with st.expander("📦 View PL/SQL Code Chunks"):
        for i, chunk in enumerate(chunks):
            st.subheader(f"Chunk {i + 1}")
            st.code(chunk, language="sql")

db = FAISS.from_texts(st.session_state["chunks"], embedding=OpenAIEmbeddings())

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    retriever=db.as_retriever(),
    chain_type="map_reduce",
)

prompt = '''
You are analyzing a PL/SQL procedure. Provide the following:
1. High-level summary (should be no more than 1-2 sentences)
2. Input parameters and expected data types
3. Output results or state changes
4. Business logic steps including a detailed description of what each function does and how it works
5. Other PL/SQL objects or DB tables this job depends on

'''
if st.button("Analyze PL/SQL Code"):
    result = qa.run(prompt)
    # Display the result in an expandable section that can be manually edited
    with st.expander("🔍 Analysis Result"):
        st.text_area("Analysis Output", value=result, height=300)
