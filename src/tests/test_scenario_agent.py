import unittest
from unittest.mock import patch, MagicMock
from agents.scenario_agent import ScenarioAgent

class TestScenarioAgent(unittest.TestCase):
    @patch("agents.agent_base.AgentBase.load_prompt", return_value="prompt")
    @patch("agents.agent_base.AgentBase.load_intro", return_value=["hi1", "hi2"])
    def test_init(self, mock_intro, mock_prompt):
        agent = ScenarioAgent("hotel_checkin", session_id="sid")
        self.assertEqual(agent.name, "hotel_checkin")
        self.assertEqual(agent.session_id, "sid")
        self.assertEqual(agent.intro_messages, ["hi1", "hi2"])

    @patch("agents.scenario_agent.get_session_history")
    @patch("agents.agent_base.AgentBase.load_prompt", return_value="prompt")
    @patch("agents.agent_base.AgentBase.load_intro", return_value=["hi1", "hi2"])
    def test_start_new_session(self, mock_intro, mock_prompt, mock_history):
        agent = ScenarioAgent("hotel_checkin", session_id="sid")
        # history with no messages
        mock_history.return_value.messages = []
        mock_history.return_value.add_message = MagicMock()
        msg = agent.start_new_session(session_id="sid")
        self.assertIn(msg, ["hi1", "hi2"])
        # history with messages
        mock_history.return_value.messages = [MagicMock(content="last")] 
        msg2 = agent.start_new_session(session_id="sid")
        self.assertEqual(msg2, "last")

if __name__ == "__main__":
    unittest.main() 