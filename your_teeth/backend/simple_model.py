import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import tensorflow as tf
import numpy as np
from PIL import Image

class SimpleDentalPredictor:
    def __init__(self, model_path="DENTAL_MODEL_BEST.keras"):
        print("Loading model...")
        self.model = tf.keras.models.load_model(model_path, compile=False)
        self.class_names = ['caries', 'calculus', 'healthy', 'discoloration']
        print("✅ Model loaded!")
    
    def predict_simple(self, image_array):
        """Super simple prediction"""
        # Resize
        img = Image.fromarray(image_array).resize((224, 224))
        img_array = np.array(img).astype(np.float32)
        
        # Apply ResNet preprocessing
        img_array = tf.keras.applications.resnet50.preprocess_input(img_array)
        
        # Add batch dim
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predict
        predictions = self.model.predict(img_array, verbose=0)
        
        pred_idx = np.argmax(predictions[0])
        confidence = np.max(predictions[0])
        
        return {
            'class': self.class_names[pred_idx],
            'confidence': float(confidence)
        }

# Test it
if __name__ == "__main__":
    predictor = SimpleDentalPredictor()
    
    # Create test image
    test_img = np.random.randint(0, 255, (300, 400, 3), dtype=np.uint8)
    result = predictor.predict_simple(test_img)
    print(f"Test result: {result}")