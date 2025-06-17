from tensorflow.keras.models import load_model
import gradio as gr
import numpy as np
from PIL import Image

# Load the saved model
model = load_model("skin_disease_model.h5")

# Your class names (replace with your actual ones)
class_names = ['acne', 'eczema', 'fungal_infection', 'psoriasis', 'vitiligo']

def predict(image):
    image = image.resize((180, 180))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    predictions = model.predict(image)[0]
    result = {class_names[i]: float(predictions[i]) for i in range(len(class_names))}
    return result

demo = gr.Interface(fn=predict, inputs="image", outputs="label", title="Skin Disease Classifier")
demo.launch()
