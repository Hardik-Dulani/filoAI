import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import google_serp
import requests

# Load environment variables from .env file
load_dotenv()

# Access the API key
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
user_input = st.text_input("Enter your message:")

if user_input:
    if user_input.strip().lower().startswith("google"):
        input_query = user_input.split(" ", 1)[1].strip()
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(
                "Searching Google For: " + input_query + " ..."
            )
            search_results = google_serp.search_google_web_automation(input_query)
            over_all_summary = ""

            source_links = "\n \n Sources: \n \n"

            for result in search_results:
                blog_url = result["url"]
                source_links += blog_url + "\n \n"
                message_placeholder.markdown(f"Search Done, Reading {blog_url}")
                blog_summary_prompt = f"Summarize the content from this URL: {blog_url}"
                
            message_placeholder.markdown(f"Generating Final Search Report...")

            new_search_prompt = f"Generate a comprehensive summary based on the following information: {over_all_summary}"
            
            response = requests.post(
                headers={"Authorization": f"Bearer {os.getenv('GEMINI_API_KEY')}"},
                
            )
            response_obj = response.json()
            research_final = response_obj.get('text', '')

            message_placeholder.markdown(research_final + source_links)
            st.write(research_final + source_links)

    else:
        # Handle non-Google search input
        response = chat_session.send_message(user_input)
        st.write(response.text)
