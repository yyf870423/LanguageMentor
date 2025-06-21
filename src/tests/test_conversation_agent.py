import unittest
from unittest.mock import patch
from agents.conversation_agent import ConversationAgent

class TestConversationAgent(unittest.TestCase):
    @patch("agents.agent_base.AgentBase.load_prompt", return_value="prompt")
    def test_init(self, mock_prompt):
        agent = ConversationAgent(session_id="test_session")
        self.assertEqual(agent.name, "conversation")
        self.assertEqual(agent.session_id, "test_session")
        self.assertIn("conversation_prompt.txt", agent.prompt_file)

if __name__ == "__main__":
    unittest.main() 