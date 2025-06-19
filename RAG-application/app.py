import streamlit as st
import utils as u
import tiktoken
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI


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

tokenizer = tiktoken.encoding_for_model("gpt-4o")
num_tokens = len(tokenizer.encode(plsql_code))

print(f"Number of tokens in the uploaded PL/SQL code: {num_tokens}")



# chunks = u.chunk_plsql_all(plsql_code)
# st.session_state["chunks"] = chunks

# # Display the chunks in an expandable section
# if chunks:
#     with st.expander("📦 View PL/SQL Code Chunks"):
#         for i, chunk in enumerate(chunks):
#             st.subheader(f"Chunk {i + 1}")
#             st.code(chunk, language="sql")

# db = FAISS.from_texts(st.session_state["chunks"], embedding=OpenAIEmbeddings())

llm_ = ChatOpenAI(
    model_name="gpt-4o",       # 👈 Change this to the model you want
    temperature=0.1
)

# qa = RetrievalQA.from_chain_type(
#     llm=llm_,
#     retriever=db.as_retriever(),
#     chain_type="map_reduce",
# )

prompt = '''
You are analyzing a PL/SQL procedure. Provide the following:
1. High-level summary (should be no more than 1-2 sentences)
2. Input parameters and expected data types
3. Output results or state changes
4. An analysis of the buisness logic. This should be detailed and can be as long as needed
5. A list of every function, its parameters, and a description of what it does
6. Other PL/SQL objects or DB tables this job depends on

'''

full_prompt = f"""
    You are analyzing a PL/SQL procedure. Provide the following:
    1. High-level summary (no more than 1–2 sentences)
    2. Input parameters and expected data types
    3. Output results or state changes
    4. Detailed analysis of the business logic and what this code does as well as its purpose
       (this can be as long as needed)
    5. A list of every function, its parameters, and a description of what it does
    6. Other PL/SQL objects or DB tables this job depends on

    PL/SQL Code:
    {plsql_code}
    """

if st.button("Analyze PL/SQL Code"):
    # result = qa.invoke(prompt)
    result = llm_.invoke(full_prompt)
    answer=result.content if hasattr(result, 'content') else result
    # Display the result in an expandable section that can be manually edited
    with st.expander("🔍 Analysis Result"):
        st.text_area("Analysis Output", value=answer, height=500)
