import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import test as ts
import helper
from io import BytesIO




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



# Streamlit UI
st.title("fílos AI Chat")

# Get user input


curr_history = []
user_input = 0
chat_session = model.start_chat(history=curr_history)
if not curr_history:
    user_input = st.text_input("Enter your message:",key = 'base_prompt')
    



if user_input:
    # Send the user input to the model and get the response
    
    try:
        prompt_type= chat_session.send_message(f"You are my helper AI, that supports prompts for other AI in my application, I have multiple AIs that work on certain domains, You just have to take in the prompt I provide, understand and classify it in one of following categories, ['Continuous', 'Image generation', 'Rewrite', 'Summarize' , 'Internet Search', 'others'] you just have to give one word output with the name of the category, nothing else, regardless of the prompt, please make sure there are no other characters or line break prompt:{user_input}").text
        curr_history.append({"role": "user", "content": user_input})
    except Exception as e:
        st.write(e)
    if prompt_type == 'Image generation \n':
        img = helper.generate_img(user_input)
        st.image(img, caption="Displayed Image", use_column_width=True)
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
    else:
        other_session = model.start_chat(history=curr_history)
        response = 'Hello, how can I help you?'
        i = 0
        while True:
            i+=1
            st.write('response')
            try:
                user_response = st.text_input("",key = i)
                reponse = other_session.send_message(user_input)
                curr_history.append({"role": "user", "content": response.text})
                
            except Exception as e:
                st.write(e)
                break
        
        
        




    # prompt_type = dict(prompt_obj.get('text', 'General')
    # Display the response
    
    
    
