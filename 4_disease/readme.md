5. Installation & Running Instructions
   Step 1: Create folder structure:
   bash
   dental_disease_app/
   ├── app.py
   ├── model_loader.py
   ├── requirements.txt
   ├── templates/
   │ └── index.html
   ├── models/
   │ └── DENTAL_MODEL_BEST.keras # Your trained model
   └── static/
   └── uploads/
   Step 2: Install dependencies:
   bash
   pip install -r requirements.txt
   Step 3: Place your model:
   Copy your trained model to:

text
models/DENTAL_MODEL_BEST.keras
Step 4: Run the application:
bash

# Run with Python

python app.py

# Or with uvicorn

uvicorn app:app --host 127.0.0.1 --port 8000
Step 5: Access at:
text
http://localhost:8000
