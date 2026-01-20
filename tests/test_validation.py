"""Tests for request validation with Pydantic models."""
import os
import pytest
from pydantic import ValidationError

# Set test environment before importing app
os.environ["BRIDGE_SECRET"] = "test-secret-key"
os.environ["PERPLEXITY_API_KEY"] = "test-api-key"

from app import Message, ChatReq


class TestMessageValidation:
    """Tests for Message model validation."""

    def test_valid_message(self):
        """Test valid message creation."""
        msg = Message(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"

    def test_valid_roles(self):
        """Test all valid roles are accepted."""
        valid_roles = ["user", "assistant", "system"]
        for role in valid_roles:
            msg = Message(role=role, content="test")
            assert msg.role == role

    def test_invalid_role(self):
        """Test invalid role is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Message(role="invalid", content="test")
        assert "Role must be one of" in str(exc_info.value)

    def test_empty_content(self):
        """Test empty content is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Message(role="user", content="")
        assert "Content cannot be empty" in str(exc_info.value)

    def test_whitespace_only_content(self):
        """Test whitespace-only content is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Message(role="user", content="   ")
        assert "Content cannot be empty" in str(exc_info.value)

    def test_content_trimming(self):
        """Test content is trimmed of leading/trailing whitespace."""
        msg = Message(role="user", content="  Hello  ")
        assert msg.content == "Hello"

    def test_missing_role(self):
        """Test missing role field is rejected."""
        with pytest.raises(ValidationError):
            Message(content="test")

    def test_missing_content(self):
        """Test missing content field is rejected."""
        with pytest.raises(ValidationError):
            Message(role="user")


class TestChatReqValidation:
    """Tests for ChatReq model validation."""

    def test_valid_chat_request(self):
        """Test valid chat request creation."""
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="Hello")]
        )
        assert req.model == "gpt-5.2"
        assert len(req.messages) == 1
        assert req.stream is False
        assert req.max_tokens == 1024
        assert req.temperature == 0.0

    def test_empty_model_name(self):
        """Test empty model name is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ChatReq(
                model="",
                messages=[Message(role="user", content="test")]
            )
        assert "Model name cannot be empty" in str(exc_info.value)

    def test_whitespace_only_model_name(self):
        """Test whitespace-only model name is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ChatReq(
                model="   ",
                messages=[Message(role="user", content="test")]
            )
        assert "Model name cannot be empty" in str(exc_info.value)

    def test_model_name_trimming(self):
        """Test model name is trimmed."""
        req = ChatReq(
            model="  gpt-5.2  ",
            messages=[Message(role="user", content="test")]
        )
        assert req.model == "gpt-5.2"

    def test_empty_messages_list(self):
        """Test empty messages list is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ChatReq(model="gpt-5.2", messages=[])
        # Verify it's a ValidationError for the messages field
        assert exc_info.type == ValidationError
        assert "messages" in str(exc_info.value)

    def test_too_many_messages(self):
        """Test more than 100 messages is rejected."""
        messages = [Message(role="user", content=f"msg {i}") for i in range(101)]
        with pytest.raises(ValidationError) as exc_info:
            ChatReq(model="gpt-5.2", messages=messages)
        assert "Maximum 100 messages allowed" in str(exc_info.value)

    def test_max_messages_allowed(self):
        """Test exactly 100 messages is allowed."""
        messages = [Message(role="user", content=f"msg {i}") for i in range(100)]
        req = ChatReq(model="gpt-5.2", messages=messages)
        assert len(req.messages) == 100

    def test_max_tokens_validation(self):
        """Test max_tokens must be within valid range."""
        # Too low
        with pytest.raises(ValidationError):
            ChatReq(
                model="gpt-5.2",
                messages=[Message(role="user", content="test")],
                max_tokens=0
            )

        # Too high
        with pytest.raises(ValidationError):
            ChatReq(
                model="gpt-5.2",
                messages=[Message(role="user", content="test")],
                max_tokens=5000
            )

        # Valid range
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="test")],
            max_tokens=2048
        )
        assert req.max_tokens == 2048

    def test_temperature_validation(self):
        """Test temperature must be within valid range."""
        # Too low
        with pytest.raises(ValidationError):
            ChatReq(
                model="gpt-5.2",
                messages=[Message(role="user", content="test")],
                temperature=-0.1
            )

        # Too high
        with pytest.raises(ValidationError):
            ChatReq(
                model="gpt-5.2",
                messages=[Message(role="user", content="test")],
                temperature=2.1
            )

        # Valid range
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="test")],
            temperature=0.7
        )
        assert req.temperature == 0.7

    def test_frequency_penalty_validation(self):
        """Test frequency_penalty must be within valid range."""
        # Too low
        with pytest.raises(ValidationError):
            ChatReq(
                model="gpt-5.2",
                messages=[Message(role="user", content="test")],
                frequency_penalty=-2.1
            )

        # Too high
        with pytest.raises(ValidationError):
            ChatReq(
                model="gpt-5.2",
                messages=[Message(role="user", content="test")],
                frequency_penalty=2.1
            )

        # Valid range
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="test")],
            frequency_penalty=0.5
        )
        assert req.frequency_penalty == 0.5

    def test_stream_flag(self):
        """Test stream flag can be set."""
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="test")],
            stream=True
        )
        assert req.stream is True

    def test_optional_tools_parameter(self):
        """Test optional tools parameter."""
        # Without tools
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="test")]
        )
        assert req.tools is None

        # With tools
        tools = [{"type": "function", "function": {"name": "test"}}]
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="test")],
            tools=tools
        )
        assert req.tools == tools

    def test_default_values(self):
        """Test default values are set correctly."""
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="test")]
        )
        assert req.stream is False
        assert req.max_tokens == 1024
        assert req.temperature == 0.0
        assert req.frequency_penalty == 1
        assert req.tools is None

    def test_multiple_messages(self):
        """Test multiple messages in conversation."""
        messages = [
            Message(role="system", content="You are helpful"),
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there"),
            Message(role="user", content="How are you?")
        ]
        req = ChatReq(model="gpt-5.2", messages=messages)
        assert len(req.messages) == 4
        assert req.messages[0].role == "system"
        assert req.messages[-1].role == "user"


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_unicode_content(self):
        """Test unicode content is handled correctly."""
        msg = Message(role="user", content="Hello 世界 🌍")
        assert msg.content == "Hello 世界 🌍"

    def test_long_content(self):
        """Test very long content is accepted."""
        long_content = "x" * 10000
        msg = Message(role="user", content=long_content)
        assert len(msg.content) == 10000

    def test_special_characters_in_model(self):
        """Test model names with special characters."""
        req = ChatReq(
            model="llama-3.1-sonar-small-128k-online",
            messages=[Message(role="user", content="test")]
        )
        assert req.model == "llama-3.1-sonar-small-128k-online"

    def test_minimum_max_tokens(self):
        """Test minimum value for max_tokens."""
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="test")],
            max_tokens=1
        )
        assert req.max_tokens == 1

    def test_maximum_max_tokens(self):
        """Test maximum value for max_tokens."""
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="test")],
            max_tokens=4096
        )
        assert req.max_tokens == 4096

    def test_zero_temperature(self):
        """Test zero temperature (deterministic)."""
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="test")],
            temperature=0.0
        )
        assert req.temperature == 0.0

    def test_max_temperature(self):
        """Test maximum temperature."""
        req = ChatReq(
            model="gpt-5.2",
            messages=[Message(role="user", content="test")],
            temperature=2.0
        )
        assert req.temperature == 2.0
