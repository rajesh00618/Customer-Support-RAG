import os
import streamlit as st
import requests
import json

API_URL = os.environ.get("API_URL", "http://localhost:8001")

st.set_page_config(
    page_title="IntelliSupport",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #1a2035;
    --bg-chat: #0f172a;
    --accent: #3b82f6;
    --accent-light: #60a5fa;
    --accent-glow: rgba(59,130,246,0.15);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: #1e293b;
    --border-light: #334155;
    --success: #22c55e;
    --warning: #f59e0b;
    --error: #ef4444;
    --user-bubble: #1e3a5f;
    --bot-bubble: #1a2035;
    --gradient-start: #3b82f6;
    --gradient-end: #8b5cf6;
}

.stApp {
    font-family: 'Inter', -apple-system, sans-serif;
    background: var(--bg-primary);
}

section[data-testid="stSidebar"] {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary);
}

.header-container {
    background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(139,92,246,0.08));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.header-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
}
.header-container h1 {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 6px 0;
    letter-spacing: -0.02em;
}
.header-container p {
    color: var(--text-secondary);
    margin: 0;
    font-size: 0.92rem;
    line-height: 1.5;
}

.status-bar {
    display: flex;
    gap: 20px;
    margin: 14px 0 0 0;
    flex-wrap: wrap;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.78rem;
    color: var(--text-secondary);
    font-weight: 500;
}
.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
}
.status-dot.green { background: var(--success); box-shadow: 0 0 6px var(--success); }
.status-dot.yellow { background: var(--warning); box-shadow: 0 0 6px var(--warning); }
.status-dot.red { background: var(--error); box-shadow: 0 0 6px var(--error); }

.intent-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 12px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}
.intent-billing { background: rgba(34,197,94,0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.intent-technical_issue { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.intent-feature_request { background: rgba(168,85,247,0.15); color: #c084fc; border: 1px solid rgba(168,85,247,0.3); }
.intent-integration { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.intent-account_management { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
.intent-data_and_export { background: rgba(20,184,166,0.15); color: #2dd4bf; border: 1px solid rgba(20,184,166,0.3); }
.intent-general_inquiry { background: rgba(148,163,184,0.15); color: #cbd5e1; border: 1px solid rgba(148,163,184,0.3); }

.chat-bubble-user {
    background: linear-gradient(135deg, #1e3a5f, #1a2e50);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 20px;
    color: var(--text-primary);
    line-height: 1.6;
    font-size: 0.93rem;
    max-width: 85%;
    margin-left: auto;
}

.chat-bubble-bot {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px 16px 16px 4px;
    padding: 18px 22px;
    color: var(--text-primary);
    line-height: 1.7;
    font-size: 0.93rem;
    max-width: 90%;
}

.detail-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 10px;
}
.detail-card h4 {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin: 0 0 10px 0;
}
.detail-row {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.82rem;
}
.detail-row:last-child { border-bottom: none; }
.detail-label { color: var(--text-muted); font-weight: 500; }
.detail-value { color: var(--text-primary); font-weight: 600; font-family: 'SF Mono', monospace; font-size: 0.8rem; }

.chunk-badge {
    display: inline-block;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.25);
    border-radius: 8px;
    padding: 2px 10px;
    font-size: 0.72rem;
    color: var(--accent-light);
    font-family: 'SF Mono', monospace;
    margin: 2px 3px;
}

.feedback-btn {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 6px 16px;
    border-radius: 8px;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid var(--border);
    background: var(--bg-card);
    color: var(--text-secondary);
    transition: all 0.15s;
}
.feedback-btn:hover {
    border-color: var(--accent);
    color: var(--accent-light);
    background: var(--accent-glow);
}

.typing-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    color: var(--text-muted);
    font-size: 0.85rem;
}
.typing-dots {
    display: flex;
    gap: 4px;
}
.typing-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
    animation: bounce 1.4s infinite;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-6px); opacity: 1; }
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.01em;
    transition: all 0.15s;
}

.stChatInput {
    border-radius: 12px !important;
}

hr {
    border: none;
    border-top: 1px solid var(--border);
}

.sidebar-section {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 14px;
}
.sidebar-section h3 {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin: 0 0 10px 0;
    font-weight: 600;
}
.sidebar-section p, .sidebar-section span {
    color: var(--text-secondary);
    font-size: 0.85rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(
        '<div style="text-align:center; padding: 10px 0 20px 0;">'
        '<div style="font-size:2.2rem;">🔷</div>'
        '<div style="font-size:1.1rem; font-weight:700; color:#f1f5f9; margin-top:4px;">IntelliSupport</div>'
        '<div style="font-size:0.75rem; color:#64748b;">Nexora AI Support Platform</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("<h3>Configuration</h3>", unsafe_allow_html=True)
    top_k = st.slider(
        "Chunks to retrieve",
        min_value=1,
        max_value=10,
        value=3,
        help="Number of relevant document chunks to use for answering",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("<h3>Quick Actions</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("Health Check", use_container_width=True):
            try:
                r = requests.get(f"{API_URL}/health", timeout=5)
                if r.status_code == 200:
                    h = r.json()
                    st.success(f"DB connected | {h['chunks_indexed']} chunks indexed")
                else:
                    st.error("API error")
            except Exception as e:
                st.error(f"Cannot reach API: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("<h3>Pipeline Stages</h3>", unsafe_allow_html=True)
    stages = [
        ("Intent Classification", "Classifies query into 7 intents"),
        ("Query Embedding", "Dense vector representation"),
        ("Hybrid Retrieval", "Vector + BM25 + Jaccard rerank"),
        ("RAG Generation", "Context-grounded response"),
        ("Evaluation", "Faithfulness & relevance scoring"),
    ]
    for name, desc in stages:
        st.markdown(
            f'<div style="padding:6px 0; border-bottom:1px solid #1e293b;">'
            f'<span style="color:#60a5fa; font-size:0.78rem; font-weight:600;">{name}</span>'
            f'<br><span style="color:#64748b; font-size:0.7rem;">{desc}</span></div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("<h3>API Endpoints</h3>", unsafe_allow_html=True)
    st.code(
        "POST   /query\nPOST   /evaluate/{id}\nPOST   /feedback\nGET    /health",
        language="text",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align:center; padding:20px 0 4px 0; color:#334155; font-size:0.7rem;">'
        "Powered by NVIDIA + pgvector<br>Built with FastAPI &amp; Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )


# --- MAIN CONTENT ---
def check_api_health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        return r.status_code == 200 and r.json().get("status") == "ok"
    except Exception:
        return False


api_healthy = check_api_health()

# Header
st.markdown(
    '<div class="header-container">'
    "<h1>IntelliSupport</h1>"
    "<p>Autonomous AI customer support for Nexora — classify intent, retrieve docs, generate grounded answers.</p>"
    '<div class="status-bar">'
    f'<span class="status-pill"><span class="status-dot {"green" if api_healthy else "red"}"></span>'
    f'{"API Online" if api_healthy else "API Offline"}</span>'
    '<span class="status-pill"><span class="status-dot green"></span>NVIDIA Nemotron</span>'
    '<span class="status-pill"><span class="status-dot green"></span>pgvector + BM25</span>'
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

if not api_healthy:
    st.warning(
        "Cannot reach the IntelliSupport API at `localhost:8001`. "
        "Start it with: `uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload`"
    )

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render past messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div style="display:flex;justify-content:flex-end;margin:12px 0;">'
            f'<div class="chat-bubble-user">{msg["content"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        extra = msg.get("extra", {})
        intent = extra.get("intent", "")
        confidence = extra.get("intent_confidence", 0)
        chunks = extra.get("retrieved_chunks", [])
        query_id = extra.get("query_id", "")
        response_id = extra.get("response_id", "")

        intent_class = f"intent-{intent}" if intent else ""

        chunks_html = ""
        for c in chunks:
            chunks_html += f'<span class="chunk-badge">{c}</span>'

        detail_rows = ""
        if query_id:
            detail_rows += (
                f'<div class="detail-row"><span class="detail-label">Query ID</span>'
                f'<span class="detail-value">{query_id}</span></div>'
            )
        if response_id:
            detail_rows += (
                f'<div class="detail-row"><span class="detail-label">Response ID</span>'
                f'<span class="detail-value">{response_id}</span></div>'
            )
        if intent:
            detail_rows += (
                f'<div class="detail-row"><span class="detail-label">Intent</span>'
                f'<span class="detail-value">{intent.replace("_", " ").title()}</span></div>'
            )
        if confidence:
            detail_rows += (
                f'<div class="detail-row"><span class="detail-label">Confidence</span>'
                f'<span class="detail-value">{confidence:.0%}</span></div>'
            )

        st.markdown(
            '<div style="display:flex;justify-content:flex-start;margin:12px 0;">'
            '<div style="max-width:85%;">'
            f'<div class="chat-bubble-bot">{msg["content"]}</div>'
            f'{"<div class=\"intent-badge " + intent_class + "\">" + intent.replace("_", " ").title() + "</div>" if intent else ""}'
            "<div class='detail-card'>"
            "<h4>Response Details</h4>"
            f"{detail_rows}"
            f'<div class="detail-row"><span class="detail-label">Chunks</span>'
            f'<span class="detail-value">{chunks_html or "None"}</span></div>'
            "</div></div></div>",
            unsafe_allow_html=True,
        )

        if response_id:
            with st.expander(f"Submit Feedback for `{response_id}`", expanded=False):
                fb_col1, fb_col2 = st.columns([1, 3])
                with fb_col1:
                    rating = st.slider("Rating", 1, 5, 4, key=f"fb_rate_{response_id}")
                with fb_col2:
                    comment = st.text_input(
                        "Comment (optional)", key=f"fb_comment_{response_id}"
                    )
                if st.button("Submit Feedback", key=f"fb_submit_{response_id}"):
                    try:
                        fr = requests.post(
                            f"{API_URL}/feedback",
                            json={
                                "response_id": response_id,
                                "rating": rating,
                                "comment": comment or None,
                            },
                            timeout=10,
                        )
                        if fr.status_code == 200:
                            st.success("Feedback submitted!")
                        else:
                            st.error(f"Error: {fr.text}")
                    except Exception as e:
                        st.error(f"Failed: {e}")

            with st.expander(f"Evaluate Response `{response_id}`", expanded=False):
                if st.button("Run Evaluation", key=f"eval_{response_id}"):
                    with st.spinner("Running faithfulness & relevance evaluation..."):
                        try:
                            er = requests.post(
                                f"{API_URL}/evaluate/{response_id}",
                                timeout=60,
                            )
                            if er.status_code == 200:
                                ed = er.json()
                                ec1, ec2, ec3 = st.columns(3)
                                ec1.metric(
                                    "Faithfulness",
                                    f"{ed['faithfulness_score']:.0%}",
                                )
                                ec2.metric(
                                    "Relevance",
                                    f"{ed['relevance_score']:.0%}",
                                )
                                ec3.metric(
                                    "Combined",
                                    f"{ed['combined_score']:.0%}",
                                )
                            else:
                                st.error(f"Evaluation failed: {er.text}")
                        except Exception as e:
                            st.error(f"Evaluation error: {e}")


# Chat input
if prompt := st.chat_input("Ask a question about Nexora..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    st.markdown(
        f'<div style="display:flex;justify-content:flex-end;margin:12px 0;">'
        f'<div class="chat-bubble-user">{prompt}</div></div>',
        unsafe_allow_html=True,
    )

    with st.spinner(""):
        st.markdown(
            '<div class="typing-indicator">'
            '<div class="typing-dots"><span></span><span></span><span></span></div>'
            "Classifying intent, retrieving documents, generating response..."
            "</div>",
            unsafe_allow_html=True,
        )

        try:
            resp = requests.post(
                f"{API_URL}/query",
                json={"query": prompt, "top_k": top_k},
                timeout=90,
            )
            if resp.status_code == 200:
                data = resp.json()

                intent = data.get("intent", "")
                confidence = data.get("intent_confidence", 0)
                chunks = data.get("retrieved_chunk_ids", [])
                query_id = data.get("query_id", "")
                response_id = data.get("response_id", "")
                response_text = data.get("response_text", "")

                intent_class = f"intent-{intent}" if intent else ""
                chunks_html = ""
                for c in chunks:
                    chunks_html += f'<span class="chunk-badge">{c}</span>'

                detail_rows = ""
                if query_id:
                    detail_rows += (
                        f'<div class="detail-row"><span class="detail-label">Query ID</span>'
                        f'<span class="detail-value">{query_id}</span></div>'
                    )
                if response_id:
                    detail_rows += (
                        f'<div class="detail-row"><span class="detail-label">Response ID</span>'
                        f'<span class="detail-value">{response_id}</span></div>'
                    )
                if intent:
                    detail_rows += (
                        f'<div class="detail-row"><span class="detail-label">Intent</span>'
                        f'<span class="detail-value">{intent.replace("_", " ").title()}</span></div>'
                    )
                if confidence:
                    detail_rows += (
                        f'<div class="detail-row"><span class="detail-label">Confidence</span>'
                        f'<span class="detail-value">{confidence:.0%}</span></div>'
                    )

                st.markdown(
                    '<div style="display:flex;justify-content:flex-start;margin:12px 0;">'
                    '<div style="max-width:85%;">'
                    f'<div class="chat-bubble-bot">{response_text}</div>'
                    f'{"<div class=\"intent-badge " + intent_class + "\">" + intent.replace("_", " ").title() + "</div>" if intent else ""}'
                    "<div class='detail-card'>"
                    "<h4>Response Details</h4>"
                    f"{detail_rows}"
                    f'<div class="detail-row"><span class="detail-label">Chunks</span>'
                    f'<span class="detail-value">{chunks_html or "None"}</span></div>'
                    "</div></div></div>",
                    unsafe_allow_html=True,
                )

                if response_id:
                    with st.expander(f"Submit Feedback for `{response_id}`", expanded=False):
                        fb_col1, fb_col2 = st.columns([1, 3])
                        with fb_col1:
                            rating = st.slider(
                                "Rating", 1, 5, 4, key=f"fb_rate_{response_id}"
                            )
                        with fb_col2:
                            comment = st.text_input(
                                "Comment (optional)", key=f"fb_comment_{response_id}"
                            )
                        if st.button("Submit Feedback", key=f"fb_submit_{response_id}"):
                            try:
                                fr = requests.post(
                                    f"{API_URL}/feedback",
                                    json={
                                        "response_id": response_id,
                                        "rating": rating,
                                        "comment": comment or None,
                                    },
                                    timeout=10,
                                )
                                if fr.status_code == 200:
                                    st.success("Feedback submitted!")
                                else:
                                    st.error(f"Error: {fr.text}")
                            except Exception as e:
                                st.error(f"Failed: {e}")

                    with st.expander(f"Evaluate Response `{response_id}`", expanded=False):
                        if st.button("Run Evaluation", key=f"eval_{response_id}"):
                            with st.spinner("Running faithfulness & relevance evaluation..."):
                                try:
                                    er = requests.post(
                                        f"{API_URL}/evaluate/{response_id}",
                                        timeout=60,
                                    )
                                    if er.status_code == 200:
                                        ed = er.json()
                                        ec1, ec2, ec3 = st.columns(3)
                                        ec1.metric(
                                            "Faithfulness",
                                            f"{ed['faithfulness_score']:.0%}",
                                        )
                                        ec2.metric(
                                            "Relevance",
                                            f"{ed['relevance_score']:.0%}",
                                        )
                                        ec3.metric(
                                            "Combined",
                                            f"{ed['combined_score']:.0%}",
                                        )
                                    else:
                                        st.error(f"Evaluation failed: {er.text}")
                                except Exception as e:
                                    st.error(f"Evaluation error: {e}")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response_text,
                        "extra": {
                            "query_id": query_id,
                            "response_id": response_id,
                            "intent": intent,
                            "intent_confidence": confidence,
                            "retrieved_chunks": chunks,
                        },
                    }
                )
            else:
                st.error(f"API Error {resp.status_code}: {resp.text}")
        except requests.ConnectionError:
            st.error(
                "Cannot connect to the API server. Please ensure it is running at `localhost:8001`."
            )
        except requests.Timeout:
            st.error(
                "The request timed out. The model may be slow — please try again."
            )
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
