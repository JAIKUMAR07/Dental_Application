import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import numpy as np
from PIL import Image
import tensorflow as tf
import io

print("Testing FastAPI-compatible prediction...")

# Load model
model = tf.keras.models.load_model("DENTAL_MODEL_BEST.keras", compile=False)

def predict_image_fastapi(image_bytes):
    """Function that mimics FastAPI's file handling"""
    try:
        # Step 1: Read bytes (like FastAPI does)
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img_array = np.array(image)
        
        print(f"1. Image loaded: {img_array.shape}, {img_array.dtype}")
        
        # Step 2: Preprocess (Colab method)
        image_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)
        image_tensor = tf.image.resize(image_tensor, [224, 224])
        image_tensor = tf.keras.applications.resnet.preprocess_input(image_tensor)
        image_tensor = tf.expand_dims(image_tensor, axis=0)
        
        print(f"2. Tensor ready: {image_tensor.shape}")
        
        # Step 3: Predict
        predictions = model.predict(image_tensor, verbose=0)
        
        # Step 4: Format results
        class_names = ['caries', 'calculus', 'healthy', 'discoloration']
        pred_idx = np.argmax(predictions[0])
        confidence = np.max(predictions[0])
        
        return {
            'class': class_names[pred_idx],
            'confidence': float(confidence),
            'all_probabilities': {class_names[i]: float(p) for i, p in enumerate(predictions[0])}
        }
        
    except Exception as e:
        return {'error': str(e)}

# Create a test image
print("\nCreating test image...")
test_img = Image.new('RGB', (500, 500), color='red')
img_byte_arr = io.BytesIO()
test_img.save(img_byte_arr, format='JPEG')
img_byte_arr = img_byte_arr.getvalue()

print(f"Test image bytes: {len(img_byte_arr)} bytes")

# Test prediction
result = predict_image_fastapi(img_byte_arr)
print(f"\nResult: {result}")

if 'error' not in result:
    print("✅ FastAPI-style prediction works!")
else:
    print(f"❌ Error: {result['error']}")