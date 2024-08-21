import streamlit as st
import requests
import os
from dotenv import load_dotenv
import test
import io
from PIL import Image
# Load environment variables from .env file
def generate_image(prompt):
    load_dotenv()

    # Access the API key
    LW_API = os.getenv("LIMEWIRE_KEY")

    # Streamlit UI

    if prompt:
        ratio = st.radio('Please confirm the aspect Ratio'["1:1", "13:19", "19:13", "2:3", "3:2"])
        if ratio:
        # API endpoint
            url = "https://api.limewire.com/api/image/generation"

            # API request payload
            payload = {
                "prompt": prompt,
                "quality":'MID',
                "aspect_ratio": ratio 
            }

            headers = {
                "Content-Type": "application/json",
                "X-Api-Version": "v1",
                "Accept": "application/json",
                "Authorization": f"Bearer {LW_API}"
            }

            # Make the API request
            response = requests.post(url, json=payload, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
            data = response.json()
            image_url = data['data'][0]['asset_url']  # Adjust based on the response format

            if image_url:
                # Display the image in the Streamlit app
                st.image(image_url, caption=f"Generated Image for: {prompt}")

                # Fetch the image content from the URL
                image_response = requests.get(image_url)
                image = Image.open(io.BytesIO(image_response.content))

                # Convert the image to bytes for downloading
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPG')
                img_byte_arr = img_byte_arr.getvalue()

                # Add a download button
                st.download_button(
                    label="Download Image",
                    data=img_byte_arr,
                    file_name="generated_image.",jpg
                    mime="image/jpg"
                )

            else:
                st.error("Failed to retrieve the image URL from the response.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")

    # Display a message if no prompt is provided
    else:
        st.write("Enter a prompt to generate an image.")
