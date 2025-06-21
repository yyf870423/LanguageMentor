import gradio as gr  # 导入 Gradio 库，用于构建用户界面
from agents.conversation_agent import ConversationAgent  # 导入对话代理类
from agents.scenario_agent import ScenarioAgent  # 导入场景代理类
from utils.logger import LOG  # 导入日志记录工具
import random
import json

# 创建对话代理实例
conversation_agent = ConversationAgent()

# 定义场景代理的选择与调用
agents = {
    "job_interview": ScenarioAgent("job_interview"),  # 求职面试场景代理
    "hotel_checkin": ScenarioAgent("hotel_checkin"),  # 酒店入住场景代理
    "salary_negotiation": ScenarioAgent("salary_negotiation"),  # 薪资谈判场景代理
    "bmw_sales": ScenarioAgent("bmw_sales"),  # 汽车选购场景代理
    # "renting": ScenarioAgent("renting")  # 租房场景代理（注释掉）
}

# 处理用户对话的函数
def handle_conversation(user_input, chat_history):
    bot_message = conversation_agent.chat_with_history(user_input)
    LOG.info(f"[ChatBot]: {bot_message}")
    chat_history = chat_history or []
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": bot_message})
    return chat_history

# 获取场景介绍的函数
def get_scenario_intro(scenario):
    with open(f"content/page/{scenario}.md", "r", encoding="utf-8") as file:  # 打开对应场景的介绍文件
        scenario_intro = file.read().strip()  # 读取文件内容并去除多余空白
    return scenario_intro  # 返回场景介绍内容

# 场景代理处理函数，根据选择的场景调用相应的代理
def handle_scenario(user_input, chat_history, scenario):
    bot_message = agents[scenario].chat_with_history(user_input)
    LOG.info(f"[ChatBot]: {bot_message}")
    chat_history = chat_history or []
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": bot_message})
    return chat_history

def get_intro_message(scenario):
    with open(f"content/intro/{scenario}.json", "r", encoding="utf-8") as f:
        messages = json.load(f)
    return random.choice(messages)

# Gradio 界面构建
with gr.Blocks(title="LanguageMentor 英语私教") as language_mentor_app:
    with gr.Tab("场景训练"):  # 场景训练标签
        gr.Markdown("## 选择一个场景完成目标和挑战")  # 场景选择说明

        # 创建单选框组件
        scenario_radio = gr.Radio(
            choices=[
                ("求职面试", "job_interview"),  # 求职面试选项
                ("酒店入住", "hotel_checkin"),  # 酒店入住选项
                ("薪资谈判", "salary_negotiation"),  # 薪资谈判选项
                ("汽车选购", "bmw_sales"),  # 汽车选购选项
                # ("租房", "renting")  # 租房选项（注释掉）
            ], 
            label="场景"  # 单选框标签
        )

        scenario_intro = gr.Markdown()  # 场景介绍文本组件
        scenario_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>选择场景后开始对话吧！",
            height=600,
            type='messages'
        )
        scenario_msg = gr.Textbox(placeholder="请输入你想说的话...", label="输入")
        with gr.Row():
            scenario_send_btn = gr.Button("发送")
            scenario_retry_btn = gr.Button("重试")
            scenario_undo_btn = gr.Button("撤销")
            scenario_clear_btn = gr.Button("清除历史记录")
        scenario_history = gr.State([])

        def scenario_send(user_input, history, scenario):
            bot_message = agents[scenario].chat_with_history(user_input)
            history = history or []
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": bot_message})
            return history, "", history

        def scenario_retry(history, scenario):
            if not history or history[-1]["role"] != "user":
                return history, history
            last_user_input = history[-1]["content"]
            bot_message = agents[scenario].chat_with_history(last_user_input)
            if history and history[-1]["role"] == "assistant":
                history = history[:-1]
            history.append({"role": "assistant", "content": bot_message})
            return history, history

        def scenario_undo(history):
            if len(history) >= 2:
                history = history[:-2]
            return history, history

        def scenario_clear():
            return [], []

        scenario_send_btn.click(scenario_send, [scenario_msg, scenario_history, scenario_radio], [scenario_chatbot, scenario_msg, scenario_history])
        scenario_msg.submit(scenario_send, [scenario_msg, scenario_history, scenario_radio], [scenario_chatbot, scenario_msg, scenario_history])
        scenario_retry_btn.click(scenario_retry, [scenario_history, scenario_radio], [scenario_chatbot, scenario_history])
        scenario_undo_btn.click(scenario_undo, scenario_history, [scenario_chatbot, scenario_history])
        scenario_clear_btn.click(scenario_clear, None, [scenario_chatbot, scenario_history])

        def update_scenario_on_change(scenario):
            intro = get_scenario_intro(scenario)
            intro_message = get_intro_message(scenario)
            history = [{"role": "assistant", "content": intro_message}]
            return intro, history, history
        scenario_radio.change(update_scenario_on_change, scenario_radio, [scenario_intro, scenario_chatbot, scenario_history])

    with gr.Tab("对话练习"):  # 对话练习标签
        gr.Markdown("## 练习英语对话 ")  # 对话练习说明
        conversation_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>想和我聊什么话题都可以，记得用英语哦！",
            height=800,
            type='messages'
        )
        conversation_msg = gr.Textbox(placeholder="请输入你想说的话...", label="输入")
        with gr.Row():
            conversation_send_btn = gr.Button("发送")
            conversation_retry_btn = gr.Button("重试")
            conversation_undo_btn = gr.Button("撤销")
            conversation_clear_btn = gr.Button("清除历史记录")
        conversation_history = gr.State([])

        def conversation_send(user_input, history):
            bot_message = conversation_agent.chat_with_history(user_input)
            history = history or []
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": bot_message})
            return history, "", history

        def conversation_retry(history):
            if not history or history[-1]["role"] != "user":
                return history, history
            last_user_input = history[-1]["content"]
            bot_message = conversation_agent.chat_with_history(last_user_input)
            if history and history[-1]["role"] == "assistant":
                history = history[:-1]
            history.append({"role": "assistant", "content": bot_message})
            return history, history

        def conversation_undo(history):
            if len(history) >= 2:
                history = history[:-2]
            return history, history

        def conversation_clear():
            return [], []

        conversation_send_btn.click(conversation_send, [conversation_msg, conversation_history], [conversation_chatbot, conversation_msg, conversation_history])
        conversation_msg.submit(conversation_send, [conversation_msg, conversation_history], [conversation_chatbot, conversation_msg, conversation_history])
        conversation_retry_btn.click(conversation_retry, conversation_history, [conversation_chatbot, conversation_history])
        conversation_undo_btn.click(conversation_undo, conversation_history, [conversation_chatbot, conversation_history])
        conversation_clear_btn.click(conversation_clear, None, [conversation_chatbot, conversation_history])

# 启动应用
if __name__ == "__main__":
    language_mentor_app.launch(share=True, server_name="0.0.0.0")  # 启动 Gradio 应用并共享