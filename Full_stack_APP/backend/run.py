"""
Quick startup script for Dental & Gum Disease Classification System
Run this from the backend directory
"""

import sys
import os
from pathlib import Path

# Add the app directory to path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def check_models():
    """Check if model files exist"""
    models_dir = app_dir / "models"
    dental_model = models_dir / "DENTAL_MODEL_BEST.keras"
    gingivitis_model = models_dir / "GINGIVITIS_MODEL_AUGMENTED.keras"
    
    print("\n" + "=" * 60)
    print("🔍 Checking Model Files...")
    print("=" * 60)
    
    dental_exists = dental_model.exists()
    gingivitis_exists = gingivitis_model.exists()
    
    print(f"\n📁 Models Directory: {models_dir}")
    print(f"\n🦷 Dental Model (DENTAL_MODEL_BEST.keras):")
    print(f"   Status: {'✅ Found' if dental_exists else '❌ Not Found'}")
    if dental_exists:
        size_mb = dental_model.stat().st_size / (1024 * 1024)
        print(f"   Size: {size_mb:.1f} MB")
    
    print(f"\n🩺 Gingivitis Model (GINGIVITIS_MODEL_AUGMENTED.keras):")
    print(f"   Status: {'✅ Found' if gingivitis_exists else '❌ Not Found'}")
    if gingivitis_exists:
        size_mb = gingivitis_model.stat().st_size / (1024 * 1024)
        print(f"   Size: {size_mb:.1f} MB")
    
    if not dental_exists or not gingivitis_exists:
        print("\n⚠️  WARNING: Some models are missing!")
        print("   The system will run in TEST MODE with lightweight models.")
        print(f"   Please place your model files in: {models_dir}")
    
    print("\n" + "=" * 60)
    
    return dental_exists and gingivitis_exists

def main():
    """Main startup function"""
    print("\n🚀 Starting Dental & Gum Disease Classification System")
    
    # Check models
    models_ok = check_models()
    
    # Import and run the app
    try:
        print("\n📦 Loading application...")
        from main import app
        import uvicorn
        
        print("\n" + "=" * 60)
        print("✅ Application Ready!")
        print("=" * 60)
        print("\n🌐 Access the application at: http://localhost:8000")
        print("\n💡 Tips:")
        print("   - Select model type (Teeth or Gum) before uploading")
        print("   - Supported formats: JPG, PNG")
        print("   - Max file size: 10MB")
        print("   - Press Ctrl+C to stop the server")
        print("\n" + "=" * 60 + "\n")
        
        # Run the server
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=False,
            workers=1,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        print("   Thank you for using Dental AI System!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the backend directory")
        print("2. Activate virtual environment: .\\venv\\Scripts\\activate")
        print("3. Install dependencies: pip install -r requirements.txt")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
