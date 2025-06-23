🧠 SkinVision – AI Skin Disease Classifier with Multilingual Support
SkinVision is an AI-powered application that classifies 23 different skin conditions using deep learning. It provides rich metadata, health advice, multilingual translations (English, Hausa, Yoruba, Igbo), and text-to-speech recommendations — all from an image of a skin condition.



🌟 Features
✅ Classifies 23 common skin diseases from image input

✅ Displays disease name, description, symptoms, causes, treatments, and contagious info

✅ Translates health tips into Hausa, Yoruba, and Igbo

✅ Text-to-Speech for health tips in selected languages

✅ Model loaded from Hugging Face Hub

✅ Built with TensorFlow (MobileNetV2), Gradio, and deployed on Hugging Face Spaces

🚀 Try It Live
👉 [Launch on Hugging Face](https://m3ash-skin-disease-classifier.hf.space/?logs=container&__theme=system&deep_link=Alw9-u6V2J0)

🧠 Model Information
Architecture: MobileNetV2 (Transfer Learning)

Dataset: DermNet Skin Disease Images (23 Classes)

Format: .keras, hosted on Hugging Face Hub

Framework: TensorFlow/Keras

📁 Project Structure
bash
Copy
Edit
skin-disease-classifier/
├── app.py                   # Streamlit or Gradio app
├── metadata.json            # Disease metadata
├── requirements.txt         # Dependencies
├── utils/                   # Utility modules (model loading, TTS, translation)
├── assets/                  # Screenshots or icons
└── README.md
⚙️ How to Run Locally
bash
Copy
Edit
# 1. Clone the repo
git clone https://github.com/your-username/skin-disease-classifier.git
cd skin-disease-classifier

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
📦 Hugging Face Model Loader Example
python
Copy
Edit
from huggingface_hub import hf_hub_download
from tensorflow.keras.models import load_model

model_path = hf_hub_download(
    repo_id="your-username/skin-disease-model",
    filename="DermNet_Samples.keras"
)
model = load_model(model_path)
👨‍⚕️ Note
This tool provides informational support only and is not a substitute for professional medical advice. Always consult a licensed dermatologist for clinical diagnosis or treatment.
