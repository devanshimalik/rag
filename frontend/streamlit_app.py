import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG Chat", layout="wide")
st.title("📚 RAG with GenAI + LangChain")
st.caption("Upload documents and ask questions. Powered by FastAPI, LangChain, and Chroma.")

with st.sidebar:
    st.header("Document Indexing")
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "md"])

    if uploaded_file and st.button("Index Document"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        with st.spinner("Indexing document..."):
            try:
                r = requests.post(f"{API_URL}/upload", files=files, timeout=60)
                if r.status_code == 200:
                    st.success(r.json()["message"])
                else:
                    st.error(r.json().get("detail", "Error"))
            except Exception as e:
                st.error(str(e))

st.subheader("Ask a question about your documents")
question = st.text_input("Question", placeholder="e.g., What are the key findings?")

if st.button("Ask"):
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving and generating answer..."):
            try:
                r = requests.post(f"{API_URL}/query", json={"question": question}, timeout=60)
                if r.status_code == 200:
                    data = r.json()
                    st.markdown("### Answer")
                    st.write(data["answer"])
                    st.markdown("### Retrieved Sources")
                    for i, src in enumerate(data["sources"], 1):
                        with st.expander(f"Source {i} — {src['metadata'].get('source', 'Unknown')}"):
                            st.write(src["content"])
                            st.caption(str(src["metadata"]))
                else:
                    st.error(r.json().get("detail", "Error"))
            except Exception as e:
                st.error(str(e))