import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

print("🚀 SERVER STARTING...")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔐 Secure API Key (from Render Environment)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ✅ Home route (optional UI support)
@app.route('/')
def home():
    return jsonify({"message": "API is running 🚀"})

# 🔹 TEXT → PROMPT
def generate_text_prompt(concept, mode):
    if mode == 'image':
        system_msg = """You are an expert AI Image Prompt Engineer.
Create a highly detailed prompt including subject, lighting, camera angle,
style (cinematic, 8k, unreal engine), color palette and negative prompts."""
    else:
        system_msg = """You are an expert AI Video Prompt Engineer.
Create a cinematic prompt including camera movement, motion, lighting,
atmosphere, subject detail and pacing."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": concept}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


# 🔹 IMAGE → PROMPT
def analyze_media(base64_image, mode):
    system_msg = "Analyze this media and generate a professional AI prompt."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_msg},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe and recreate this."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=300
    )

    return response.choices[0].message.content


# 🔥 MAIN API
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json

    try:
        mode = data.get('mode')
        input_type = data.get('type')

        if input_type == 'text':
            concept = data.get('concept')
            if not concept:
                return jsonify({"error": "Concept is required"}), 400

            result = generate_text_prompt(concept, mode)

        else:
            image_data = data.get('imageData')
            if not image_data:
                return jsonify({"error": "Image data missing"}), 400

            result = analyze_media(image_data, mode)

        return jsonify({"prompt": result})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)}), 500


# 🚀 RUN
if __name__ == '__main__':
    app.run()