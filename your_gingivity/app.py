import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import List

import aiofiles
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import model loader AFTER TensorFlow settings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from model_loader import ModelPredictor

# Initialize FastAPI app
app = FastAPI(
    title="Gingivitis Detection",
    description="Simple dental image analysis",
    version="1.0.0"
)

# Create necessary directories
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Setup static files and templates
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Initialize model predictor (this will show startup messages)
print("=" * 50)
print("Starting Gingivitis Detection Application")
print("=" * 50)

# Initialize model
model_predictor = ModelPredictor()

# Store model reference in app state
app.state.model = model_predictor

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("\n📊 Application Info:")
    print(f"   Upload directory: {UPLOAD_DIR}")
    print(f"   Model loaded: {model_predictor.is_loaded}")
    print(f"   Using {'REAL' if model_predictor.is_loaded else 'TEST'} model")
    print("\n✅ Application ready! Access at: http://localhost:8000")
    print("=" * 50)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Gingivitis Detection",
            "model_loaded": model_predictor.is_loaded
        }
    )

@app.post("/predict")
async def predict_single_image(
    request: Request,
    file: UploadFile = File(...)
):
    """Predict single image"""
    try:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if file.content_type not in allowed_types:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": f"Invalid file type. Use: {', '.join(allowed_types)}",
                    "model_loaded": model_predictor.is_loaded
                }
            )
        
        # Save file
        filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
        file_path = UPLOAD_DIR / filename
        
        async with aiofiles.open(file_path, 'wb') as buffer:
            content = await file.read()
            if len(content) > 10 * 1024 * 1024:  # 10MB limit
                return templates.TemplateResponse(
                    "index.html",
                    {
                        "request": request,
                        "error": "File too large (max 10MB)",
                        "model_loaded": model_predictor.is_loaded
                    }
                )
            await buffer.write(content)
        
        # Predict
        result = model_predictor.predict(str(file_path))
        
        # Add display info
        result["image_url"] = f"/static/uploads/{filename}"
        result["filename"] = file.filename
        result["upload_time"] = datetime.now().strftime("%H:%M:%S")
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": result,
                "image_url": result["image_url"],
                "model_loaded": model_predictor.is_loaded
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Error: {str(e)}",
                "model_loaded": model_predictor.is_loaded
            }
        )

@app.get("/clear")
async def clear_files():
    """Clear uploaded files"""
    deleted = 0
    for file_path in UPLOAD_DIR.iterdir():
        if file_path.is_file():
            try:
                file_path.unlink()
                deleted += 1
            except:
                pass
    
    return JSONResponse({
        "message": f"Cleared {deleted} files",
        "status": "success"
    })

@app.get("/health")
async def health_check():
    """Health check"""
    return JSONResponse({
        "status": "running",
        "model_loaded": model_predictor.is_loaded,
        "timestamp": datetime.now().isoformat()
    })

# For Windows, run with: python app.py
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host="127.0.0.1",  # Use localhost instead of 0.0.0.0
        port=8000,
        reload=False,  # Disable reload for stability
        workers=1,     # Single worker for i3
        log_level="info"
    )