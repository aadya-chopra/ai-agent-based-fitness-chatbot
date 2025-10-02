# app.py

import streamlit as st
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv() 

from src.agent import get_agent_response



# Set API Key (needed for Streamlit Cloud deployment too)
# The Groq object automatically picks up the GROQ_API_KEY from environment variables
if "GROQ_API_KEY" not in os.environ:
    st.error("GROQ_API_KEY not found. Please set it in your .env file or Streamlit secrets.")
    st.stop()


# --- Streamlit UI Setup ---
st.set_page_config(page_title="💪 GroqFit AI Coach", layout="wide")
st.title("💪 GroqFit AI Coach")
st.caption("⚡ Powered by Groq and LangChain")

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm GroqFit, your fast AI fitness coach. What are your fitness goals today?"}
    ]

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask me for a workout plan, diet advice, or recovery tips..."):
    # 1. Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get agent response
    with st.spinner("Thinking... Groq is fast, but I'm planning your perfect response!"):
        response = get_agent_response(prompt)
    
    # 3. Add assistant message to history and display
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)