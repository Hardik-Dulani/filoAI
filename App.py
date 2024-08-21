import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import test as ts



# Load environment variables from .env file
load_dotenv()

# Access the API key
# Configure the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start a chat session

chat_session = model.start_chat(history=[])

# Streamlit UI
st.title("fílos AI Chat")

# Get user input
user_input = st.text_input("Enter your message:",key = 'base_prompt')

if user_input:
    # Send the user input to the model and get the response
    response = chat_session.send_message(user_input)
    
    # Display the response
    st.write(response.text)

    if st.button("Go Back to Home"):
                    st.session_state['redirect'] = True
                    st.experimental_rerun()