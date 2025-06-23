# 🧬 Skin Disease Classifier – AI Dermatology Assistant

**Skin Disease Classifier** is an AI-powered web application that predicts skin conditions from images and returns rich metadata including symptoms, causes, treatments, language-translated health tips, and text-to-speech audio guidance.

---

## 🌍 Features

- ✅ Classifies 23 common skin diseases using image input  
- ✅ Provides English, Hausa, Yoruba, and Igbo health tips  
- ✅ Speaks the diagnosis and advice using text-to-speech (TTS)  
- ✅ Uses metadata for detailed disease descriptions, symptoms, causes, and treatments  
- ✅ Built with TensorFlow (MobileNetV2), Gradio, and deployed on Hugging Face Spaces  

---

## 🚀 Try It Live

👉 [Launch on Hugging Face](https://m3ash-skin-disease-classifier.hf.space/?logs=container&__theme=system&deep_link=Alw9-u6V2J0) 

---

## 🧠 Model Information

- **Architecture**: EfficientNetB0 via Transfer Learning  
- **Dataset**: DermNet skin disease images (23 classes)  
- **Framework**: TensorFlow/Keras  
- **Deployment**: Hugging Face Spaces with Gradio UI  

---

## 🧑‍💻 How to Use

```bash
# 1. Clone this repo
git clone https://github.com/your-username/skin-disease-classifier.git
cd skin-disease-classifier

# 2. Install required packages
pip install -r requirements.txt

# 3. Run the Gradio app
python app.py  # or gradio_app.py
```

## 🙏 Acknowledgements

This project would not have been possible without the contributions and tools from the following communities and platforms:

- [DermNet NZ](https://dermnetnz.org/) – For providing the dermatology image dataset that powers this classifier.
- [TensorFlow](https://www.tensorflow.org/) – For deep learning and model development tools.
- [Hugging Face](https://huggingface.co/) – For model and app hosting through Spaces and `huggingface_hub`.
- [Gradio](https://www.gradio.app/) – For building the interactive and user-friendly web interface.
- [gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/) – For enabling voice output in multiple languages.
- [Deep Translator](https://pypi.org/project/deep-translator/) – For enabling text translation into Hausa, Yoruba, and Igbo.
- [Pillow (PIL)](https://pypi.org/project/Pillow/) – For handling image inputs.
- [NumPy](https://numpy.org/) – For efficient array operations used in preprocessing and predictions.

Special thanks to the open-source community for providing tools and inspiration, and to all healthcare professionals whose real-world insights guide the meaningful application of AI in medicine.

