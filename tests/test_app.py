# tests/test_app.py
import sys
import os

# Dodaj folder projektu na ścieżkę importów
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import streamlit as st
import base64
import importlib
import pytest

# Zresetuj i zainicjalizuj wymagane klucze w session_state
st.session_state.clear()
st.session_state['avatars_dir'] = os.path.join(os.path.dirname(__file__), os.pardir, 'avatars')

# Import modułów do testów avatarów i chat
from pages import bot_avatar, user_avatar, chat

# ----------------------
# Tests for bot_avatar.py
# ----------------------
def test_bot_get_image_base64(tmp_path):
    file = tmp_path / "img.png"
    data = b"abc"
    file.write_bytes(data)

    result = bot_avatar.get_image_base64(str(file))
    assert result == base64.b64encode(data).decode()


def test_bot_set_avatar(monkeypatch):
    st.session_state.clear()
    st.session_state['avatars_dir'] = 'avatars'
    importlib.reload(bot_avatar)

    bot_avatar.set_avatar("me.png")
    assert st.session_state.bot_avatar == "me.png"


def test_bot_avatar_files_and_paths(tmp_path):
    avatars_dir = tmp_path
    for name in ["a.png","b.png","c.txt"]:
        (avatars_dir/name).write_bytes(b"x")

    st.session_state.clear()
    st.session_state['avatars_dir'] = str(avatars_dir)
    importlib.reload(bot_avatar)

    assert sorted(bot_avatar.avatar_files) == ["a.png","b.png"]
    for f in bot_avatar.avatar_files:
        assert bot_avatar.avatar_paths[f] == os.path.join(str(avatars_dir), f)

# ----------------------
# Tests for user_avatar.py
# ----------------------
def test_user_get_image_base64(tmp_path):
    file = tmp_path / "img2.png"
    data = b"123"
    file.write_bytes(data)

    assert user_avatar.get_image_base64(str(file)) == base64.b64encode(data).decode()


def test_user_set_avatar():
    st.session_state.clear()
    st.session_state['avatars_dir'] = 'avatars'
    importlib.reload(user_avatar)

    user_avatar.set_avatar("you.png")
    assert st.session_state.user_avatar == "you.png"


def test_user_avatar_files_and_paths(tmp_path):
    avatars_dir = tmp_path
    for name in ["x.png","y.jpg","z.png"]:
        (avatars_dir/name).write_bytes(b"x")

    st.session_state.clear()
    st.session_state['avatars_dir'] = str(avatars_dir)
    importlib.reload(user_avatar)

    assert sorted(user_avatar.avatar_files) == ["x.png","z.png"]
    for f in user_avatar.avatar_files:
        assert user_avatar.avatar_paths[f] == os.path.join(str(avatars_dir), f)

# ----------------------
# Tests for chat.py
# ----------------------
class DummyOllama:
    def __init__(self):
        self.pulled_model = None
    def pull(self, model):
        self.pulled_model = model
    def chat(self, model, messages, stream):
        yield {'message': {'content': 'chunk1'}}
        yield {'message': {'content': 'chunk2'}}


def test_get_bot_response(monkeypatch):
    dummy = DummyOllama()
    monkeypatch.setattr(chat, 'ollama', dummy)

    history = [{'role':'user','content':'hi'}]
    gen = chat.get_bot_response(history)

    assert hasattr(gen, '__iter__')
    result = list(gen)
    assert result == [
        {'message': {'content': 'chunk1'}},
        {'message': {'content': 'chunk2'}}
    ]
    assert dummy.pulled_model == 'llama3.2'
