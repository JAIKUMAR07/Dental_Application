import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import tensorflow as tf
import numpy as np
from PIL import Image

print(f"TensorFlow version: {tf.__version__}")

# Test 1: Basic TensorFlow functionality
print("\n1️⃣ Testing TensorFlow...")
try:
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
    c = tf.matmul(a, b)
    print(f"✅ TensorFlow works: {c.numpy()}")
except Exception as e:
    print(f"❌ TensorFlow error: {e}")

# Test 2: Try to load any model
print("\n2️⃣ Testing model loading...")
model_files = [
    "DENTAL_MODEL_TF215.keras",
    "DENTAL_MODEL_BEST.keras", 
    "DENTAL_MODEL_COMPATIBLE.h5"
]

model = None
for model_file in model_files:
    if os.path.exists(model_file):
        print(f"  Trying {model_file}...")
        try:
            model = tf.keras.models.load_model(
                model_file,
                compile=False,
                safe_mode=False
            )
            print(f"  ✅ Loaded: {model_file}")
            print(f"  Input shape: {model.input_shape}")
            break
        except Exception as e:
            print(f"  ❌ Failed: {e}")

if model is None:
    print("❌ No model could be loaded")
else:
    # Test 3: Prediction
    print("\n3️⃣ Testing prediction...")
    try:
        # Create test image
        test_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        # Preprocess (EXACTLY like your Colab)
        img_tensor = tf.convert_to_tensor(test_img, dtype=tf.float32)
        img_tensor = tf.image.resize(img_tensor, [224, 224])
        img_tensor = tf.keras.applications.resnet.preprocess_input(img_tensor)
        img_tensor = tf.expand_dims(img_tensor, axis=0)
        
        # Predict
        prediction = model.predict(img_tensor, verbose=0)
        print(f"✅ Prediction works!")
        print(f"   Shape: {prediction.shape}")
        print(f"   Values: {prediction[0]}")
        
    except Exception as e:
        print(f"❌ Prediction test failed: {e}")

print("\n" + "="*60)
print("SUMMARY:")
print(f"TensorFlow: {tf.__version__}")
print(f"NumPy: {np.__version__}")
print(f"PIL: {Image.__version__}")
print("="*60)