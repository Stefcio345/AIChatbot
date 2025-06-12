import os

import ollama
import streamlit as st

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from datetime import datetime

avatar_dir = "avatars"


def get_bot_response(history):
    ollama.pull('llama3.2')
    response = ollama.chat(model='llama3.2', messages=history, stream=True)
    return response

def save_to_azure_storage(input, output):
    try:
        account_url = 'https://crackemotions.blob.core.windows.net'
        default_credential = DefaultAzureCredential()

        blob_service_client = BlobServiceClient(account_url, credential=default_credential)

        container_name = str(datetime.now())
        blob_service_client.create_container(container_name)
        print('Created container', container_name)

        input_client = blob_service_client.get_blob_client(container=container_name, blob='input.txt')
        output_client = blob_service_client.get_blob_client(container=container_name, blob='output.txt')

        input_client.upload_blob(input)
        output_client.upload_blob(output)
        
        print('Uploaded input.txt and output.txt to ', container_name)
    except Exception as e:
        print('Failed to upload to blob storage', e)
    

st.title("Chatbot")

if "user_avatar" not in st.session_state or st.session_state.user_avatar is None:
    st.warning("Please select an avatar first on the 'user avatar' page.")
elif "bot_avatar" not in st.session_state or st.session_state.bot_avatar is None:
    st.warning("Please select an avatar first on the 'bot avatar' page.")
else:
    st.write(f"Your avatar:")
    st.image(os.path.join(avatar_dir, st.session_state.user_avatar), width=100)
    st.write("Type a message and see what I reply!")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar=os.path.join(avatar_dir, st.session_state.user_avatar)):
                st.write(message["content"])
        else:
            with st.chat_message(message["role"], avatar=os.path.join(avatar_dir, st.session_state.bot_avatar)):
                st.write(message["content"])

    # User input
    user_input = st.chat_input("Say something...")
    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user", avatar=os.path.join(avatar_dir, st.session_state.user_avatar)):
            st.write(user_input)

        input = st.session_state.messages
        bot_response = get_bot_response(st.session_state.messages)

        output = ''
        # Display message with typing effect
        with st.chat_message("bot", avatar=os.path.join(avatar_dir, st.session_state.bot_avatar)):
            placeholder = st.empty()
            typed_text = ""
            for chunk in bot_response:
                typed_text += chunk['message']['content']
                placeholder.markdown(typed_text)  # You can also use st.write(typed_text) but markdown looks cleanerre
            output += typed_text
            st.session_state.messages.append({"role": "bot", "content": typed_text})
        
        save_to_azure_storage(input, output)