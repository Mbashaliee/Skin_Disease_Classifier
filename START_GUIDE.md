# Quick Start Guide

## Starting the Application

You need to run both the backend and frontend servers. Follow these steps:

### Terminal 1: Start Backend (Flask API)

```bash
# Navigate to backend directory
cd backend

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the Flask server
python app.py
```

Backend will run on: `http://localhost:5000`

### Terminal 2: Start Frontend (React App)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start the development server
npm run dev
```

Frontend will run on: `http://localhost:5173`

## Access the Application

Open your browser and visit: **http://localhost:5173**

## Quick Test

1. Click on "Image Classifier" tab
2. Upload any skin image
3. Select a language (English, Hausa, Yoruba, or Igbo)
4. Click "Analyze Image"
5. View the results and listen to audio advice
6. Try the "AI Assistant" tab to ask questions

## Troubleshooting

### Backend Issues

**Error: Module not found**
```bash
cd backend
pip install -r requirements.txt
```

**Error: Port 5000 already in use**
- Stop other applications using port 5000
- Or change the port in `backend/app.py` (line: `app.run(debug=True, port=5000)`)

### Frontend Issues

**Error: Cannot connect to API**
- Make sure the backend is running on port 5000
- Check that `http://localhost:5000/api/health` returns a response

**Error: Module not found**
```bash
cd frontend
npm install
```

### Model Loading Issues

**Error: Model file not found**
- Ensure `DermNet_Samples.keras` exists in the project root directory
- The backend looks for the model at `../DermNet_Samples.keras`

## Features to Try

### Image Classifier
- Upload images of skin conditions
- Try different languages
- Listen to audio advice in multiple languages
- View detailed disease information
- Check confidence scores

### AI Assistant Chatbot
- Ask about symptoms
- Request treatment information
- Get help using the app
- Learn about skin conditions

## Production Build

To create a production build of the frontend:

```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

## Notes

- All predictions are automatically saved to Supabase
- The application requires internet for translation and TTS services
- For best results, use clear, well-lit images of skin conditions
- Always consult a healthcare professional for medical advice

## Support

For issues or questions:
1. Check the console for error messages
2. Verify both servers are running
3. Check network connectivity
4. Review the PROJECT_README.md for detailed information
