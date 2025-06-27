import os

import ollama
import streamlit as st

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from datetime import datetime, timezone
import json

avatar_dir = "avatars"


def get_bot_response(history):
    # Get the personality info from session
    personality = st.session_state.get("bot_personality", {})
    prompt_prefix = personality.get("prompt_prefix", "")

    # Inject the personality as a system message
    if prompt_prefix:
        history = [{"role": "system", "content": prompt_prefix}] + history

    # Call the model
    ollama.pull('llama3.2')  # Optional: you can remove this if already pulled
    response = ollama.chat(model='llama3.2', messages=history, stream=True)
    return response

def save_to_azure_storage(input, output):
    print('Uploading conversation to Azure Storage...')
    print(input)
    print(output)
    try:
        account_url = 'https://crackemotions.blob.core.windows.net'
        default_credential = DefaultAzureCredential()

        blob_service_client = BlobServiceClient(account_url, credential=default_credential)

        container_name = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ').lower()
        print(f'Creating container with name "{container_name}"...')
        blob_service_client.create_container(container_name)
        print('Created container', container_name)

        print('Uploading blobs...')
        input_client = blob_service_client.get_blob_client(container=container_name, blob='input.txt')
        output_client = blob_service_client.get_blob_client(container=container_name, blob='output.txt')

        input_client.upload_blob(input)
        print('Uploaded input.txt to ', container_name)
        
        output_client.upload_blob(output)
        print('Uploaded output.txt to ', container_name)
    except Exception as e:
        print('Failed to upload to blob storage:')
        print(e)


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
        avatar_path = os.path.join(avatar_dir, message.get("avatar", "default.png"))
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar=avatar_path):
                st.write(message["content"])
        else:
            with st.chat_message(message["role"], avatar=avatar_path):
                st.write(message["content"])

    # User input
    user_input = st.chat_input("Say something...")
    if user_input:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input, "avatar": st.session_state.user_avatar})

        with st.chat_message("user", avatar=os.path.join(avatar_dir, st.session_state.user_avatar)):
            st.write(user_input)

        input = json.dumps(st.session_state.messages, indent=4)
        bot_response = get_bot_response(st.session_state.messages)

        with st.chat_message("bot", avatar=os.path.join(avatar_dir, st.session_state.bot_avatar)):
            placeholder = st.empty()
            typed_text = ""
            for chunk in bot_response:
                typed_text += chunk['message']['content']
                placeholder.markdown(typed_text)  # You can also use st.write(typed_text) but markdown looks cleanerre
            st.session_state.messages.append({"role": "bot", "content": typed_text, "avatar": st.session_state.bot_avatar})
        
        output = json.dumps(st.session_state.messages[-1], indent=4)
        save_to_azure_storage(input, output)