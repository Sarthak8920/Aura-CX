import streamlit as st
import requests
import os
# ---------------- CONFIG ----------------
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/chat")

st.set_page_config(
    page_title="AURA-CX | Retail AI Agent",
    page_icon="🤖",
    layout="centered"
)

# ---------------- SESSION STATE INIT ----------------
if "response" not in st.session_state:
    st.session_state.response = ""

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# ---------------- HEADER ----------------
st.title("🤖 AURA-CX: Retail AI Agent")
st.caption("Multi-Agent AI System powered by Groq, LangChain & LangGraph")
st.divider()

# ---------------- INPUT ----------------
user_query = st.text_area(
    "Customer Query",
    placeholder="Example: My payment failed, money was deducted, order is delayed...",
    height=120,
    key="query_input"
)

# ---------------- ACTION ----------------
if st.button("Resolve Issue 🚀"):
    if not user_query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("AI agents are working..."):
            try:
                # IMPORTANT: always send fresh request
                response = requests.post(
                    BACKEND_URL,
                    json={"query": user_query},
                    timeout=60
                )

                if response.status_code == 200:
                    st.session_state.response = response.json()["response"]
                    st.session_state.last_query = user_query
                else:
                    st.session_state.response = f"Backend error: {response.text}"

            except Exception as e:
                st.session_state.response = (
                    "Backend not reachable. "
                    "Make sure FastAPI is running on port 8000.\n\n"
                    f"Error: {e}"
                )

# ---------------- OUTPUT ----------------
if st.session_state.response:
    st.success("Issue Resolved")
    st.markdown("### 🧠 AI Response")
    st.write(st.session_state.response)

# ---------------- FOOTER ----------------
st.divider()
st.caption("Industry-grade multi-agent architecture | Streamlit Demo UI")
