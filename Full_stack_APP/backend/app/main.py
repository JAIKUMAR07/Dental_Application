import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import List

import aiofiles
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Import model loaders
from services.model_loader import DentalDiseasePredictor, GingivitisPredictor

# Initialize FastAPI app
app = FastAPI(
    title="Dental & Gum Disease Classifier",
    description="AI-powered detection for dental diseases and gingivitis",
    version="2.0.0"
)

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Setup static files and templates
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Initialize model predictors
print("=" * 60)
print("🦷 Starting Dental & Gum Disease Classification System")
print("=" * 60)

dental_predictor = DentalDiseasePredictor()
gingivitis_predictor = GingivitisPredictor()

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("\n📊 System Information:")
    print(f"   Upload directory: {UPLOAD_DIR}")
    print(f"   Dental model loaded: {dental_predictor.is_loaded}")
    print(f"   Gingivitis model loaded: {gingivitis_predictor.is_loaded}")
    print(f"   Dental classes: {', '.join(dental_predictor.class_names)}")
    print(f"   Gingivitis classes: {', '.join(gingivitis_predictor.class_names)}")
    print("\n✅ System ready! Access at: http://localhost:8000")
    print("=" * 60)

# API endpoint to get model info
@app.get("/api/models")
async def get_models():
    """Get information about available models"""
    dental_class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
    gingivitis_class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
    
    return JSONResponse({
        "dental": {
            "loaded": dental_predictor.is_loaded,
            "classes": dental_class_info,
            "name": "Teeth Disease Detection",
            "description": "4-class detection for dental conditions"
        },
        "gingivitis": {
            "loaded": gingivitis_predictor.is_loaded,
            "classes": gingivitis_class_info,
            "name": "Gum Disease Detection",
            "description": "Binary classification for gingivitis"
        }
    })

# API endpoint for single prediction
@app.post("/api/predict")
async def predict_api(
    file: UploadFile = File(...),
    model_type: str = Form(...)
):
    """API endpoint for single image prediction"""
    try:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if file.content_type not in allowed_types:
            return JSONResponse(
                status_code=400,
                content={"error": f"Invalid file type. Use: {', '.join(allowed_types)}"}
            )
        
        # Save file
        filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
        file_path = UPLOAD_DIR / filename
        
        async with aiofiles.open(file_path, 'wb') as buffer:
            content = await file.read()
            if len(content) > 10 * 1024 * 1024:  # 10MB limit
                return JSONResponse(
                    status_code=400,
                    content={"error": "File too large (max 10MB)"}
                )
            await buffer.write(content)
        
        # Select predictor based on model_type
        if model_type == "dental":
            result = dental_predictor.predict(str(file_path))
        elif model_type == "gingivitis":
            result = gingivitis_predictor.predict(str(file_path))
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid model type selected"}
            )
        
        # Add display info
        result["image_url"] = f"http://localhost:8000/static/uploads/{filename}"
        result["filename"] = file.filename
        result["upload_time"] = datetime.now().strftime("%H:%M:%S")
        result["selected_model"] = model_type
        
        return JSONResponse(result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error: {str(e)}"}
        )

# API endpoint for batch prediction
@app.post("/api/predict_batch")
async def predict_batch_api(
    files: List[UploadFile] = File(...),
    model_type: str = Form(...)
):
    """API endpoint for batch image prediction"""
    if not files:
        return JSONResponse(
            status_code=400,
            content={"error": "No files uploaded"}
        )
    
    # Select predictor
    if model_type == "dental":
        predictor = dental_predictor
    elif model_type == "gingivitis":
        predictor = gingivitis_predictor
    else:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid model type selected"}
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
                result = predictor.predict(str(file_path))
                
                # Add display info
                result["image_url"] = f"http://localhost:8000/static/uploads/{filename}"
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
    
    return JSONResponse({"results": results, "model_type": model_type})

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with model selection"""
    dental_class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
    gingivitis_class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Dental & Gum Disease Classifier",
            "dental_model_loaded": dental_predictor.is_loaded,
            "gingivitis_model_loaded": gingivitis_predictor.is_loaded,
            "dental_class_info": dental_class_info,
            "gingivitis_class_info": gingivitis_class_info
        }
    )

@app.post("/predict")
async def predict_single_image(
    request: Request,
    file: UploadFile = File(...),
    model_type: str = Form(...)
):
    """Predict single dental image with selected model"""
    try:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if file.content_type not in allowed_types:
            dental_class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
            gingivitis_class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
            
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": f"Invalid file type. Use: {', '.join(allowed_types)}",
                    "dental_model_loaded": dental_predictor.is_loaded,
                    "gingivitis_model_loaded": gingivitis_predictor.is_loaded,
                    "dental_class_info": dental_class_info,
                    "gingivitis_class_info": gingivitis_class_info
                }
            )
        
        # Save file
        filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
        file_path = UPLOAD_DIR / filename
        
        async with aiofiles.open(file_path, 'wb') as buffer:
            content = await file.read()
            if len(content) > 10 * 1024 * 1024:  # 10MB limit
                dental_class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
                gingivitis_class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
                
                return templates.TemplateResponse(
                    "index.html",
                    {
                        "request": request,
                        "error": "File too large (max 10MB)",
                        "dental_model_loaded": dental_predictor.is_loaded,
                        "gingivitis_model_loaded": gingivitis_predictor.is_loaded,
                        "dental_class_info": dental_class_info,
                        "gingivitis_class_info": gingivitis_class_info
                    }
                )
            await buffer.write(content)
        
        # Select predictor based on model_type
        if model_type == "dental":
            result = dental_predictor.predict(str(file_path))
            class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
        elif model_type == "gingivitis":
            result = gingivitis_predictor.predict(str(file_path))
            class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
        else:
            dental_class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
            gingivitis_class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
            
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": "Invalid model type selected",
                    "dental_model_loaded": dental_predictor.is_loaded,
                    "gingivitis_model_loaded": gingivitis_predictor.is_loaded,
                    "dental_class_info": dental_class_info,
                    "gingivitis_class_info": gingivitis_class_info
                }
            )
        
        # Add display info
        result["image_url"] = f"/static/uploads/{filename}"
        result["filename"] = file.filename
        result["upload_time"] = datetime.now().strftime("%H:%M:%S")
        result["selected_model"] = model_type
        
        dental_class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
        gingivitis_class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": result,
                "image_url": result["image_url"],
                "dental_model_loaded": dental_predictor.is_loaded,
                "gingivitis_model_loaded": gingivitis_predictor.is_loaded,
                "dental_class_info": dental_class_info,
                "gingivitis_class_info": gingivitis_class_info,
                "class_info": class_info
            }
        )
        
    except Exception as e:
        dental_class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
        gingivitis_class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Error: {str(e)}",
                "dental_model_loaded": dental_predictor.is_loaded,
                "gingivitis_model_loaded": gingivitis_predictor.is_loaded,
                "dental_class_info": dental_class_info,
                "gingivitis_class_info": gingivitis_class_info
            }
        )

@app.post("/predict_batch")
async def predict_batch_images(
    request: Request,
    files: List[UploadFile] = File(...),
    model_type: str = Form(...)
):
    """Predict multiple dental images"""
    if not files:
        dental_class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
        gingivitis_class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "No files uploaded",
                "dental_model_loaded": dental_predictor.is_loaded,
                "gingivitis_model_loaded": gingivitis_predictor.is_loaded,
                "dental_class_info": dental_class_info,
                "gingivitis_class_info": gingivitis_class_info
            }
        )
    
    # Select predictor
    if model_type == "dental":
        predictor = dental_predictor
        class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
    elif model_type == "gingivitis":
        predictor = gingivitis_predictor
        class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
    else:
        dental_class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
        gingivitis_class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Invalid model type selected",
                "dental_model_loaded": dental_predictor.is_loaded,
                "gingivitis_model_loaded": gingivitis_predictor.is_loaded,
                "dental_class_info": dental_class_info,
                "gingivitis_class_info": gingivitis_class_info
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
                result = predictor.predict(str(file_path))
                
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
    
    dental_class_info = [dental_predictor.get_class_info(c) for c in dental_predictor.class_names]
    gingivitis_class_info = [gingivitis_predictor.get_class_info(c) for c in gingivitis_predictor.class_names]
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "batch_results": results,
            "batch_mode": True,
            "selected_model": model_type,
            "dental_model_loaded": dental_predictor.is_loaded,
            "gingivitis_model_loaded": gingivitis_predictor.is_loaded,
            "dental_class_info": dental_class_info,
            "gingivitis_class_info": gingivitis_class_info,
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
        "dental_model_loaded": dental_predictor.is_loaded,
        "gingivitis_model_loaded": gingivitis_predictor.is_loaded,
        "dental_classes": dental_predictor.class_names,
        "gingivitis_classes": gingivitis_predictor.class_names,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        workers=1,
        log_level="info"
    )
