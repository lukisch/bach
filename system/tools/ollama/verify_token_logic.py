# SPDX-License-Identifier: MIT
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Pfade setzen
BACH_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BACH_ROOT / "tools"))
sys.path.insert(0, str(BACH_ROOT / "tools" / "ollama"))

from ollama_client import OllamaResponse
import token_monitor

class TestOllamaTokenAware(unittest.TestCase):
    def test_response_tokens(self):
        resp = OllamaResponse(
            success=True, 
            text="Hello world", 
            prompt_tokens=10, 
            completion_tokens=5
        )
        self.assertEqual(resp.total_tokens, 15)
        
    @patch('sqlite3.connect')
    def test_logging(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        success = token_monitor.log_ollama_usage(20, 10, "test_session")
        self.assertTrue(success)
        
        # Pruefe ob INSERT aufgerufen wurde
        # Wir schauen uns alle Aufrufe von execute auf dem Cursor an
        calls = [args[0] for args, kwargs in mock_cursor.execute.call_args_list]
        self.assertTrue(any("INSERT INTO monitor_tokens" in c for c in calls))

if __name__ == "__main__":
    unittest.main()
