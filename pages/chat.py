import os

import ollama
import streamlit as st

avatar_dir = "avatars"

def get_bot_response(history):
    ollama.pull('llama3.2')
    response = ollama.chat(model='llama3.2', messages=history, stream=True)
    return response

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

        bot_response = get_bot_response(st.session_state.messages)

        # Display message with typing effect
        with st.chat_message("bot", avatar=os.path.join(avatar_dir, st.session_state.bot_avatar)):
            placeholder = st.empty()
            typed_text = ""
            for chunk in bot_response:
                typed_text += chunk['message']['content']
                placeholder.markdown(typed_text)  # You can also use st.write(typed_text) but markdown looks cleanerre
            st.session_state.messages.append({"role": "bot", "content": typed_text})