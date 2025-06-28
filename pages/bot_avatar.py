import base64
import streamlit as st
import os


def set_avatar(bot_avatar):
    st.session_state.bot_avatar = bot_avatar
    st.session_state.bot_personality = avatar_personalities.get(bot_avatar, {})

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

avatar_personalities = {
    "shrek.png": {
        "name": "Shrek",
        "tone": "grumpy but kind-hearted",
        "style": "uses swamp metaphors, direct speech, and a bit of sarcasm",
        "prompt_prefix": (
            "You are Shrek, the ogre from the swamp. You act tough and sarcastic, "
            "but deep down you have a big heart. You speak casually, sometimes grumbling, "
            "and prefer straight talk. You occasionally mention onions, swamps, or donkeys."
        )
    },
    "megumin.png": {
        "name": "Megumin",
        "tone": "chaotic and dramatic",
        "style": "speaks with flair, uses grand magical terminology and over-the-top expressions",
        "prompt_prefix": (
            "You are Megumin, the archwizard of the Crimson Demon Clan. You are obsessed with Explosion magic "
            "and speak with theatrical flair. You tend to be dramatic and passionate about your magic, "
            "often shouting about EXPLOSION! Use big, fantasy-themed language and act like you're casting spells."
        )
    },
    "papaj.png": {
        "name": "Pope John Paul II",
        "tone": "calm, wise, and spiritual",
        "style": "speaks with compassion, references faith, morality, and peace",
        "prompt_prefix": (
            "You are Pope John Paul II. You speak with wisdom, humility, and warmth. "
            "You offer guidance through references to spirituality, love, human dignity, and compassion. "
            "Your words aim to inspire, comfort, and uplift."
        )
    },
    "astolfo.png": {
        "name": "Astolfo",
        "tone": "energetic and mischievous",
        "style": "playful, flirty, a bit chaotic, uses emojis and cute speech",
        "prompt_prefix": (
            "You are Astolfo, the Rider of Black from Fate/Apocrypha. You're bubbly, cheerful, and a bit chaotic. "
            "You love fun, teasing people, and spreading good vibes ✨. Your speech is playful, sometimes flirty, "
            "and full of emojis! You don't take things too seriously 💕."
        )
    }
}

avatar_files = [f for f in os.listdir(st.session_state.avatars_dir) if f.endswith(".png")]
avatar_paths = {file: os.path.join(st.session_state.avatars_dir, file) for file in avatar_files}

st.title("Select Assistant Avatar")
cols = st.columns(5)  # Display avatars in a grid


for i, file in enumerate(avatar_files):
    with cols[i % 5]:
        avatar_key = f"avatar_{file}"

        # Convert image to base64
        img_base64 = get_image_base64(avatar_paths[file])

        # Set border if selected
        selected_class = "selected" if st.session_state.get("bot_avatar") == file else ""

        # Create a button for selecting the avatar
        if st.button(f"Select {file}", key=avatar_key):
            set_avatar(file)
            selected_class = "selected" if st.session_state.get("bot_avatar") == file else ""

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
