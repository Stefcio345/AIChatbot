import base64
import pytest
import os
import importlib

# Import modules under test
import app
from pages import bot_avatar, chat, user_avatar

# ----------------------
# Tests for app.py
# ----------------------
def test_get_base64_img(tmp_path):
    # Create a dummy image file
    file_path = tmp_path / "test.png"
    data = b"hello world"
    file_path.write_bytes(data)

    html = app.get_base64_img(str(file_path), width=42)

    # Verify HTML img tag formation
    assert html.startswith("<img src='data:image/png;base64,")
    assert "width='42px'" in html

    # Ensure base64-encoded data is present
    expected = base64.b64encode(data).decode()
    assert expected in html


def test_set_background_image(tmp_path, monkeypatch):
    # Prepare a dummy background image
    file_path = tmp_path / "bg.png"
    data = b"background"
    file_path.write_bytes(data)

    # Capture markdown call
    calls = {}
    def fake_markdown(arg, unsafe_allow_html):
        calls['arg'] = arg
        calls['unsafe'] = unsafe_allow_html
    monkeypatch.setattr(app.st, 'markdown', fake_markdown)

    # Call under test
    app.set_background_image(str(file_path))

    # Assertions
    assert calls.get('unsafe') is True
    assert 'background-image' in calls.get('arg', '')
    assert base64.b64encode(data).decode() in calls['arg']

# ----------------------
# Tests for bot_avatar.py
# ----------------------
def test_bot_get_image_base64(tmp_path):
    file = tmp_path / "test.png"
    data = b"abc"
    file.write_bytes(data)

    result = bot_avatar.get_image_base64(str(file))
    assert result == base64.b64encode(data).decode()


def test_bot_set_avatar(monkeypatch):
    import streamlit as st
    # Reset session_state
    st.session_state.clear()

    bot_avatar.set_avatar("avatar1.png")
    assert st.session_state.bot_avatar == "avatar1.png"


def test_bot_avatar_files_and_paths(tmp_path, monkeypatch):
    # Create dummy avatars directory
    avatars_dir = tmp_path
    files = ["a.png", "b.png", "c.txt"]
    for name in files:
        (avatars_dir / name).write_bytes(b"x")

    import streamlit as st
    st.session_state.avatars_dir = str(avatars_dir)

    # Reload module to pick up new directory
    importlib.reload(bot_avatar)

    expected = ["a.png", "b.png"]
    assert sorted(bot_avatar.avatar_files) == expected
    for f in expected:
        assert bot_avatar.avatar_paths[f] == os.path.join(str(avatars_dir), f)

# ----------------------
# Tests for user_avatar.py
# ----------------------
def test_user_get_image_base64(tmp_path):
    file = tmp_path / "test2.png"
    data = b"123"
    file.write_bytes(data)

    result = user_avatar.get_image_base64(str(file))
    assert result == base64.b64encode(data).decode()


def test_user_set_avatar(monkeypatch):
    import streamlit as st
    st.session_state.clear()

    user_avatar.set_avatar("u.png")
    assert st.session_state.user_avatar == "u.png"


def test_user_avatar_files_and_paths(tmp_path, monkeypatch):
    avatars_dir = tmp_path
    names = ["x.png", "y.jpg", "z.png"]
    for n in names:
        (avatars_dir / n).write_bytes(b"x")

    import streamlit as st
    st.session_state.avatars_dir = str(avatars_dir)

    importlib.reload(user_avatar)

    expected = ["x.png", "z.png"]
    assert sorted(user_avatar.avatar_files) == expected
    for f in expected:
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

    history = [{'role': 'user', 'content': 'hi'}]
    response_gen = chat.get_bot_response(history)

    assert hasattr(response_gen, '__iter__')

    result = list(response_gen)
    assert result == [
        {'message': {'content': 'chunk1'}},
        {'message': {'content': 'chunk2'}}
    ]
    assert dummy.pulled_model == 'llama3.2'
