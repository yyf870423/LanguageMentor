# tabs/conversation_tab.py

import gradio as gr
from agents.conversation_agent import ConversationAgent
from utils.logger import LOG

# 初始化对话代理
conversation_agent = ConversationAgent()

def handle_conversation(user_input, chat_history):
    bot_message = conversation_agent.chat_with_history(user_input)
    LOG.info(f"[Conversation ChatBot]: {bot_message}")
    return {"role": "assistant", "content": bot_message}

def create_conversation_tab():
    with gr.Tab("对话"):
        gr.Markdown("## 练习英语对话 ")  # 对话练习说明
        conversation_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>想和我聊什么话题都可以，记得用英语哦！",  # 聊天机器人的占位符
            height=800,  # 聊天窗口高度
            type="messages",
        )

        # 处理用户对话的函数
        def handle_retry(history, retry_data: gr.RetryData):
            return history
        def handle_undo(history, undo_data: gr.UndoData):
            return history
        def handle_clear():
            return []
        conversation_chatbot.retry(handle_retry, conversation_chatbot, conversation_chatbot)
        conversation_chatbot.undo(handle_undo, conversation_chatbot, conversation_chatbot)
        conversation_chatbot.clear(handle_clear, outputs=conversation_chatbot)
        gr.ChatInterface(
            fn=handle_conversation,  # 处理对话的函数
            chatbot=conversation_chatbot,  # 聊天机器人组件
            submit_btn="发送",  # 发送按钮文本
            type="messages",
        )