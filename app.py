import streamlit as st
from google import genai
from config import API_KEY, SYSTEM_INSTRUCTION

# Page Config
st.set_page_config(page_title="Arjun AI - Study Mentor", page_icon="🎓", layout="centered")

st.title("🎓 Arjun AI - Study Mentor")
st.caption("🌐 Powered by Arjun | Visit: arjunhub.com")

# Initialize GenAI Client
client = genai.Client(api_key=API_KEY)

# Initialize Chat Session in Streamlit Session State
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-3.8-flash",
        config={"system_instruction": SYSTEM_INSTRUCTION}
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Box
if user_input := st.chat_input("Apna sawal yahan pucho (e.g., Explain Physics laws)..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Arjun AI soch raha hai..."):
            try:
                response = st.session_state.chat.send_message(user_input)
                ai_reply = response.text
                st.markdown(ai_reply)
                # Append assistant message
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                error_msg = f"Kuch error aa gaya: {e}"
                st.error(error_msg)