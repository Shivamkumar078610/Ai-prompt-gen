import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

print("🚀 SERVER STARTING...")

app = Flask(__name__)
CORS(app)

# ✅ Get API Key safely
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("❌ ERROR: OPENAI_API_KEY missing")

client = OpenAI(api_key=api_key)

# ✅ Home route
@app.route("/")
def home():
    return jsonify({"message": "API is running 🚀"})

# 🔹 Text → Prompt
def generate_text_prompt(concept, mode):
    if mode == "image":
        system_msg = "Create a highly detailed AI image prompt with cinematic lighting, camera angle, style and negative prompts."
    else:
        system_msg = "Create a cinematic AI video prompt with camera movement, lighting, motion and atmosphere."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": concept}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


# 🔥 MAIN API
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json

        mode = data.get("mode")
        concept = data.get("concept")

        if not concept:
            return jsonify({"error": "Concept required"}), 400

        result = generate_text_prompt(concept, mode)

        return jsonify({"prompt": result})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)}), 500


# 🔥 IMPORTANT FOR GUNICORN
application = app