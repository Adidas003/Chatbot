import os
import json
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Coder Connects LLAMA 3.1",
    page_icon="🦙",
    layout="centered"
)

# Define the working directory and load the data
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("API key is missing in the config.json file.")
    st.stop()

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

try:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    st.stop()

# Initialize to chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🦙 Welcome to ADIOS Chatbot")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask CYour Questions.....")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )

        assistant_response = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

        with st.chat_message("assistant"):
            st.markdown(assistant_response)

    except Exception as e:
        st.error(f"Error while fetching the response from GROQ: {e}")