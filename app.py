import gradio as gr
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from gtts import gTTS
from deep_translator import GoogleTranslator
from PIL import Image
import tempfile
import json
import os

# === Load model ===
model = load_model("DermNet_Samples.keras")

# === Load metadata ===
with open("dermnet_disease.json", "r") as f:
    disease_metadata = json.load(f)

# === Class names must match the model's output order ===
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

# === Health tips ===
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

# === Language codes ===
tts_lang_codes = {
    "English": "en",
    "Hausa": "ha",
    "Yoruba": "yo",
    "Igbo": "ig"
}

# === TTS Function ===
def generate_tip_audio(disease, language):
    tip = original_tips.get(disease, "Maintain good hygiene and seek professional care.")
    sentence = f"This disease is most likely {disease}. The health tip for this predicted disease is: {tip}. Contact a dermatologist for better treatment."
    translated_tip = GoogleTranslator(source='en', target=tts_lang_codes[language]).translate(sentence)

    tts = gTTS(text=translated_tip, lang=tts_lang_codes[language])
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return translated_tip, temp_audio.name

# === Classifier Function ===
def generate_tip_audio(disease, language, translated_tip):
    message = (
        f"This disease is most likely to be {disease}. "
        f"The health tip for this predicted disease is: {translated_tip}"
    )
    lang_code = tts_lang_codes.get(language, "en")
    tts = gTTS(text=message, lang=lang_code)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

def predict_and_translate(img, language):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    prediction = model.predict(img_array)[0]
    top_indices = prediction.argsort()[-3:][::-1]  # Top 3 predictions
    top_probs = [(class_names[i], int(prediction[i] * 100)) for i in top_indices]

    most_likely_class, most_likely_prob = top_probs[0]

    # Translate tip
    tip_text = original_tips.get(most_likely_class, "Maintain good hygiene and seek professional care.")
    tip_text += " Contact a dermatologist for better treatment."
    translated_tip = GoogleTranslator(source='en', target=tts_lang_codes[language]).translate(tip_text)

    # Metadata
    meta = disease_metadata.get(most_likely_class, {})
    meta_text = f"**Description**: {meta.get('description', 'N/A')}\n\n"
    meta_text += f"**Symptoms**: {', '.join(meta.get('symptoms', []))}\n\n"
    meta_text += f"**Causes**: {', '.join(meta.get('causes', []))}\n\n"
    meta_text += f"**Treatments**: {', '.join(meta.get('treatments', []))}\n\n"
    meta_text += f"**Is Contagious?**: {meta.get('is_contagious', 'Unknown')}"

    # Prepare Audio
    audio_path = generate_tip_audio(most_likely_class, language, translated_tip)

    # Format top predictions string
    prediction_summary = "\n".join([f"{name}: {prob}%" for name, prob in top_probs])

    return (
        f"This disease is most likely to be: {most_likely_class} ({most_likely_prob}%)",
        prediction_summary,
        meta_text,
        f"The health tip for this predicted disease is:\n{translated_tip}",
        audio_path
    )


# === AI Assistant Bot ===
def ai_assistant_bot(message):
    message = message.lower()
    if "hello" in message or "hi" in message:
        return "👋 Hello! How can I assist you with skin diseases or this app?"
    elif "symptom" in message:
        return "Upload an image to get the predicted disease and its symptoms."
    elif "treatment" in message:
        return "I'll give treatment advice once a disease is predicted."
    elif "tip" in message:
        return "Tips will appear after prediction in your selected language."
    elif "thank" in message:
        return "You're welcome! 😊"
    else:
        return "I'm your AI Assistant. Ask me about skin conditions, translations, or app usage."

# === Main Interface ===
skin_disease_interface = gr.Interface(
    fn=predict_and_translate,
    inputs=[
        gr.Image(type="pil", label="Upload or Capture Skin Image", sources=["upload", "webcam"]),
        gr.Radio(choices=["English", "Hausa", "Yoruba", "Igbo"], label="Select Language", value="English")
    ],
    outputs=[
        gr.Text(label="Most Likely Disease Prediction"),
        gr.Text(label="Top 3 Predictions with Probabilities"),
        gr.Text(label="Disease Metadata"),
        gr.Text(label="Health Tip (Translated)"),
        gr.Audio(label="Text-to-Speech Health Tip")
    ],
    title="🧠 AI Skin Disease Classifier",
    description="Upload an image to get disease prediction, health tips, TTS, and detailed metadata."
)

chatbot_interface = gr.Interface(
    fn=ai_assistant_bot,
    inputs=gr.Textbox(lines=2, placeholder="Ask the AI Assistant about skin diseases or the app..."),
    outputs="text",
    title="💬 AI Assistant Chatbot"
)

# === Combined UI ===
gr.TabbedInterface(
    [skin_disease_interface, chatbot_interface],
    ["📷 Skin Classifier", "🤖 Chatbot Assistant"]
).launch()
