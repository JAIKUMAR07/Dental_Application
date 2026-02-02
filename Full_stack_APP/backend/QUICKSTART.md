# 🚀 Quick Start Guide

## Dental & Gum Disease Classification System

### ⚡ Quick Setup (3 Steps)

#### Step 1: Run Setup Script

```powershell
# Double-click setup.bat OR run in PowerShell:
.\setup.bat
```

This will:

- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies

#### Step 2: Place Your Models

Copy your model files to `app\models\` directory:

- `DENTAL_MODEL_BEST.keras` (265 MB)
- `GINGIVITIS_MODEL_AUGMENTED.keras` (262 MB)

#### Step 3: Run the Application

```powershell
python run.py
```

Then open your browser to: **http://localhost:8000**

---

## 📖 Manual Setup (Alternative)

### 1. Create & Activate Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run Application

```powershell
python run.py
```

---

## 🎯 How to Use

1. **Select Model Type**
   - Click on "Teeth Disease" (4 classes) or "Gum Disease" (2 classes)

2. **Upload Image**
   - Single Image: Upload one image for analysis
   - Batch Analysis: Upload multiple images at once

3. **View Results**
   - See prediction with confidence score
   - View probability distribution for all classes
   - Detailed information about the detected condition

---

## 🦷 Model Types

### Teeth Disease (4 Classes)

- 🦷 **Caries**: Tooth decay or cavities
- 💎 **Calculus**: Tartar buildup
- ✅ **Healthy**: No visible issues
- 🎨 **Discoloration**: Stains or color changes

### Gum Disease (2 Classes)

- ✅ **Healthy**: Healthy gums
- ⚠️ **Gingivitis**: Gum inflammation

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── services/
│   │   ├── __init__.py
│   │   └── model_loader.py        # Dual model predictors
│   ├── models/                     # ⚠️ Place your .keras files here!
│   │   ├── DENTAL_MODEL_BEST.keras
│   │   └── GINGIVITIS_MODEL_AUGMENTED.keras
│   ├── __init__.py
│   └── main.py                     # FastAPI application
├── templates/
│   └── index.html                  # Web UI
├── static/
│   └── uploads/                    # Temporary storage
├── requirements.txt
├── run.py                          # ⭐ Start here!
├── setup.bat                       # ⭐ Setup script
└── README.md
```

---

## ❓ Troubleshooting

### "Model not found"

✅ **Solution**: Place model files in `app\models\` directory with exact names

### "Out of memory"

✅ **Solution**:

- Close other applications
- Use single image mode
- Restart the application

### "Python not found"

✅ **Solution**: Install Python 3.8+ from https://www.python.org/

### "Port 8000 already in use"

✅ **Solution**:

```powershell
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 🎨 Features

✨ **Dual Model Support**

- Switch between teeth and gum disease detection
- Real-time model selection

✨ **Batch Processing**

- Analyze multiple images at once
- Compare results side-by-side

✨ **Beautiful UI**

- Modern, responsive design
- Clear confidence visualizations
- Detailed probability charts

✨ **CPU Optimized**

- Works on low-end systems
- No GPU required
- Optimized for i3 processors

---

## 🛡️ Medical Disclaimer

⚠️ This tool is for **educational and screening purposes only**.

**Always consult with a qualified dental professional** for:

- Accurate diagnosis
- Treatment recommendations
- Professional medical advice

---

## 📞 Support

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review the main README.md
3. Ensure all requirements are met
4. Check console output for error messages

---

## 🎓 Educational Use

This system is designed for:

- Educational demonstrations
- Research purposes
- Learning AI/ML applications in healthcare
- Dental health awareness

---

**Ready to start? Run `setup.bat` and then `python run.py`!** 🚀
