from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from gtts import gTTS
from deep_translator import GoogleTranslator
from PIL import Image
import numpy as np
import json
import tempfile
import io
import os

app = Flask(__name__)
CORS(app)

model = load_model("../DermNet_Samples.keras")

with open("../dermnet_disease.json", "r") as f:
    disease_metadata = json.load(f)

class_names = [
    'Acne and Rosacea', 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions',
    'Atopic Dermatitis', 'Bullous Disease',
    'Cellulitis Impetigo and other Bacterial Infections', 'Eczema',
    'Exanthems and Drug Eruptions', 'Hair Loss Alopecia and other Hair Diseases',
    'Herpes HPV and other STDs', 'Light Diseases and Disorders of Pigmentation',
    'Lupus and other Connective Tissue diseases', 'Melanoma Skin Cancer Nevi and Moles',
    'Nail Fungus and other Nail Disease', 'Poison Ivy and other Contact Dermatitis',
    'Psoriasis pictures Lichen Planus and related diseases',
    'Scabies Lyme Disease and other Infestations and Bites',
    'Seborrheic Keratoses and other Benign Tumors', 'Systemic Disease',
    'Tinea Ringworm Candidiasis and other Fungal Infections', 'Urticaria Hives',
    'Vascular Tumors', 'Vasculitis',
    'Warts Molluscum and other Viral Infections'
]

original_tips = {
    'Acne and Rosacea': "Wash your face twice daily and use gentle skin products. For serious breakouts, consult a dermatologist.",
    'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions': "Protect your skin from sun exposure and consult a dermatologist immediately if any skin changes appear.",
    'Atopic Dermatitis': "Moisturize your skin frequently, avoid known irritants, and apply anti-inflammatory creams as prescribed.",
    'Bullous Disease': "Avoid trauma to the skin and seek immediate care, as these conditions may be autoimmune-related.",
    'Cellulitis Impetigo and other Bacterial Infections': "Keep the area clean and take antibiotics as prescribed by a healthcare provider.",
    'Eczema': "Avoid hot showers, use mild soap, and moisturize daily. Severe cases may require corticosteroid creams.",
    'Exanthems and Drug Eruptions': "Stop using the suspected medication and consult a healthcare provider urgently.",
    'Hair Loss Alopecia and other Hair Diseases': "Be gentle with hair, avoid tight hairstyles, and consult a doctor for treatment options.",
    'Herpes HPV and other STDs': "Avoid direct contact during outbreaks and use antiviral medication as prescribed.",
    'Light Diseases and Disorders of Pigmentation': "Use sunscreen regularly and seek expert evaluation for sudden pigmentation changes.",
    'Lupus and other Connective Tissue diseases': "Avoid sunlight exposure and follow the treatment prescribed by a rheumatologist.",
    'Melanoma Skin Cancer Nevi and Moles': "Monitor for any skin changes in moles and consult a dermatologist for screening.",
    'Nail Fungus and other Nail Disease': "Keep nails dry and trimmed; antifungal treatments may be required for infections.",
    'Poison Ivy and other Contact Dermatitis': "Avoid contact with allergens and use anti-itch or steroid creams as directed.",
    'Psoriasis pictures Lichen Planus and related diseases': "Keep skin moisturized and use medicated creams. Stress management can help.",
    'Scabies Lyme Disease and other Infestations and Bites': "Apply prescribed topical treatments and wash all clothes and bedding.",
    'Seborrheic Keratoses and other Benign Tumors': "Usually harmless, but removal may be done for cosmetic reasons. Consult a dermatologist.",
    'Systemic Disease': "Skin symptoms may reflect an internal condition. Immediate medical consultation is advised.",
    'Tinea Ringworm Candidiasis and other Fungal Infections': "Apply antifungal cream regularly and keep the area dry. Avoid sharing personal items.",
    'Urticaria Hives': "Avoid known allergens and take antihistamines. If persistent, consult a doctor.",
    'Vascular Tumors': "Some vascular tumors are harmless, but others may need medical imaging or removal.",
    'Vasculitis': "Seek medical care promptly, as vasculitis may indicate an underlying autoimmune disorder.",
    'Warts Molluscum and other Viral Infections': "Avoid scratching, maintain hygiene, and use antiviral or cryotherapy treatments as needed."
}

tts_lang_codes = {
    "English": "en",
    "Hausa": "ha",
    "Yoruba": "yo",
    "Igbo": "ig"
}

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": True})

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        language = request.form.get('language', 'English')
        file = request.files['image']

        img = Image.open(io.BytesIO(file.read()))
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        prediction = model.predict(img_array)[0]
        predicted_index = np.argmax(prediction)
        confidence = float(prediction[predicted_index]) * 100
        most_likely_class = class_names[predicted_index]

        tip_text = original_tips.get(most_likely_class, "Maintain good hygiene and seek professional care.")
        tip_text += " Contact a dermatologist for better treatment."

        lang_code = tts_lang_codes.get(language, "en")
        translated_tip = GoogleTranslator(source='en', target=lang_code).translate(tip_text)

        meta = disease_metadata.get(most_likely_class, {})

        response_data = {
            "disease": most_likely_class,
            "confidence": round(confidence, 2),
            "metadata": {
                "description": meta.get('description', 'N/A'),
                "symptoms": meta.get('symptoms', []),
                "causes": meta.get('causes', []),
                "treatments": meta.get('treatments', []),
                "is_contagious": meta.get('is_contagious', 'Unknown')
            },
            "health_tip": translated_tip,
            "language": language
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.json
        disease = data.get('disease')
        tip = data.get('tip')
        language = data.get('language', 'English')

        message = f"This disease is most likely to be {disease}. The health tip for this predicted disease is: {tip}"

        lang_code = tts_lang_codes.get(language, "en")
        tts = gTTS(text=message, lang=lang_code)

        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)

        return send_file(temp_audio.name, mimetype="audio/mpeg")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').lower()

        if "hello" in message or "hi" in message:
            response = "Hello! How can I assist you with skin diseases or this app?"
        elif "symptom" in message:
            response = "Upload an image to get the predicted disease and its symptoms."
        elif "treatment" in message:
            response = "I'll give treatment advice once a disease is predicted."
        elif "tip" in message:
            response = "Tips will appear after prediction in your selected language."
        elif "thank" in message:
            response = "You're welcome!"
        else:
            response = "I'm your AI Assistant. Ask me about skin conditions, translations, or app usage."

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
