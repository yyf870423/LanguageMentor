import unittest
from unittest.mock import patch, MagicMock
from agents.agent_base import AgentBase

class DummyAgent(AgentBase):
    def __init__(self, **kwargs):
        super().__init__(name="dummy", prompt_file="dummy_prompt.txt", intro_file="dummy_intro.json", **kwargs)

class TestAgentBase(unittest.TestCase):
    @patch.object(AgentBase, "load_intro", return_value=["hello"])
    @patch.object(AgentBase, "load_prompt", return_value="system prompt")
    def test_load_prompt(self, mock_prompt, mock_intro):
        agent = DummyAgent()
        self.assertEqual(agent.prompt, "system prompt")

    @patch.object(AgentBase, "load_intro", return_value=["hello"])
    @patch.object(AgentBase, "load_prompt", return_value="system prompt")
    def test_load_intro(self, mock_prompt, mock_intro):
        agent = DummyAgent()
        self.assertEqual(agent.intro_messages, ["hello"])

    @patch("agents.agent_base.ChatOpenAI")
    @patch("agents.agent_base.ChatPromptTemplate.from_messages")
    @patch.object(AgentBase, "load_intro", return_value=["hello"])
    @patch.object(AgentBase, "load_prompt", return_value="system prompt")
    def test_create_chatbot(self, mock_prompt, mock_intro, mock_template, mock_chat):
        agent = DummyAgent()
        self.assertTrue(hasattr(agent, "chatbot"))
        self.assertTrue(hasattr(agent, "chatbot_with_history"))

    @patch("agents.agent_base.RunnableWithMessageHistory")
    @patch("agents.agent_base.ChatOpenAI")
    @patch("agents.agent_base.ChatPromptTemplate.from_messages")
    @patch.object(AgentBase, "load_intro", return_value=["hello"])
    @patch.object(AgentBase, "load_prompt", return_value="system prompt")
    def test_chat_with_history(self, mock_prompt, mock_intro, mock_template, mock_chat, mock_runnable):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value.content = "response"
        mock_runnable.return_value = mock_instance
        agent = DummyAgent()
        result = agent.chat_with_history("hi", session_id="test")
        self.assertEqual(result, "response")

if __name__ == "__main__":
    unittest.main() 