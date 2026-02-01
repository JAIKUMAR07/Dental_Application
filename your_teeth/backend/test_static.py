import os
from pathlib import Path

print("🔍 Checking static files structure...")
print(f"Current directory: {os.getcwd()}")

# Check if static directory exists
static_dir = Path("static")
if not static_dir.exists():
    print("❌ static/ directory not found!")
    print("Creating static directories...")
    os.makedirs("static/uploads", exist_ok=True)
    os.makedirs("static/gradcam", exist_ok=True)
    print("✅ Created static directories")
else:
    print("✅ static/ directory exists")

# List contents
print("\n📁 Contents of static/:")
for root, dirs, files in os.walk("static"):
    level = root.replace("static", "").count(os.sep)
    indent = " " * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = " " * 2 * (level + 1)
    for file in files:
        print(f"{subindent}{file}")

# Test creating a dummy image
print("\n🧪 Creating test image...")
from PIL import Image
import numpy as np

# Create test image in uploads
test_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
img = Image.fromarray(test_img)
img.save("static/uploads/test_image.png")
print("✅ Created test_image.png in static/uploads/")

# Verify it's accessible via URL
print("\n🔗 Test URLs:")
print("  Original: http://localhost:8001/static/uploads/test_image.png")
print("  GradCAM:  http://localhost:8001/static/gradcam/gradcam_example.png")