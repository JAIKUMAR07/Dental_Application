import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress all warnings
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Force CPU

import tensorflow as tf
import numpy as np
from PIL import Image
import traceback
import json

print("=" * 70)
print("🔍 DENTAL MODEL DIAGNOSTIC SCRIPT")
print("=" * 70)

# Step 1: Check TensorFlow version
print("\n1️⃣ TENSORFLOW INFO:")
print(f"   Version: {tf.__version__}")
print(f"   Built with CUDA: {tf.test.is_built_with_cuda()}")
print(f"   GPU Available: {len(tf.config.list_physical_devices('GPU')) > 0}")

# Step 2: Check if model file exists
model_path = "DENTAL_MODEL_BEST.keras"
print(f"\n2️⃣ MODEL FILE CHECK:")
print(f"   Looking for: {model_path}")
print(f"   File exists: {os.path.exists(model_path)}")
print(f"   File size: {os.path.getsize(model_path) if os.path.exists(model_path) else 0:,} bytes")

if not os.path.exists(model_path):
    print("❌ ERROR: Model file not found!")
    print("   Please ensure DENTAL_MODEL_BEST.keras is in the same folder")
    exit()

# Step 3: Try to load the model
print("\n3️⃣ LOADING MODEL...")
try:
    # Try different loading methods
    print("   Method 1: Standard load...")
    model = tf.keras.models.load_model(model_path, compile=False)
    print("   ✅ Standard load successful!")
    
    # Check model details
    print(f"\n   Model Name: {model.name}")
    print(f"   Input Shape: {model.input_shape}")
    print(f"   Output Shape: {model.output_shape}")
    print(f"   Number of Layers: {len(model.layers)}")
    print(f"   Trainable Params: {model.count_params():,}")
    
except Exception as e1:
    print(f"   ❌ Standard load failed: {e1}")
    
    try:
        print("\n   Method 2: Load with safe_mode=False...")
        model = tf.keras.models.load_model(
            model_path, 
            compile=False,
            safe_mode=False
        )
        print("   ✅ Load with safe_mode=False successful!")
        
    except Exception as e2:
        print(f"   ❌ Second attempt failed: {e2}")
        
        try:
            print("\n   Method 3: Try to load weights only...")
            # Create a dummy model with same architecture
            from tensorflow.keras.applications import ResNet50
            from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
            
            base_model = ResNet50(weights=None, include_top=False, input_shape=(224, 224, 3))
            base_model.trainable = False
            
            inputs = tf.keras.Input(shape=(224, 224, 3))
            x = tf.keras.applications.resnet50.preprocess_input(inputs)
            x = base_model(x, training=False)
            x = GlobalAveragePooling2D()(x)
            x = Dense(256, activation='relu')(x)
            x = Dropout(0.5)(x)
            outputs = Dense(4, activation='softmax')(x)
            
            model = tf.keras.Model(inputs, outputs)
            model.load_weights(model_path)
            print("   ✅ Loaded weights successfully!")
            
        except Exception as e3:
            print(f"   ❌ All loading methods failed: {e3}")
            traceback.print_exc()
            exit()

# Step 4: Test prediction with sample image
print("\n4️⃣ TESTING PREDICTION...")
try:
    # Create a test image
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    print(f"   Test image shape: {test_image.shape}")
    print(f"   Test image dtype: {test_image.dtype}")
    
    # Preprocess EXACTLY like your Colab code
    print("\n   Preprocessing (Colab method):")
    print("   1. Convert to tensor (float32)...")
    image_tensor = tf.convert_to_tensor(test_image, dtype=tf.float32)
    
    print("   2. Resize to 224x224...")
    image_tensor = tf.image.resize(image_tensor, [224, 224])
    
    print("   3. Apply ResNet preprocessing...")
    image_tensor = tf.keras.applications.resnet.preprocess_input(image_tensor)
    
    print("   4. Add batch dimension...")
    image_tensor = tf.expand_dims(image_tensor, axis=0)
    
    print(f"\n   Final tensor shape: {image_tensor.shape}")
    print(f"   Tensor dtype: {image_tensor.dtype}")
    print(f"   Tensor range: [{tf.reduce_min(image_tensor):.2f}, {tf.reduce_max(image_tensor):.2f}]")
    
    # Make prediction
    print("\n   Making prediction...")
    predictions = model.predict(image_tensor, verbose=0)
    
    print(f"   ✅ Prediction successful!")
    print(f"   Predictions shape: {predictions.shape}")
    
    class_names = ['caries', 'calculus', 'healthy', 'discoloration']
    pred_idx = np.argmax(predictions[0])
    confidence = np.max(predictions[0])
    
    print(f"\n   🎯 RESULT:")
    print(f"   Predicted class: {class_names[pred_idx]}")
    print(f"   Confidence: {confidence:.2%}")
    print(f"\n   All probabilities:")
    for i, (cls, prob) in enumerate(zip(class_names, predictions[0])):
        print(f"   {i+1}. {cls:12}: {prob:.2%}")
    
    # Save model info to file
    model_info = {
        "status": "success",
        "tensorflow_version": tf.__version__,
        "model_loaded": True,
        "input_shape": str(model.input_shape),
        "output_shape": str(model.output_shape),
        "layers": len(model.layers),
        "test_prediction": {
            "class": class_names[pred_idx],
            "confidence": float(confidence),
            "probabilities": {cls: float(prob) for cls, prob in zip(class_names, predictions[0])}
        }
    }
    
    with open("model_debug_info.json", "w") as f:
        json.dump(model_info, f, indent=2)
    
    print(f"\n✅ Diagnostic completed successfully!")
    print(f"📄 Debug info saved to: model_debug_info.json")
    
except Exception as e:
    print(f"❌ Prediction test failed: {e}")
    traceback.print_exc()
    
    # Try simpler test
    print("\n🔄 Trying simpler test...")
    try:
        # Just forward pass without preprocessing
        dummy_input = np.random.randn(1, 224, 224, 3).astype(np.float32)
        output = model(dummy_input)
        print(f"✅ Forward pass works! Output shape: {output.shape}")
    except Exception as e2:
        print(f"❌ Forward pass also failed: {e2}")

print("\n" + "=" * 70)
print("📊 DIAGNOSTIC SUMMARY")
print("=" * 70)
print("If this script works but your web app doesn't, the issue is likely:")
print("1. Memory limits on i3 processor")
print("2. Image preprocessing mismatch")
print("3. File upload handling in FastAPI")
print("\nRun this next: python test_fastapi_simple.py")