
from flask import Blueprint, make_response, jsonify, request, send_file
from gtts import gTTS
import os
import pytesseract
from PIL import Image
import io
import speech_recognition as sr
from random import choice
from api.models import *
from api.models.pytorch import *

blueprint = Blueprint("blueprint", __name__)
recognizer = sr.Recognizer()

@blueprint.route('/v1/chat', methods=["POST"]) 
def chat():
    data = {"success": False}
    if request.method == "POST":
        try:
            if request.is_json:
                json = request.get_json(force=True)
                if json.get("message"):
                    res = predict_tag(ai_therapy_model, json.get("message"), device)
                    intent = list(filter(lambda x: x['tag'] == res.tag, intents))[0]
                    message = choice(
                        intent['responses']
                    )
                    data = {
                        'success': True,
                        'prediction': res.to_json(),
                        'response': BotResponse(message=message).to_json() 
                    }  
                else:
                    data['error']  = "you should pass the 'text' in your json body while making this request."
            else:
                raise Exception("the is no json data in your request.")
        except Exception as e:
            print(e)
            data['error'] = 'something went wrong on the server'
    else:
        data['error']  = "the request method should be post only."        
    return make_response(jsonify(data)), 200

@blueprint.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        image = Image.open(io.BytesIO(file.read()))
        text = pytesseract.image_to_string(image)
        return jsonify({"extracted_text": text}), 200

@blueprint.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'file' not in request.files:
        return "File not uploaded", 400
    
    audio_file = request.files['file']
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)

            return jsonify({"text": text}), 200
        except sr.UnknownValueError:
            return jsonify({"error": "Google Speech Recognition could not understand audio"}), 400
        except sr.RequestError as e:
            return jsonify({"error": "Could not request results; {0}".format(e)}), 500


@blueprint.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    if 'text' not in request.json:
        return jsonify({"error": "No text provided"}), 400
    
    text = request.json['text']
    language = request.json.get('lang', 'en')  # Default to English if no language is provided

    try:
        tts = gTTS(text=text, lang=language, slow=False)
        # Save the audio file temporarily
        audio_file_path = "/Users/aashigupta/Documents/AIThearpy/output/output.mp3"
        tts.save(audio_file_path)

        # Send the file to the client
        return send_file(audio_file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500