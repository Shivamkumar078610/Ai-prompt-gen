import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

print("🚀 SERVER STARTING...")

app = Flask(__name__)

# ✅ FIXED CORS (important)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔐 Put your real OpenAI API key here
client = OpenAI(api_key="https://github.com/Shivamkumar078610/seo-api.git")

# ✅ Home route
@app.route('/')
def home():
    return jsonify({"message": "API is running 🚀"})

# 🔹 TEXT → PROMPT
def generate_text_prompt(concept, mode):
    if mode == 'image':
        system_msg = "Create a detailed cinematic AI image prompt with lighting, angle, style, colors and negative prompts."
    else:
        system_msg = "Create a cinematic AI video prompt with camera movement, motion, lighting and atmosphere."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": concept}
        ]
    )

    return response.choices[0].message.content


# 🔹 IMAGE → PROMPT
def analyze_media(base64_image, mode):
    system_msg = "Analyze and recreate this as a professional AI prompt."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_msg},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ]
    )

    return response.choices[0].message.content


# 🔥 MAIN API
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json

    try:
        if data['type'] == 'text':
            result = generate_text_prompt(data['concept'], data['mode'])
        else:
            result = analyze_media(data['imageData'], data['mode'])

        return jsonify({"prompt": result})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()