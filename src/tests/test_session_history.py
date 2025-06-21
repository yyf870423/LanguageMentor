import unittest
from agents import session_history

class TestSessionHistory(unittest.TestCase):
    def test_get_session_history_new_and_reuse(self):
        sid = "test1"
        # 新建
        hist1 = session_history.get_session_history(sid)
        self.assertIsNotNone(hist1)
        # 复用
        hist2 = session_history.get_session_history(sid)
        self.assertIs(hist1, hist2)
        # 新 id
        sid2 = "test2"
        hist3 = session_history.get_session_history(sid2)
        self.assertIsNot(hist1, hist3)

if __name__ == "__main__":
    unittest.main() 