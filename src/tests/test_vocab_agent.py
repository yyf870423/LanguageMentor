import unittest
from unittest.mock import patch, MagicMock
from agents.vocab_agent import VocabAgent

class TestVocabAgent(unittest.TestCase):
    @patch("agents.agent_base.AgentBase.load_prompt", return_value="prompt")
    def test_init(self, mock_prompt):
        agent = VocabAgent(session_id="sid")
        self.assertEqual(agent.name, "vocab_study")
        self.assertEqual(agent.session_id, "sid")

    @patch("agents.vocab_agent.get_session_history")
    @patch("agents.agent_base.AgentBase.load_prompt", return_value="prompt")
    def test_restart_session(self, mock_prompt, mock_history):
        agent = VocabAgent(session_id="sid")
        mock_history.return_value.clear = MagicMock()
        mock_history.return_value.__str__ = lambda s: "history_obj"
        result = agent.restart_session(session_id="sid")
        self.assertEqual(result, mock_history.return_value)
        mock_history.return_value.clear.assert_called_once()

if __name__ == "__main__":
    unittest.main() 