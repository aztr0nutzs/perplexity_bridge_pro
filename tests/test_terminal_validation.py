"""Tests for terminal command validation and other utility functions."""
import os
import pytest
from fastapi import HTTPException

# Set test environment
os.environ["BRIDGE_SECRET"] = "test-secret-key"
os.environ["PERPLEXITY_API_KEY"] = "test-api-key"

from app import _validate_terminal_command


class TestTerminalCommandValidation:
    """Tests for _validate_terminal_command function."""
    
    def test_valid_simple_command(self):
        """Test validation of simple valid command."""
        args = _validate_terminal_command("echo hello")
        assert args == ["echo", "hello"]
    
    def test_valid_command_with_multiple_args(self):
        """Test validation of command with multiple arguments."""
        args = _validate_terminal_command("ls -la src")
        assert args == ["ls", "-la", "src"]
    
    def test_empty_command(self):
        """Test validation fails for empty command."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("")
        assert exc_info.value.status_code == 400
        assert "empty" in exc_info.value.detail.lower()
    
    def test_whitespace_only_command(self):
        """Test validation fails for whitespace-only command."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("   ")
        assert exc_info.value.status_code == 400
    
    def test_command_too_long(self):
        """Test validation fails for command exceeding length limit."""
        long_command = "echo " + "a" * 200
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command(long_command)
        assert exc_info.value.status_code == 400
        assert "too long" in exc_info.value.detail.lower()
    
    def test_command_with_pipe(self):
        """Test validation fails for command with pipe operator."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("ls | grep test")
        assert exc_info.value.status_code == 400
        assert "shell operators" in exc_info.value.detail.lower()
    
    def test_command_with_ampersand(self):
        """Test validation fails for command with && operator."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("echo hello && echo world")
        assert exc_info.value.status_code == 400
    
    def test_command_with_semicolon(self):
        """Test validation fails for command with semicolon."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("echo hello; echo world")
        assert exc_info.value.status_code == 400
    
    def test_command_with_or_operator(self):
        """Test validation fails for command with || operator."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("echo hello || echo world")
        assert exc_info.value.status_code == 400
    
    def test_command_with_backticks(self):
        """Test validation fails for command with backticks."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("echo `whoami`")
        assert exc_info.value.status_code == 400
    
    def test_command_with_command_substitution(self):
        """Test validation fails for command with command substitution."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("echo $(whoami)")
        assert exc_info.value.status_code == 400
    
    def test_command_with_redirection_gt(self):
        """Test validation fails for command with > redirection."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("echo hello > file.txt")
        assert exc_info.value.status_code == 400
    
    def test_command_with_redirection_lt(self):
        """Test validation fails for command with < redirection."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("cat < file.txt")
        assert exc_info.value.status_code == 400
    
    def test_disallowed_command_rm(self):
        """Test validation fails for disallowed command rm."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("rm file.txt")
        assert exc_info.value.status_code == 400
        assert "not allowed" in exc_info.value.detail.lower()
    
    def test_disallowed_command_curl(self):
        """Test validation fails for disallowed command curl."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("curl http://example.com")
        assert exc_info.value.status_code == 400
    
    def test_disallowed_command_python(self):
        """Test validation fails for disallowed command python."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("python script.py")
        assert exc_info.value.status_code == 400
    
    def test_disallowed_command_bash(self):
        """Test validation fails for disallowed command bash."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("bash script.sh")
        assert exc_info.value.status_code == 400
    
    def test_allowed_command_echo(self):
        """Test validation passes for allowed command echo."""
        args = _validate_terminal_command("echo test")
        assert args[0] == "echo"
    
    def test_allowed_command_pwd(self):
        """Test validation passes for allowed command pwd."""
        args = _validate_terminal_command("pwd")
        assert args[0] == "pwd"
    
    def test_allowed_command_ls(self):
        """Test validation passes for allowed command ls."""
        args = _validate_terminal_command("ls -la")
        assert args[0] == "ls"
    
    def test_allowed_command_grep(self):
        """Test validation passes for allowed command grep."""
        args = _validate_terminal_command("grep pattern file.txt")
        assert args[0] == "grep"
    
    def test_allowed_command_cat(self):
        """Test validation passes for allowed command cat."""
        args = _validate_terminal_command("cat file.txt")
        assert args[0] == "cat"
    
    def test_allowed_command_head(self):
        """Test validation passes for allowed command head."""
        args = _validate_terminal_command("head -n 10 file.txt")
        assert args[0] == "head"
    
    def test_allowed_command_tail(self):
        """Test validation passes for allowed command tail."""
        args = _validate_terminal_command("tail -f log.txt")
        assert args[0] == "tail"
    
    def test_allowed_command_wc(self):
        """Test validation passes for allowed command wc."""
        args = _validate_terminal_command("wc -l file.txt")
        assert args[0] == "wc"
    
    def test_absolute_path_argument(self):
        """Test validation fails for absolute path argument."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("cat /etc/passwd")
        assert exc_info.value.status_code == 400
        assert "path" in exc_info.value.detail.lower()
    
    def test_home_directory_argument(self):
        """Test validation fails for home directory path argument."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("cat ~/file.txt")
        assert exc_info.value.status_code == 400
    
    def test_parent_directory_traversal(self):
        """Test validation fails for parent directory traversal."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("cat ../../../etc/passwd")
        assert exc_info.value.status_code == 400
    
    def test_windows_absolute_path(self):
        """Test validation fails for Windows absolute path."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("cat C:\\Windows\\System32\\file.txt")
        assert exc_info.value.status_code == 400
    
    def test_null_byte_in_argument(self):
        """Test validation fails for null byte in argument."""
        with pytest.raises(HTTPException) as exc_info:
            _validate_terminal_command("echo test\x00malicious")
        assert exc_info.value.status_code == 400
        assert "invalid" in exc_info.value.detail.lower()
    
    def test_relative_path_allowed(self):
        """Test validation passes for relative path."""
        args = _validate_terminal_command("cat file.txt")
        assert args == ["cat", "file.txt"]
    
    def test_subdirectory_path_allowed(self):
        """Test validation passes for subdirectory path."""
        args = _validate_terminal_command("cat src/main.py")
        assert args == ["cat", "src/main.py"]
    
    def test_hidden_file_allowed(self):
        """Test validation passes for hidden file (starts with dot but not ..)."""
        args = _validate_terminal_command("cat .gitignore")
        assert args == ["cat", ".gitignore"]
    
    def test_command_with_quotes(self):
        """Test validation handles quoted arguments."""
        args = _validate_terminal_command('echo "hello world"')
        assert len(args) == 2
        assert args[0] == "echo"
        assert args[1] == "hello world"
    
    def test_command_with_single_quotes(self):
        """Test validation handles single-quoted arguments."""
        args = _validate_terminal_command("echo 'hello world'")
        assert len(args) == 2
        assert args[1] == "hello world"
