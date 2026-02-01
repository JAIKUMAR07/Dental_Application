uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


inside backend 


# Create venv
python -m venv venv

# Activate venv
venv\Scripts\activate


# 🦷 Dental AI Web Application

A FastAPI web application for dental disease detection with Grad-CAM visualization.

## Features
- Upload dental images (drag & drop or browse)
- AI-powered disease classification (Caries, Calculus, Healthy, Discoloration)
- Grad-CAM visualization showing AI's focus areas
- Beautiful, responsive UI with Tailwind CSS
- Real-time probability bars and confidence scores

## Installation

### 1. Clone and Setup
```bash
# Create project directory
mkdir dental_ai_webapp
cd dental_ai_webapp

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate