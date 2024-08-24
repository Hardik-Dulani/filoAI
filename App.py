import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

import helper, prompts, google_serp
from io import BytesIO





# Load environment variables from .env file
load_dotenv()

# Access the API key
# Configure the API key
gs_api = os.getenv("gs_api_key")
cse_id = os.getenv("cse_id")

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



# Streamlit UI
st.title("fílos AI")

# Get user input
with st.chat_message('assistant'):
    st.write('Hello I am fílos AI, how can I help you today?')
with st.chat_message("user"):
    user_input = st.text_input("Enter your message:",key = 'base_prompt')
    

chat_session = model.start_chat(history=[])


if user_input:
    # Send the user input to the model and get the response
    
    try:
        prompt_type= chat_session.send_message(f"{prompts.classify_prompt}{user_input}").text
        
        user_input = chat_session.send_message(f"{prompts.remove_prefix} {user_input}").text
        st.write(prompt_type)
        if prompt_type == 'Image generation \n':
            response = 'I hope the picture met your expectations, if you want you can download the image or generate a new one'
            with st.spinner("Processing..."):
        
                img_prompt = chat_session.send_message(f"{prompts.img_prompt} {user_input}").text
                img = helper.generate_img(img_prompt)
            with st.chat_message("assistant"):
                st.image(img, caption="credit: pollinations.ai")
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='JPEG')  # You can change the format if needed
                img_byte_arr = img_byte_arr.getvalue()

                # Add a download button below the image
                st.download_button(
                    label="Download Image",
                    data=img_byte_arr,
                    file_name="downloaded_image.jpeg",  # You can change the file name
                    mime="image/png"  # You can change the MIME type based on the image format
                )

        elif prompt_type == 'Summarize \n':
            with st.spinner("Processing..."):
                response = chat_session.send_message(f"{prompts.summary_prompt}{user_input}").text
        elif prompt_type == 'Rewrite \n':
            with st.spinner("Processing..."):
                response = chat_session.send_message(f"{prompts.rewrite_prompt}{user_input}").text
        elif prompt_type == 'Internet Search \n' or 'InternetSearch \n':
            user_input = chat_session.send_message(f"{prompts.remove_prefix} {user_input}").text
            
            
            with st.spinner("Processing..."):
                search_results = google_serp.search_google_custom_api(user_input,gs_api,cse_id)
                
                curr_articles = ""
                j = 1
                
                for i in search_results:
                    
                    this_article = helper.get_article_from_url(i['url'])
                    if this_article:
                        curr_articles += f"Article {j} \n" + this_article + "\n"
                        j+=1
            

            if curr_articles != "":
                
                try:
                    response = chat_session.send_message(f"{prompts.articles_summary_prompt} query={user_input} articles = {curr_articles}").text
                except Exception as e:
                    st.write(e)
                    response = chat_session.send_message(prompts.general_prompt + user_input).text

            else:

                st.write('Could not fetch information due to privacy purposes from internet, this is something I can provide though')
                st.markdown("---")
                response = chat_session.send_message(prompts.general_prompt + user_input).text


        elif prompt_type == 'About \n' or prompt_type == 'About':
            response = chat_session.send_message(f"{prompts.about_prompt}{user_input}").text

        else:
            response = chat_session.send_message(prompts.general_prompt + user_input).text
            
        
    except Exception as e:

        
        response = 'This search may contain some inappropriate content which I can not generate.'
    with st.chat_message("assistant"):
            st.write(response)
    
            

