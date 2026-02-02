# Dental & Gum Disease Classification System

AI-powered dental health screening with dual model support.

## Features

🦷 **Teeth Disease Detection** (4 Classes)

- Caries (tooth decay)
- Calculus (tartar buildup)
- Healthy teeth
- Discoloration

🩺 **Gum Disease Detection** (2 Classes)

- Healthy gums
- Gingivitis

## Installation

### 1. Create Virtual Environment (if not exists)

```powershell
python -m venv venv
```

### 2. Activate Virtual Environment

```powershell
.\venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Usage

### Quick Start

```powershell
# From the backend directory
python run.py
```

Or manually:

```powershell
cd app
python main.py
```

### Access the Application

Open your browser and navigate to:

```
http://localhost:8000
```

## Project Structure

```
backend/
├── app/
│   ├── services/
│   │   ├── __init__.py
│   │   └── model_loader.py      # Dual model predictors
│   ├── models/                   # Place your .keras models here
│   │   ├── DENTAL_MODEL_BEST.keras
│   │   └── GINGIVITIS_MODEL_AUGMENTED.keras
│   ├── __init__.py
│   └── main.py                   # FastAPI application
├── templates/
│   └── index.html                # Web interface
├── static/
│   └── uploads/                  # Temporary image storage
├── requirements.txt              # Python dependencies
├── run.py                        # Quick startup script
└── README.md                     # This file
```

## How It Works

1. **Select Model**: Choose between Teeth Disease or Gum Disease analysis
2. **Upload Image**: Single image or batch upload
3. **AI Analysis**: Selected model processes the image
4. **View Results**: Get confidence scores and detailed predictions

## Models

### Teeth Disease Model (DENTAL_MODEL_BEST.keras)

- Architecture: ResNet50
- Input: 224x224x3 RGB images
- Output: 4 classes with probabilities
- Preprocessing: ResNet50 preprocessing

### Gum Disease Model (GINGIVITIS_MODEL_AUGMENTED.keras)

- Architecture: Custom CNN
- Input: 224x224x3 RGB images
- Output: Binary classification (Healthy/Gingivitis)
- Preprocessing: Simple normalization (0-1)

## API Endpoints

- `GET /` - Main web interface
- `POST /predict` - Single image prediction
- `POST /predict_batch` - Batch image prediction
- `GET /clear` - Clear uploaded files
- `GET /health` - Health check

## Requirements

- Python 3.8+
- FastAPI
- TensorFlow (CPU optimized)
- Pillow
- aiofiles
- Jinja2

## Performance Optimization

- CPU-only mode (no GPU required)
- Batch size: 1 for memory efficiency
- Max file size: 10MB per image
- Optimized for i3 processors and low-end systems

## Medical Disclaimer

⚕️ This tool is for **educational and screening purposes only**. Always consult with a qualified dental professional for diagnosis and treatment.

## Troubleshooting

### Model not loading?

- Ensure model files are in `app/models/` directory
- Check file names match exactly:
  - `DENTAL_MODEL_BEST.keras`
  - `GINGIVITIS_MODEL_AUGMENTED.keras`

### Out of memory errors?

- Close other applications
- Use single image mode instead of batch
- Restart the application

### Slow predictions?

- First prediction is slower (model warmup)
- Subsequent predictions are faster
- CPU-bound, so patience on older hardware

## Development

To modify the application:

1. Edit `app/main.py` for API endpoints
2. Edit `app/services/model_loader.py` for model logic
3. Edit `templates/index.html` for UI changes
4. Run with `reload=True` in main.py for development

## Credits

Developed for educational dental health screening research.
Version 2.0 - Dual Model Support

## License

Educational use only.
