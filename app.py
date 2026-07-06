import streamlit as st
import requests

# -----------------------------
# Insert your Google API Key here
API_KEY = "YOUR-API-KEY"
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

**Features**
- Auto language detection  
- Telugu (English letters supported)  
- English support  
- Informational responses only  

**Tech Stack**
- Gemini Flash
- Python
- Streamlit
""")

st.sidebar.info("⚠️ Informational use only")

# ---------------- MAIN UI ----------------
st.title("🚨 Disaster Management Response & Relief Bot")
st.caption("Explains evacuation, relief camps, response stages & safety procedures")

st.markdown("""
<div style="padding:15px;border-radius:10px;">
This AI bot explains disaster response procedures for public awareness.  
<strong>No alerts, no predictions.</strong>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- INPUT ----------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "💬 Ask a disaster-related question:",
        placeholder="Example: varadalu vachinappudu em cheyyali?"
    )
    send = st.form_submit_button("Send ➤")

# ---------------- GEMINI API CALL ----------------
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
            candidate = data.get("candidates", [{}])[0]
            parts = candidate.get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "")
            return "No response generated."
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

# ---------------- HANDLE INPUT ----------------
if send and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    system_prompt = (
    "You are a Disaster Management Information Bot.\n"
    "Your job is to explain disaster response, evacuation procedures, "
    "relief camps, response stages, and safety precautions.\n\n"

    "Response style rules:\n"
    "- Give VERY SHORT and CLEAR answers.\n"
    "- Use bullet points if possible.\n"
    "- Maximum 3–5 lines only.\n"
    "- Avoid long explanations.\n\n"

    "Language rules:\n"
    "- Automatically detect the user's language.\n"
    "- If the user types Telugu using English letters (Tanglish), "
    "respond in proper Telugu script.\n"
    "- If the user types in English, respond in English.\n\n"

    "Safety rules:\n"
    "- Provide only informational and educational content.\n"
    "- Do NOT give alerts, warnings, predictions, or rescue coordination.\n"
)
 

    full_prompt = f"{system_prompt}\nUser: {user_input}\nBot:"
    bot_response = query_gemini_api(full_prompt)

    st.session_state.messages.append({"role": "bot", "content": bot_response})

# ---------------- DISPLAY CHAT ----------------
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
