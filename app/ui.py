import gradio as gr

from app.sensors.env_monitor import EnvironmentMonitor
from app.vision.fall_detector import FallDetector
from app.storage.db import (
    init_db,
    insert_env_record,
    get_recent_env_records,
    insert_reminder,
    get_reminders,
)

env_monitor = EnvironmentMonitor(simulation=True)
fall_detector = FallDetector()
init_db()

def check_environment():
    record = env_monitor.read()
    alert = env_monitor.analyze(record)
    insert_env_record(record, alert)
    return (
        record["temperature"],
        record["humidity"],
        record["smoke"],
        record["gas"],
        alert,
    )

def show_env_history():
    return get_recent_env_records()

def run_fall_detection():
    result = fall_detector.detect_from_simulated_keypoints()
    return result["risk_level"], result["score"], result["reason"]

def add_reminder(title, time_text):
    if not title.strip() or not time_text.strip():
        return get_reminders()
    insert_reminder(title.strip(), time_text.strip())
    return get_reminders()

def chat(user_input, history):
    if history is None:
        history = []
    if not user_input.strip():
        return "", history
    response = "已记录。本项目演示对话陪伴、环境监测、跌倒风险判断和提醒管理流程。"
    history.append((user_input, response))
    return "", history

def build_app():
    with gr.Blocks(title="Elderly Companion Edge System") as demo:
        gr.Markdown("# Elderly Companion Edge System")
        gr.Markdown(
            "基于树莓派的智能老人陪伴与跌倒风险监测系统。"
            "当前 GitHub 展示版默认使用模拟模式，可以在普通电脑上运行。"
        )

        with gr.Tab("Dialogue Companion"):
            chatbot = gr.Chatbot(label="Dialogue History")
            user_input = gr.Textbox(
                label="User Input",
                placeholder="例如：提醒我晚上8点吃药",
            )
            send_btn = gr.Button("Send")
            send_btn.click(chat, inputs=[user_input, chatbot], outputs=[user_input, chatbot])

        with gr.Tab("Environment Monitoring"):
            gr.Markdown("Simulated DHT22 / MQ-2 / MQ-5 sensor values")
            check_btn = gr.Button("Check Environment")
            temperature = gr.Number(label="Temperature")
            humidity = gr.Number(label="Humidity")
            smoke = gr.Number(label="Smoke Level")
            gas = gr.Number(label="Gas Level")
            alert = gr.Textbox(label="Alert")
            check_btn.click(
                check_environment,
                outputs=[temperature, humidity, smoke, gas, alert],
            )

            history_btn = gr.Button("Show Recent Records")
            env_table = gr.Dataframe(label="Recent Environment Records")
            history_btn.click(show_env_history, outputs=env_table)

        with gr.Tab("Fall-Risk Detection"):
            gr.Markdown("The public demo version uses simulated body keypoints.")
            fall_btn = gr.Button("Run Fall-Risk Detection")
            risk_level = gr.Textbox(label="Risk Level")
            score = gr.Number(label="Risk Score")
            reason = gr.Textbox(label="Reason")
            fall_btn.click(run_fall_detection, outputs=[risk_level, score, reason])

        with gr.Tab("Reminder Management"):
            title = gr.Textbox(label="Reminder Title", placeholder="例如：吃药 / 喝水 / 休息")
            time_text = gr.Textbox(label="Time", placeholder="例如：20:00")
            add_btn = gr.Button("Add Reminder")
            reminder_table = gr.Dataframe(label="Reminder List")
            add_btn.click(add_reminder, inputs=[title, time_text], outputs=reminder_table)

    return demo
