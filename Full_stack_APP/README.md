# 🦷 Dental & Gum Disease Classifier - Full Stack Application

## Stack Overview

- **Frontend**: React + Vite + TailwindCSS
- **Backend**: FastAPI + TensorFlow/Keras
- **Communication**: REST API with CORS

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (for backend)
- Node.js 16+ (for frontend)

### Step 1: Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Place your model files in app/models/:
# - DENTAL_MODEL_BEST.keras
# - GINGIVITIS_MODEL_AUGMENTED.keras

# Run backend server
cd app
python main.py
```

Backend will be available at: **http://localhost:8000**

### Step 2: Frontend Setup

```powershell
# Navigate to frontend (open new terminal)
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: **http://localhost:5173**

---

## 📁 Project Structure

```
full_stack_app/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   └── model_loader.py    # Dual model predictors
│   │   ├── models/                 # Place .keras files here
│   │   └── main.py                 # FastAPI app with CORS
│   ├── static/
│   │   └── uploads/                # Temporary image storage
│   ├── templates/
│   │   └── index.html              # Original HTML (still works)
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── services/
    │   │   └── api.js              # API service for backend
    │   ├── App.jsx                 # Main React component
    │   ├── App.css                 # Custom styles
    │   └── main.jsx                # Entry point
    ├── index.html
    ├── vite.config.js
    └── package.json
```

---

## 🔗 API Endpoints

| Method | Endpoint             | Description             |
| ------ | -------------------- | ----------------------- |
| GET    | `/api/models`        | Get model information   |
| POST   | `/api/predict`       | Single image prediction |
| POST   | `/api/predict_batch` | Batch image prediction  |
| GET    | `/health`            | Health check            |
| GET    | `/clear`             | Clear uploaded files    |
| GET    | `/`                  | Original HTML interface |

---

## 🎨 Features

### Dual Model System

- **Teeth Disease Model**: 4-class detection (caries, calculus, healthy, discoloration)
- **Gum Disease Model**: 2-class detection (healthy, gingivitis)

### User Features

- ✅ Interactive model selection
- ✅ Single image upload & analysis
- ✅ Batch image processing
- ✅ Real-time predictions
- ✅ Visual confidence charts
- ✅ Animated UI elements
- ✅ Responsive design

### Technical Features

- ✅ React frontend with Vite
- ✅ FastAPI backend with CORS
- ✅ RESTful API architecture
- ✅ File upload handling
- ✅ Error handling & validation
- ✅ CPU-optimized inference

---

## 🛠️ Development

### Backend Development

```powershell
cd backend/app
python main.py
```

The backend serves both:

- **React API**: `http://localhost:8000/api/*`
- **HTML UI**: `http://localhost:8000/`

### Frontend Development

```powershell
cd frontend
npm run dev
```

Hot reload enabled for React components.

### Building for Production

```powershell
# Build frontend
cd frontend
npm run build

# The dist folder can be served by FastAPI
# Update backend to serve React build
```

---

## 🔧 Configuration

### Backend CORS Settings

Edit `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend API URL

Edit `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = "http://localhost:8000"; // Change for production
```

---

## 📊 How It Works

### Architecture Flow

```
React Frontend (Port 5173)
    ↓ HTTP Request
FastAPI Backend (Port 8000)
    ↓ Load Image
Model Predictor
    ↓ Inference
TensorFlow/Keras Models
    ↓ Results
JSON Response
    ↓
React UI Update
```

### Request Flow Example

1. **User uploads image** in React
2. **React calls API** (`/api/predict`)
3. **FastAPI receives file** and model_type
4. **Backend saves image** to uploads/
5. **Model predicts** disease
6. **Results sent** as JSON
7. **React displays** results with charts

---

## 🎯 Usage

### Using the React App

1. **Open** `http://localhost:5173`
2. **Select Model**:
   - Click "Teeth Disease" or "Gum Disease"
3. **Choose Upload Mode**:
   - Single Image tab
   - Batch Analysis tab
4. **Upload Image(s)**
5. **View Results**:
   - Prediction with confidence
   - Probability distribution
   - Visual charts

### Using the HTML Interface

1. **Open** `http://localhost:8000`
2. Same functionality, traditional HTML forms

---

## 🐛 Troubleshooting

### CORS Errors

✅ **Solution**: Ensure backend is running and CORS is configured for `http://localhost:5173`

### API Connection Failed

✅ **Solution**:

- Check backend is running on port 8000
- Check `API_BASE_URL` in `frontend/src/services/api.js`

### Models Not Loading

✅ **Solution**: Place `.keras` files in `backend/app/models/`

### Port Already in Use

✅ **Solution**:

```powershell
# Kill process on port
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 📦 Dependencies

### Backend (`requirements.txt`)

```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
Pillow==10.1.0
numpy==1.24.3
tensorflow-cpu==2.15.0
aiofiles==23.2.1
jinja2==3.1.2
python-dotenv==1.0.0
```

### Frontend (`package.json`)

```json
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.4",
    "@tailwindcss/vite": "^4.0.0-beta.6",
    "vite": "^6.0.7"
  }
}
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Build React app: `npm run build`
- [ ] Update CORS for production URLs
- [ ] Change API_BASE_URL to production
- [ ] Set up reverse proxy (nginx)
- [ ] Enable HTTPS
- [ ] Configure environment variables
- [ ] Set file upload limits
- [ ] Add rate limiting
- [ ] Monitor backend logs

---

## ⚕️ Medical Disclaimer

This tool is for **educational and screening purposes only**.

Always consult with a qualified dental professional for:

- Accurate diagnosis
- Treatment recommendations
- Professional medical advice

---

## 📖 API Documentation

### GET /api/models

Returns information about available models.

**Response**:

```json
{
  "dental": {
    "loaded": true,
    "classes": [...],
    "name": "Teeth Disease Detection",
    "description": "4-class detection for dental conditions"
  },
  "gingivitis": {
    "loaded": true,
    "classes": [...],
    "name": "Gum Disease Detection",
    "description": "Binary classification for gingivitis"
  }
}
```

### POST /api/predict

Predict single image.

**Form Data**:

- `file`: Image file (JPG, PNG)
- `model_type`: "dental" or "gingivitis"

**Response**:

```json
{
  "prediction": "caries",
  "confidence": 85.23,
  "all_probabilities": {...},
  "image_url": "...",
  "processing_time_ms": 1234.56,
  ...
}
```

### POST /api/predict_batch

Predict multiple images.

**Form Data**:

- `files`: Multiple image files
- `model_type`: "dental" or "gingivitis"

**Response**:

```json
{
  "results": [...],
  "model_type": "dental"
}
```

---

## 🎓 Learning Resources

### Technologies Used

- **React**: Frontend framework
- **Vite**: Build tool and dev server
- **TailwindCSS**: Utility-first CSS
- **FastAPI**: Python web framework
- **TensorFlow**: Machine learning
- **CORS**: Cross-origin resource sharing

### Next Steps

- Add user authentication
- Implement result history
- Add PDF report generation
- Create mobile app
- Deploy to cloud

---

## 🏆 Success!

You now have a complete full-stack dental AI application with:

- ✨ Modern React frontend
- 🤖 Powerful FastAPI backend
- 🔗 Seamless API communication
- 📱 Responsive UI
- 🎨 Beautiful design

**Start both servers and visit http://localhost:5173!** 🎉

---

© 2024 Dental AI Research Project • Educational Use Only
