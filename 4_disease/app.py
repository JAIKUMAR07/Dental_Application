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

# Import model loader
from model_loader import DentalDiseasePredictor

# Initialize FastAPI app
app = FastAPI(
    title="Dental Disease Classifier",
    description="AI-powered detection of caries, calculus, healthy teeth, and discoloration",
    version="1.0.0"
)

# Create necessary directories
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Setup static files and templates
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Initialize model predictor
print("=" * 50)
print("🦷 Starting Dental Disease Classification System")
print("=" * 50)

model_predictor = DentalDiseasePredictor()

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("\n📊 System Information:")
    print(f"   Upload directory: {UPLOAD_DIR}")
    print(f"   Model loaded: {model_predictor.is_loaded}")
    print(f"   Classes: {', '.join(model_predictor.class_names)}")
    print(f"   Using {'REAL' if model_predictor.is_loaded else 'TEST'} model")
    print("\n✅ System ready! Access at: http://localhost:8000")
    print("=" * 50)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    # Get class information for display
    class_info = []
    for class_name in model_predictor.class_names:
        info = model_predictor.get_class_info(class_name)
        class_info.append(info)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Dental Disease Classifier",
            "model_loaded": model_predictor.is_loaded,
            "class_info": class_info
        }
    )

@app.post("/predict")
async def predict_single_image(
    request: Request,
    file: UploadFile = File(...)
):
    """Predict single dental image"""
    try:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if file.content_type not in allowed_types:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": f"Invalid file type. Use: {', '.join(allowed_types)}",
                    "model_loaded": model_predictor.is_loaded,
                    "class_info": [model_predictor.get_class_info(c) for c in model_predictor.class_names]
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
                        "model_loaded": model_predictor.is_loaded,
                        "class_info": [model_predictor.get_class_info(c) for c in model_predictor.class_names]
                    }
                )
            await buffer.write(content)
        
        # Predict
        result = model_predictor.predict(str(file_path))
        
        # Add display info
        result["image_url"] = f"/static/uploads/{filename}"
        result["filename"] = file.filename
        result["upload_time"] = datetime.now().strftime("%H:%M:%S")
        
        # Get class info
        class_info = [model_predictor.get_class_info(c) for c in model_predictor.class_names]
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": result,
                "image_url": result["image_url"],
                "model_loaded": model_predictor.is_loaded,
                "class_info": class_info
            }
        )
        
    except Exception as e:
        class_info = [model_predictor.get_class_info(c) for c in model_predictor.class_names]
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Error: {str(e)}",
                "model_loaded": model_predictor.is_loaded,
                "class_info": class_info
            }
        )

@app.post("/predict_batch")
async def predict_batch_images(
    request: Request,
    files: List[UploadFile] = File(...)
):
    """Predict multiple dental images"""
    if not files:
        class_info = [model_predictor.get_class_info(c) for c in model_predictor.class_names]
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "No files uploaded",
                "model_loaded": model_predictor.is_loaded,
                "class_info": class_info
            }
        )
    
    results = []
    for file in files:
        if file.content_type.startswith("image/"):
            try:
                # Save file
                filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
                file_path = UPLOAD_DIR / filename
                
                async with aiofiles.open(file_path, 'wb') as buffer:
                    content = await file.read()
                    await buffer.write(content)
                
                # Predict
                result = model_predictor.predict(str(file_path))
                
                # Add display info
                result["image_url"] = f"/static/uploads/{filename}"
                result["filename"] = file.filename
                result["upload_time"] = datetime.now().strftime("%H:%M:%S")
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "error": str(e),
                    "prediction": "Error",
                    "confidence": 0.0
                })
    
    # Get class info
    class_info = [model_predictor.get_class_info(c) for c in model_predictor.class_names]
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "batch_results": results,
            "batch_mode": True,
            "model_loaded": model_predictor.is_loaded,
            "class_info": class_info
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
        "classes": model_predictor.class_names,
        "timestamp": datetime.now().isoformat()
    })

@app.get("/class_info/{class_name}")
async def get_class_information(class_name: str):
    """Get information about a specific dental condition"""
    info = model_predictor.get_class_info(class_name)
    return JSONResponse(info)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        workers=1,
        log_level="info"
    )