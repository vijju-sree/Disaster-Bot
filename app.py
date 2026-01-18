import streamlit as st
import requests

# -----------------------------
# Insert your Google API Key here
API_KEY = "UR-API-Key"
MODEL_NAME = "gemini-2.5-flash"
# -----------------------------

st.set_page_config(
    page_title="Disaster Management Explainer Bot",
    page_icon="🌀",
    layout="centered"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌀 Disaster Explainer Bot")
st.sidebar.markdown("""
**Project 41**  
Disaster Management Response & Relief Process Explainer  

**Purpose**
- Public awareness
- Procedural explanations
- No alerts / No predictions  

**Tech Stack**
- Gemini Flash
- Python
- Streamlit
""")

st.sidebar.markdown("---")
st.sidebar.info("⚠️ Informational use only")

# ---------------- MAIN UI ----------------
st.title("🚨 Disaster Management Response & Relief Bot")
st.caption("Explains evacuation, relief camps, response stages & safety procedures")

st.markdown("""
<div style="padding:15px;border-radius:10px;">
This AI bot provides **clear and factual explanations** about disaster response processes.  
It **does NOT** issue emergency alerts or predictions.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- INPUT AREA ----------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "💬 Ask a disaster-related question:",
        placeholder="Example: What happens at relief camps?"
    )
    send_button = st.form_submit_button("Send ➤")

# ---------------- API CALL FUNCTION ----------------
def query_gemini_api(prompt_text):
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            first_candidate = data.get("candidates", [{}])[0]
            content = first_candidate.get("content", {})
            parts = content.get("parts", [])
            if parts:
                return parts[0].get("text", "No response text found.")
            return "No response generated."
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

# ---------------- HANDLE INPUT ----------------
if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    system_prompt = (
        "You are a Disaster Management Information Bot. "
        "Answer only with factual, informative responses about evacuation, relief, "
        "disaster response stages, and safety precautions. "
        "Do NOT provide emergency alerts, warnings, or predictions."
    )

    full_prompt = f"{system_prompt}\n\nUser: {user_input}\nBot:"
    bot_response = query_gemini_api(full_prompt)

    st.session_state.messages.append({"role": "bot", "content": bot_response})

# ---------------- CHAT DISPLAY ----------------
st.markdown("### 💬 Conversation")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="padding:10px;border-radius:10px;margin-bottom:8px;">
            <b>You:</b> {msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="padding:10px;border-radius:10px;margin-bottom:8px;">
            <b>Bot:</b> {msg['content']}
            </div>
            """,
            unsafe_allow_html=True
        )
