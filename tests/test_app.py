import pytest
import base64
from unittest import mock

import HomePage
from pages import bot_avatar, user_avatar, chat

### Tests for HomePage.py ###

def test_get_base64_img(tmp_path):
    """
    Test if get_base64_img correctly converts an image file to a base64 HTML <img> tag.
    """
    # Create a temporary fake image file
    img_path = tmp_path / "test.png"
    img_path.write_bytes(b"fake_image_data")

    # Call the function
    result = HomePage.get_base64_img(str(img_path), width=100)

    # Assert that the result is a valid HTML image tag with base64 data
    assert result.startswith("<img src='data:image/png;base64,")
    assert "width='100px'" in result


def test_set_background_image(tmp_path):
    """
    Test if set_background_image generates a background style and calls Streamlit's markdown.
    """
    # Create a temporary fake image file
    img_path = tmp_path / "background.jpg"
    img_path.write_bytes(b"fake_image_data")

    # Mock Streamlit's markdown function
    with mock.patch("streamlit.markdown") as mock_markdown:
        HomePage.set_background_image(str(img_path))

        # Check that markdown was called once with expected content
        mock_markdown.assert_called_once()
        assert "background" in mock_markdown.call_args[0][0]


### Tests for bot_avatar.py and user_avatar.py ###

@pytest.mark.parametrize("module", [bot_avatar, user_avatar])
def test_get_image_base64(module, tmp_path):
    """
    Test if get_image_base64 correctly encodes image files to base64 strings.
    This test is applied to both bot_avatar.py and user_avatar.py modules.
    """
    # Create a temporary fake image file
    img_path = tmp_path / "avatar.png"
    img_path.write_bytes(b"test_image_data")

    # Call the function
    encoded = module.get_image_base64(str(img_path))

    # Assert that the output is a correct base64 encoded string
    assert isinstance(encoded, str)
    assert base64.b64encode(b"test_image_data").decode() == encoded


@pytest.mark.parametrize("module, key", [
    (bot_avatar, "bot_avatar"),
    (user_avatar, "user_avatar")
])
def test_set_avatar(module, key):
    """
    Test if set_avatar correctly updates Streamlit's session_state with the selected avatar.
    This test covers both bot and user avatar modules.
    """
    with mock.patch.dict("streamlit.session_state", {}, clear=True):
        module.set_avatar("test_avatar.png")

        # Check if the avatar key is set correctly in session_state
        assert key in mock.patch.dict
        assert mock.patch.dict["streamlit.session_state"][key] == "test_avatar.png"


### Tests for chat.py ###

def test_get_bot_response():
    """
    Test if get_bot_response calls ollama.chat with correct parameters and returns the response.
    The ollama.chat function is mocked to avoid external dependencies.
    """
    fake_history = [{"role": "user", "content": "Hello"}]

    # Simulate a fake streaming response
    fake_response = [{"message": {"content": "Hi there!"}}, {"message": {"content": " How can I help?"}}]

    with mock.patch("chat.ollama.chat", return_value=fake_response) as mock_ollama:
        response = chat.get_bot_response(fake_history)

        # Verify that ollama.chat was called correctly
        mock_ollama.assert_called_once_with(model='llama3.2', messages=fake_history, stream=True)

        # Check if the response matches the mocked return value
        assert response == fake_response
