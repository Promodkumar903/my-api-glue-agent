import  os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "nvidia/nemotron-3-super-120b-a12b:free")

@app.route("/")
def home():
    return "API Glue Agent is running! Use /scan endpoint to find gaps."

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    tools = data.get("tools", "")
    prompt = f"Find data gaps between these tools: {tools}. List each gap and suggest a fix workflow."
    
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 4000
        }
    )
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
