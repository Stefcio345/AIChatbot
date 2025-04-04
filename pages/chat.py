import streamlit as st
import random
import os

avatar_dir = "avatars"

responses = [
    "Człowiek jest wielki nie przez to, co ma, nie przez to, kim jest, lecz przez to, czym dzieli się z innymi.",
    "Niech nasza droga będzie wspólna. Niech nasza modlitwa będzie pokorna. Niech nasza miłość będzie potężna.",
    "Przyszłość zaczyna się dzisiaj, nie jutro.",
    "Musicie od siebie wymagać, nawet gdyby inni od was nie wymagali.",
    "Nie żyje się, nie kocha się, nie umiera się - na próbę.",
    "Wymagajcie od siebie, choćby inni od was nie wymagali.",
    "Człowiek nie może siebie sam do końca zrozumieć bez Chrystusa.",
    "Wolność nie jest ulgą, lecz trudem wielkości.",
    "Miłość mi wszystko wyjaśniła, miłość wszystko rozwiązała - dlatego uwielbiam tę Miłość, gdziekolwiek by przebywała.",
    "Nie lękajcie się!"
]

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
        if(message["role"] == "user"):
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

        # Generate bot response
        bot_response = random.choice(responses)
        st.session_state.messages.append({"role": "bot", "content": bot_response})
        with st.chat_message("bot", avatar=os.path.join(avatar_dir, st.session_state.bot_avatar)):
            st.write(bot_response)
