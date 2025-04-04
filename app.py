import streamlit as st
import base64


def get_base64_img(file_path: str, width: int = 100) -> str:
    with open(file_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return f"<img src='data:image/png;base64,{encoded}' width='{width}px' />"


def set_background_image(image_file: str):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def main_page():
    set_background_image("images/megumi.jpg")

    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .title {
        text-align: center;
        color: white;
        font-size: 72px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .bottom-icons {
        display: flex;
        justify-content: center;
        margin-top: 150px;
    }
    .icon {
        margin: 0 50px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='title'>CrackEmotions</h1>", unsafe_allow_html=True)

    # Ikony
    avatar_top = get_base64_img("images/avatar.png", width=150)
    chat_center = get_base64_img("images/chat.png", width=200)
    bottom_avatar = get_base64_img("images/avatar.png", width=120)
    bottom_bar = get_base64_img("images/bar.png", width=120)
    bottom_camera = get_base64_img("images/camera.png", width=120)

    st.markdown(f"<div style='text-align:center'>{chat_center}</div>", unsafe_allow_html=True)
    if st.button("💬 Przejdź do chatu"):
        st.session_state.page = "chat"
        st.rerun()

    # Przycisk avatar w rogu
    col1, col2 = st.columns([10, 1])
    with col2:
        st.markdown(f"<div style='position:absolute;top:20px;right:20px'>{avatar_top}</div>", unsafe_allow_html=True)
        if st.button("👤 Avatar"):
            st.session_state.page = "avatar"
            st.rerun()

    # Dolne ikony (bez funkcji)
    st.markdown(f"""
        <div class="bottom-icons">
            <div class="icon">
                {bottom_avatar}<br/>
                <button disabled>Avatar</button>
            </div>
            <div class="icon">
                {bottom_bar}<br/>
                <button disabled>Bar</button>
            </div>
            <div class="icon">
                {bottom_camera}<br/>
                <button disabled>Camera</button>
            </div>
        </div>
    """, unsafe_allow_html=True)


def chat_page():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    h1 {color: white; text-align: center; margin-top: 50px;}
    .center {text-align: center; color: white;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>Chat Page</h1>", unsafe_allow_html=True)
    st.markdown("<div class='center'>Tutaj będzie interfejs chatu.</div>", unsafe_allow_html=True)

    if st.button("⬅ Powrót"):
        st.session_state.page = "main"
        st.rerun()


def avatar_page():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    h1 {color: white; text-align: center; margin-top: 50px;}
    .center {text-align: center; color: white;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>Avatar Page</h1>", unsafe_allow_html=True)
    st.markdown("<div class='center'>Tutaj będzie wybór avatara.</div>", unsafe_allow_html=True)

    if st.button("⬅ Powrót"):
        st.session_state.page = "main"
        st.rerun()


def main():
    st.set_page_config(page_title="CrackEmotions", layout="wide")

    if "page" not in st.session_state:
        st.session_state.page = "main"

    if st.session_state.page == "chat":
        chat_page()
    elif st.session_state.page == "avatar":
        avatar_page()
    else:
        main_page()


if __name__ == "__main__":
    main()
