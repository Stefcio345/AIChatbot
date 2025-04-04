import base64
import streamlit as st
import os


def set_avatar(user_avatar):
    st.session_state.user_avatar = user_avatar

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


avatar_files = [f for f in os.listdir(st.session_state.avatars_dir) if f.endswith(".png")]
avatar_paths = {file: os.path.join(st.session_state.avatars_dir, file) for file in avatar_files}

st.title("Select User Avatar")
cols = st.columns(5)  # Display avatars in a grid


for i, file in enumerate(avatar_files):
    with cols[i % 5]:
        avatar_key = f"avatar_{file}"

        # Convert image to base64
        img_base64 = get_image_base64(avatar_paths[file])

        # Set border if selected
        selected_class = "selected" if st.session_state.get("user_avatar") == file else ""

        # Create a button for selecting the avatar
        if st.button(f"Select {file}", key=avatar_key):
            set_avatar(file)
            selected_class = "selected" if st.session_state.get("user_avatar") == file else ""

        # Display avatar image
        st.markdown(f"""
            <style>
            .avatar-img {{
                border: 4px solid #000000;
                transition: transform 0.2s ease;
                border-radius: 10px;
                cursor: pointer;
                width: 120px;
                height: 120px;
            }}
            .avatar-img:hover {{
                transform: scale(1.1);
            }}
            .avatar-img.selected {{
                border: 4px solid #4CAF50;  /* Green border for selection */
                box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);  /* Glow effect */
            }}
            </style>
            <img src="data:image/png;base64,{img_base64}" 
                 alt="{file}" class="avatar-img {selected_class}" />
        """, unsafe_allow_html=True)
