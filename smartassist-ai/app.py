from flask import Flask, render_template, request, jsonify, send_file
from groq import Groq
from fpdf import FPDF
import json
import os

app = Flask(__name__)

client = Groq(
    api_key="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"
)

conversation = []

SYSTEM_PROMPTS = {
    "General": "You are a helpful AI assistant.",
    "Coding": "You are an expert software engineer.",
    "Study": "You are a friendly tutor helping students learn.",
    "Resume": "You are a professional resume reviewer."
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    user_message = data["message"]
    mode = data["mode"]

    conversation.append({
        "role": "user",
        "content": user_message
    })

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPTS[mode]
        }
    ] + conversation

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    bot_reply = response.choices[0].message.content

    conversation.append({
        "role": "assistant",
        "content": bot_reply
    })

    with open("chat_history.json", "w") as f:
        json.dump(conversation, f, indent=4)

    return jsonify({
        "reply": bot_reply
    })

@app.route("/summarize", methods=["POST"])
def summarize():

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Summarize this conversation briefly."
            },
            {
                "role": "user",
                "content": str(conversation)
            }
        ]
    )

    return jsonify({
        "summary": response.choices[0].message.content
    })

@app.route("/export")
def export_pdf():

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    for msg in conversation:
        pdf.multi_cell(
            0,
            10,
            f"{msg['role']} : {msg['content']}"
        )

    filename = "chat_export.pdf"
    pdf.output(filename)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)