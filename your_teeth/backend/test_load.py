import tensorflow as tf
import numpy as np
from PIL import Image
import traceback

print("🔍 Testing Model Locally")
print("=" * 60)

# Load model
try:
    model = tf.keras.models.load_model(
        "DENTAL_MODEL_BEST.keras",
        compile=False,
        safe_mode=False
    )
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Model load failed: {e}")
    exit()

# Test with a sample image
def test_with_sample_image():
    # Create a test image (224x224 RGB)
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    # Apply EXACT same preprocessing as Colab
    image_tensor = tf.convert_to_tensor(test_image, dtype=tf.float32)
    image_tensor = tf.image.resize(image_tensor, [224, 224])
    image_tensor = tf.keras.applications.resnet.preprocess_input(image_tensor)
    image_tensor = tf.expand_dims(image_tensor, axis=0)
    
    # Predict
    predictions = model.predict(image_tensor, verbose=0)
    print(f"✅ Predictions shape: {predictions.shape}")
    print(f"✅ Sample prediction: {predictions[0]}")
    
    class_names = ['caries', 'calculus', 'healthy', 'discoloration']
    pred_idx = np.argmax(predictions[0])
    confidence = np.max(predictions[0])
    
    print(f"🎯 Prediction: {class_names[pred_idx]} ({confidence:.2%})")
    return True

# Run test
test_with_sample_image()