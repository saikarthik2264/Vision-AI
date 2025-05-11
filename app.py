from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from PIL import Image
import io

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = 'AIzaSyAm3IA8xBoVjui3LItdi18ysA1feYD-pvA'
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini models
model = genai.GenerativeModel('gemini-2.0-flash')

# Configure model settings
generation_config = genai.types.GenerationConfig(
    temperature=0.7,  # Reduced for more focused responses
    top_p=0.8,       # Reduced for more precise outputs
    top_k=40,        # Balanced token selection
    max_output_tokens=150  # Limit response length for brevity
)

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/chat')
def chat_page():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        response = model.generate_content(message, generation_config=generation_config)
        return jsonify({'response': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image_file = request.files['image']
        prompt = request.form.get('prompt', 'Provide a brief, focused description of the key elements in this image in 2-3 sentences.')

        # Process the image
        image_data = Image.open(io.BytesIO(image_file.read()))
        response = model.generate_content([prompt, image_data], generation_config=generation_config)

        return jsonify({'response': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)