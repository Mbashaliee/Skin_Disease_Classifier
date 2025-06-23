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
    'Acne and Rosacea',
    'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions',
    'Atopic Dermatitis',
    'Bullous Disease',
    'Cellulitis Impetigo and other Bacterial Infections',
    'Eczema',
    'Exanthems and Drug Eruptions',
    'Hair Loss Alopecia and other Hair Diseases',
    'Herpes HPV and other STDs',
    'Light Diseases and Disorders of Pigmentation',
    'Lupus and other Connective Tissue diseases',
    'Melanoma Skin Cancer Nevi and Moles',
    'Nail Fungus and other Nail Disease',
    'Poison Ivy and other Contact Dermatitis',
    'Psoriasis pictures Lichen Planus and related diseases',
    'Scabies Lyme Disease and other Infestations and Bites',
    'Seborrheic Keratoses and other Benign Tumors',
    'Systemic Disease',
    'Tinea Ringworm Candidiasis and other Fungal Infections',
    'Urticaria Hives',
    'Vascular Tumors',
    'Vasculitis',
    'Warts Molluscum and other Viral Infections'
]

# === Short health tips in English ===
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

# === Text + TTS for Tip and Recommendation ===
def generate_tip_audio(disease, language):
    tip = original_tips.get(disease, "Maintain good hygiene and seek professional care.")
    base_tip = f"{tip} Contact a dermatologist for better treatment."
    translated_tip = GoogleTranslator(source='en', target=tts_lang_codes[language]).translate(base_tip)

    tts = gTTS(text=f"{disease}. {translated_tip}", lang=tts_lang_codes[language])
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return translated_tip, temp_audio.name

# === Prediction, Translation, Metadata ===
def predict_and_translate(img, language):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction)
    predicted_class = class_names[predicted_index]

    # Get and format metadata
    meta = disease_metadata.get(predicted_class, {})
    meta_text = f"**Description**: {meta.get('description', 'N/A')}\n\n"
    meta_text += f"**Symptoms**: {', '.join(meta.get('symptoms', []))}\n\n"
    meta_text += f"**Causes**: {', '.join(meta.get('causes', []))}\n\n"
    meta_text += f"**Treatments**: {', '.join(meta.get('treatments', []))}\n\n"
    meta_text += f"**Is Contagious?**: {meta.get('is_contagious', 'Unknown')}"

    # Generate multilingual health tip + TTS
    translated_tip, audio_path = generate_tip_audio(predicted_class, language)

    return predicted_class, meta_text, translated_tip, audio_path


# === Gradio Interface ===
interface = gr.Interface(
    fn=predict_and_translate,
    inputs=[
        gr.Image(type="pil", label="Upload Skin Image"),
        gr.Radio(choices=["English", "Hausa", "Yoruba", "Igbo"], label="Select Language", value="English")
    ],
    outputs=[
        gr.Text(label="Predicted Disease"),
        gr.Text(label="Disease Metadata"),
        gr.Text(label="Health Tip (Translated)"),
        gr.Audio(label="Health Tip Audio")
    ],
    title="🧠 AI-Powered Skin Disease Classifier",
    description="Upload a skin image. Get a disease prediction, multilingual health tips, audio advice, and dermatologist recommendation."
)
interface.launch()
