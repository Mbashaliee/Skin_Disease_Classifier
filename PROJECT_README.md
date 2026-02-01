# Skin Disease Classifier Web Application

A modern web application for AI-powered skin disease classification with multilingual support, text-to-speech health advice, and an AI assistant chatbot.

## Features

- **Image-Based Classification**: Upload or capture skin images to detect 23 common skin diseases
- **Multilingual Support**: Get health advice in English, Hausa, Yoruba, and Igbo
- **Text-to-Speech**: Listen to health recommendations in your preferred language
- **Disease Information**: View detailed symptoms, causes, treatments, and contagiousness
- **AI Assistant**: Interactive chatbot to answer questions about skin conditions
- **Prediction History**: All predictions are saved to Supabase for tracking

## Architecture

### Frontend (React + Vite)
- Modern, responsive UI with gradient design
- Image upload with preview
- Real-time disease classification
- Audio playback for health tips
- Interactive chatbot interface

### Backend (Flask)
- REST API for model inference
- TensorFlow/Keras model integration
- Text-to-speech generation
- Translation services
- CORS enabled for frontend communication

### Database (Supabase)
- PostgreSQL database for prediction history
- Row Level Security enabled
- Public access for logging predictions

## Project Structure

```
project/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Classifier.jsx
│   │   │   ├── Classifier.css
│   │   │   ├── Chatbot.jsx
│   │   │   └── Chatbot.css
│   │   ├── lib/
│   │   │   └── supabase.js   # Supabase client
│   │   ├── App.jsx           # Main app component
│   │   ├── App.css
│   │   └── index.css
│   ├── .env                  # Environment variables
│   └── package.json
│
├── backend/                  # Flask API
│   ├── app.py               # Main Flask application
│   └── requirements.txt     # Python dependencies
│
├── DermNet_Samples.keras    # Trained model
├── dermnet_disease.json     # Disease metadata
└── .env                     # Supabase credentials

```

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Supabase account (already configured)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## Usage

1. Open your browser and go to `http://localhost:5173`
2. Click on the "Image Classifier" tab
3. Upload or capture a skin image
4. Select your preferred language
5. Click "Analyze Image"
6. View the results including:
   - Disease prediction with confidence score
   - Detailed disease information
   - Health advice in your selected language
   - Audio playback of the advice
7. Switch to the "AI Assistant" tab to ask questions

## Supported Diseases (23 Classes)

1. Acne and Rosacea
2. Actinic Keratosis, Basal Cell Carcinoma and other Malignant Lesions
3. Atopic Dermatitis
4. Bullous Disease
5. Cellulitis, Impetigo and other Bacterial Infections
6. Eczema
7. Exanthems and Drug Eruptions
8. Hair Loss, Alopecia and other Hair Diseases
9. Herpes, HPV and other STDs
10. Light Diseases and Disorders of Pigmentation
11. Lupus and other Connective Tissue diseases
12. Melanoma, Skin Cancer, Nevi and Moles
13. Nail Fungus and other Nail Disease
14. Poison Ivy and other Contact Dermatitis
15. Psoriasis, Lichen Planus and related diseases
16. Scabies, Lyme Disease and other Infestations and Bites
17. Seborrheic Keratoses and other Benign Tumors
18. Systemic Disease
19. Tinea, Ringworm, Candidiasis and other Fungal Infections
20. Urticaria (Hives)
21. Vascular Tumors
22. Vasculitis
23. Warts, Molluscum and other Viral Infections

## Technologies Used

### Frontend
- React 18
- Vite
- Axios
- Supabase JS Client
- Lucide React (icons)

### Backend
- Flask
- TensorFlow/Keras
- gTTS (Google Text-to-Speech)
- Deep Translator
- Pillow (PIL)
- NumPy

### Database
- Supabase (PostgreSQL)

## Environment Variables

The `.env` file contains:
```
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_SUPABASE_ANON_KEY=your_anon_key
```

## API Endpoints

### GET /api/health
Health check endpoint

### POST /api/predict
Classify skin disease from image
- Body: `multipart/form-data` with `image` file and `language` parameter
- Returns: Disease prediction with metadata

### POST /api/tts
Generate text-to-speech audio
- Body: `{ disease, tip, language }`
- Returns: Audio file (MP3)

### POST /api/chat
Chat with AI assistant
- Body: `{ message }`
- Returns: `{ response }`

## Important Notes

- This application is for educational purposes only
- Always consult a healthcare professional for accurate diagnosis
- The AI predictions should not replace professional medical advice
- Prediction history is stored in Supabase for tracking purposes

## License

MIT License - See LICENSE file for details

## Acknowledgements

- DermNet NZ for the dataset
- TensorFlow/Keras for deep learning framework
- Supabase for database infrastructure
- Google for translation and TTS services
