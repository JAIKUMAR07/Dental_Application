import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import io
import uuid
import traceback
import numpy as np
from pathlib import Path
from PIL import Image
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import model - IMPORTANT: Use relative import
try:
    from .model import DentalDiseasePredictor
except ImportError:
    from model import DentalDiseasePredictor

app = FastAPI(title="Dental AI System")
BASE_DIR = Path(__file__).resolve().parent

# Setup folders
UPLOAD_DIR = "static/uploads"
GRADCAM_DIR = "static/gradcam"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GRADCAM_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Model paths to try (in order)
MODEL_PATHS = [
    "DENTAL_MODEL_TF215.keras",      # Fixed version
    "DENTAL_MODEL_COMPATIBLE.h5",    # Converted
    "DENTAL_MODEL_BEST.keras",       # Original
]

predictor = None

def load_model():
    global predictor
    
    if predictor is not None:
        return predictor
    
    print("\n" + "=" * 60)
    print("🤖 LOADING MODEL")
    print("=" * 60)
    
    # Find which model file exists
    model_path = None
    for path in MODEL_PATHS:
        if os.path.exists(path):
            model_path = path
            print(f"📁 Found model: {path}")
            break
    
    if model_path is None:
        print("❌ No model file found!")
        return None
    
    try:
        predictor = DentalDiseasePredictor(model_path)
        print(f"✅ Model loaded from: {model_path}")
        return predictor
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        traceback.print_exc()
        return None

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/api/check-files")
async def check_files():
    """Check if static files are accessible"""
    import glob
    
    uploads = glob.glob("static/uploads/*")
    gradcam = glob.glob("static/gradcam/*")
    
    return JSONResponse({
        "static_directory": os.path.abspath("static"),
        "uploads": {
            "path": os.path.abspath("static/uploads"),
            "files": [os.path.basename(f) for f in uploads],
            "count": len(uploads)
        },
        "gradcam": {
            "path": os.path.abspath("static/gradcam"),
            "files": [os.path.basename(f) for f in gradcam],
            "count": len(gradcam)
        },
        "url_examples": {
            "upload_example": "/static/uploads/test_image.png",
            "gradcam_example": "/static/gradcam/test_gradcam.png"
        }
    })
@app.get("/health")
async def health_check():
    predictor_instance = load_model()
    
    if predictor_instance is None:
        return JSONResponse({
            "status": "error",
            "message": "Model not loaded",
            "tensorflow": tf.__version__
        })
    
    return JSONResponse({
        "status": "healthy",
        "message": "Server is running",
        "model_loaded": True,
        "tensorflow_version": tf.__version__
    })
@app.post("/api/analyze")
async def analyze_image(file: UploadFile = File(...)):
    print(f"\n📤 Received file: {file.filename}")
    
    # Load model
    predictor_instance = load_model()
    if predictor_instance is None:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "error": "Model not available"
            }
        )
    
    try:
        # Read file
        contents = await file.read()
        
        if len(contents) == 0:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "error": "Empty file"}
            )
        
        # Open image
        img = Image.open(io.BytesIO(contents)).convert('RGB')
        img_array = np.array(img)
        
        print(f"📏 Image loaded: {img_array.shape}")
        
        # Save original
        unique_id = str(uuid.uuid4())[:8]
        file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'png'
        original_name = f"original_{unique_id}.{file_ext}"
        original_path = os.path.join(UPLOAD_DIR, original_name)
        img.save(original_path)
        
        # Make prediction WITH REAL Grad-CAM
        print("🎯 Making prediction with Grad-CAM...")
        result = predictor_instance.predict_with_gradcam(img_array)
        
        if 'error' in result:
            print(f"❌ Prediction error: {result['error']}")
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "error": result['error']
                }
            )
        
        # Save BOTH visualizations
        gradcam_name = f"gradcam_{unique_id}.png"
        gradcam_path = os.path.join(GRADCAM_DIR, gradcam_name)
        result['gradcam_image'].save(gradcam_path)
        
        # Also save the simple superimposed image
        simple_name = f"simple_gradcam_{unique_id}.png"
        simple_path = os.path.join(GRADCAM_DIR, simple_name)
        result['simple_gradcam_image'].save(simple_path)
        
        print(f"✅ Prediction successful: {result['class']}")
        print(f"📍 Detected regions: {result['heatmap_data']['num_regions']}")
        
        # Return URLs
        original_url = f"uploads/{original_name}"
        gradcam_url = f"gradcam/{simple_name}"  # Use the simple version for web
        
        print(f"📁 Original saved: {original_path}")
        print(f"📁 GradCAM saved: {gradcam_path}")
        print(f"📁 Simple GradCAM saved: {simple_path}")
        
        # Return response WITH heatmap data
        return JSONResponse({
            "status": "success",
            "prediction": {
                "class": result['class'],
                "confidence": result['confidence'],
                "all_probabilities": result['all_probabilities'],
                "message": result['message']
            },
            "images": {
                "original": original_url,
                "gradcam": gradcam_url  # This now has green overlay
            },
            "heatmap_data": result['heatmap_data']  # Add heatmap data for green dots
        })
        
    except Exception as e:
        print(f"❌ Server error: {e}")
        traceback.print_exc()
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(e)
            }
        )
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Dental AI Server...")
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"📁 Model files:")
    
    for path in MODEL_PATHS:
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"  {exists} {path}")
    
    # Pre-load model
    load_model()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )