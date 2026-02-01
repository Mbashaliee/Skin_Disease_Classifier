import { useState, useRef } from 'react'
import axios from 'axios'
import { Camera, Upload, Loader2, Volume2, X } from 'lucide-react'
import { supabase } from '../lib/supabase'
import './Classifier.css'

const API_URL = '/api'

const languages = ['English', 'Hausa', 'Yoruba', 'Igbo']

function Classifier() {
  const [selectedImage, setSelectedImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [selectedLanguage, setSelectedLanguage] = useState('English')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [audioUrl, setAudioUrl] = useState(null)
  const [playingAudio, setPlayingAudio] = useState(false)
  const fileInputRef = useRef(null)
  const audioRef = useRef(null)

  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedImage(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
      setResult(null)
      setAudioUrl(null)
    }
  }

  const handleClearImage = () => {
    setSelectedImage(null)
    setImagePreview(null)
    setResult(null)
    setAudioUrl(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handlePredict = async () => {
    if (!selectedImage) return

    setLoading(true)
    setResult(null)
    setAudioUrl(null)

    try {
      const formData = new FormData()
      formData.append('image', selectedImage)
      formData.append('language', selectedLanguage)

      const response = await axios.post(`${API_URL}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setResult(response.data)

      const ttsResponse = await axios.post(`${API_URL}/tts`, {
        disease: response.data.disease,
        tip: response.data.health_tip,
        language: selectedLanguage
      }, {
        responseType: 'blob'
      })

      const audioBlob = new Blob([ttsResponse.data], { type: 'audio/mpeg' })
      const audioUrl = URL.createObjectURL(audioBlob)
      setAudioUrl(audioUrl)

      await savePredictionToSupabase(response.data)

    } catch (error) {
      console.error('Prediction error:', error)
      alert('Failed to analyze image. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const savePredictionToSupabase = async (predictionData) => {
    try {
      await supabase.from('predictions').insert([
        {
          disease: predictionData.disease,
          confidence: predictionData.confidence,
          language: selectedLanguage,
          created_at: new Date().toISOString()
        }
      ])
    } catch (error) {
      console.error('Error saving to Supabase:', error)
    }
  }

  const handlePlayAudio = () => {
    if (audioRef.current) {
      if (playingAudio) {
        audioRef.current.pause()
        setPlayingAudio(false)
      } else {
        audioRef.current.play()
        setPlayingAudio(true)
      }
    }
  }

  return (
    <div className="classifier-container">
      <div className="classifier-card">
        <div className="upload-section">
          <h2 className="section-title">Upload Skin Image</h2>

          {!imagePreview ? (
            <div className="upload-area">
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleImageSelect}
                accept="image/*"
                style={{ display: 'none' }}
                id="file-input"
              />
              <label htmlFor="file-input" className="upload-label">
                <Upload size={48} className="upload-icon" />
                <p className="upload-text">Click to upload or drag and drop</p>
                <p className="upload-subtext">PNG, JPG up to 10MB</p>
              </label>
            </div>
          ) : (
            <div className="image-preview-container">
              <button onClick={handleClearImage} className="clear-button">
                <X size={20} />
              </button>
              <img src={imagePreview} alt="Preview" className="image-preview" />
            </div>
          )}

          <div className="language-selector">
            <label className="selector-label">Select Language</label>
            <div className="language-buttons">
              {languages.map((lang) => (
                <button
                  key={lang}
                  onClick={() => setSelectedLanguage(lang)}
                  className={`language-button ${selectedLanguage === lang ? 'active' : ''}`}
                >
                  {lang}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handlePredict}
            disabled={!selectedImage || loading}
            className="analyze-button"
          >
            {loading ? (
              <>
                <Loader2 className="spinner" size={20} />
                Analyzing...
              </>
            ) : (
              'Analyze Image'
            )}
          </button>
        </div>

        {result && (
          <div className="results-section">
            <h2 className="section-title">Analysis Results</h2>

            <div className="result-card prediction-card">
              <h3 className="result-title">Predicted Disease</h3>
              <p className="disease-name">{result.disease}</p>
              <div className="confidence-bar">
                <div
                  className="confidence-fill"
                  style={{ width: `${result.confidence}%` }}
                ></div>
              </div>
              <p className="confidence-text">Confidence: {result.confidence}%</p>
            </div>

            <div className="result-card metadata-card">
              <h3 className="result-title">Disease Information</h3>
              <div className="metadata-content">
                <div className="metadata-item">
                  <strong>Description:</strong>
                  <p>{result.metadata.description}</p>
                </div>
                <div className="metadata-item">
                  <strong>Symptoms:</strong>
                  <ul>
                    {result.metadata.symptoms.map((symptom, index) => (
                      <li key={index}>{symptom}</li>
                    ))}
                  </ul>
                </div>
                <div className="metadata-item">
                  <strong>Causes:</strong>
                  <ul>
                    {result.metadata.causes.map((cause, index) => (
                      <li key={index}>{cause}</li>
                    ))}
                  </ul>
                </div>
                <div className="metadata-item">
                  <strong>Treatments:</strong>
                  <ul>
                    {result.metadata.treatments.map((treatment, index) => (
                      <li key={index}>{treatment}</li>
                    ))}
                  </ul>
                </div>
                <div className="metadata-item">
                  <strong>Is Contagious:</strong>
                  <p className={result.metadata.is_contagious === 'Yes' ? 'contagious-yes' : 'contagious-no'}>
                    {result.metadata.is_contagious}
                  </p>
                </div>
              </div>
            </div>

            <div className="result-card tip-card">
              <h3 className="result-title">Health Advice</h3>
              <p className="health-tip">{result.health_tip}</p>
              {audioUrl && (
                <button onClick={handlePlayAudio} className="audio-button">
                  <Volume2 size={20} />
                  {playingAudio ? 'Pause Audio' : 'Play Audio Advice'}
                </button>
              )}
              <audio
                ref={audioRef}
                src={audioUrl}
                onEnded={() => setPlayingAudio(false)}
                style={{ display: 'none' }}
              />
            </div>

            <div className="disclaimer">
              <p>This is an AI-based prediction and should not replace professional medical advice. Please consult a dermatologist for accurate diagnosis and treatment.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Classifier
