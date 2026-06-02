import streamlit as st
import requests
import json

API_URL = "http://localhost:8001"

st.set_page_config(page_title="IntelliSupport", page_icon="🤖", layout="centered")

st.title("🤖 IntelliSupport")
st.markdown("Ask questions about Nexora — the RAG pipeline classifies intent, retrieves relevant docs, and generates answers.")

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Number of chunks to retrieve", 1, 10, 3)
    st.divider()
    st.markdown("**Available endpoints**")
    st.code("POST /query\nPOST /evaluate/{id}\nPOST /feedback\nGET  /health")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "extra" in msg:
            with st.expander("Details"):
                st.json(msg["extra"])

if prompt := st.chat_input("Ask a question about Nexora..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Classifying, retrieving, generating..."):
            try:
                resp = requests.post(
                    f"{API_URL}/query",
                    json={"query": prompt, "top_k": top_k},
                    timeout=60
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.markdown(data["response_text"])
                    extra = {
                        "query_id": data["query_id"],
                        "response_id": data["response_id"],
                        "intent": data["intent"],
                        "intent_confidence": data["intent_confidence"],
                        "retrieved_chunks": data["retrieved_chunk_ids"]
                    }
                    with st.expander("View details"):
                        st.json(extra)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["response_text"],
                        "extra": extra
                    })
                else:
                    st.error(f"Error {resp.status_code}: {resp.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")
