"""Tests for ${project_name} core functionality."""

import pytest


class TestCore:
    """Core tests."""
    
    def test_import(self):
        """Test that package can be imported."""
        import ${project_name}
        assert ${project_name}.__version__ == "0.1.0"
    
    def test_cli_version(self):
        """Test CLI version flag."""
        from ${project_name}.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(["--version"])
        assert exc_info.value.code == 0
    
    def test_cli_help(self):
        """Test CLI help flag."""
        from ${project_name}.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(["--help"])
        assert exc_info.value.code == 0
