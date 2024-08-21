import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API key for Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model with generation config
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize session state for chat history and input if they don't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Streamlit UI
st.title("fílos AI Chat")

# Reload button to reset the session state

# Display the conversation history

# Input field for user message
user_input = st.text_input("Enter your message:", value=st.session_state.user_input, key="input")

# Process the input when it's not empty
if user_input and user_input != st.session_state.user_input:
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

    try:
        # Initialize the model with the current history
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
        chat_session = model.start_chat(history=st.session_state.chat_history)

        # Get the model response
        response = chat_session.send_message(user_input)
        response_text = response.text

        # Add model's response to history
        st.session_state.chat_history.append({
            "role": "model",
            "parts": [{"text": response_text}]
        })

        # Display the response
        st.write(f"**Model:** {response_text}")

    except Exception as e:
        st.error(f"An error occurred while sending the message: {e}")

    # Update session state to clear the input field
    st.session_state.user_input = ""
