import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2
from PIL import Image
import time
from pathlib import Path
from typing import Dict, Any

# Disable TensorFlow warnings and logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

class ModelPredictor:
    def __init__(self):
        """Initialize model predictor with memory optimization"""
        self.model = None
        self.is_loaded = False
        self.class_names = ['Healthy', 'Gingivitis']
        self.img_size = (224, 224)
        self.confidence_threshold = 0.5
        
        # Force TensorFlow to use CPU only (important for i3)
        tf.config.set_visible_devices([], 'GPU')
        
        # Try to load model
        model_path = Path(__file__).parent / "models" / "GINGIVITIS_MODEL_AUGMENTED.keras"
        
        if model_path.exists():
            try:
                print(f"🔄 Loading model from: {model_path}")
                self.load_model(str(model_path))
            except Exception as e:
                print(f"❌ Error loading model: {e}")
                print("⚠️ Creating lightweight model for testing...")
                self._create_lightweight_model()
        else:
            print(f"⚠️ Model not found at: {model_path}")
            print("⚠️ Creating lightweight model for testing...")
            self._create_lightweight_model()
    
    def load_model(self, model_path: str):
        """Load the trained model with minimal memory usage"""
        try:
            # Load with minimal configuration
            self.model = keras.models.load_model(
                model_path,
                compile=False
            )
            
            # Simple compilation
            self.model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            
            # Warm up with small image
            dummy_input = np.ones((1, 224, 224, 3), dtype=np.float32) * 0.5
            _ = self.model.predict(dummy_input, verbose=0, batch_size=1)
            
            self.is_loaded = True
            print(f"✅ Model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error in load_model: {e}")
            self._create_lightweight_model()
    
    def _create_lightweight_model(self):
        """Create a very lightweight model for testing"""
        from tensorflow.keras import layers
        
        print("🛠️ Creating lightweight test model...")
        
        # Simple sequential model
        self.model = keras.Sequential([
            layers.Input(shape=(224, 224, 3)),
            layers.Rescaling(1./255),  # Simple normalization
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.is_loaded = False  # Mark as not the real model
        print("✅ Lightweight test model created")
    
    def preprocess_image_simple(self, image_path: str) -> np.ndarray:
        """Simple preprocessing to save memory"""
        try:
            # Read with PIL (lighter than OpenCV)
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize
            img = img.resize(self.img_size)
            
            # Convert to numpy array and normalize
            img_array = np.array(img, dtype=np.float32) / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            raise Exception(f"Error loading image: {str(e)}")
    
    def predict(self, image_path: str) -> Dict[str, Any]:
        """Make prediction with error handling"""
        start_time = time.time()
        
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                return self._error_result("Image file not found")
            
            # Get file size
            file_size = os.path.getsize(image_path) / (1024 * 1024)  # MB
            
            if file_size > 10:  # Limit to 10MB
                return self._error_result("Image too large (max 10MB)")
            
            # Preprocess image
            processed_image = self.preprocess_image_simple(image_path)
            
            # Make prediction with small batch size
            prediction = self.model.predict(
                processed_image, 
                verbose=0, 
                batch_size=1
            )
            
            probability = float(prediction[0][0])
            
            # Interpret results
            if probability > self.confidence_threshold:
                predicted_class = self.class_names[1]  # Gingivitis
                confidence = probability
            else:
                predicted_class = self.class_names[0]  # Healthy
                confidence = 1 - probability
            
            # Prepare result
            result = {
                "prediction": predicted_class,
                "confidence": round(confidence * 100, 2),
                "raw_probability": round(probability, 6),
                "healthy_probability": round((1 - probability) * 100, 2),
                "gingivitis_probability": round(probability * 100, 2),
                "processing_time_ms": round((time.time() - start_time) * 1000, 2),
                "model_loaded": self.is_loaded,
                "error": None,
                "interpretation": self._get_interpretation(confidence)
            }
            
            return result
            
        except Exception as e:
            return self._error_result(str(e))
    
    def _get_interpretation(self, confidence: float) -> str:
        """Get interpretation based on confidence"""
        if confidence > 0.9:
            return "High confidence prediction"
        elif confidence > 0.7:
            return "Moderate confidence prediction"
        elif confidence > 0.5:
            return "Low confidence prediction"
        else:
            return "Very low confidence - may need review"
    
    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        """Create error result"""
        return {
            "prediction": "Error",
            "confidence": 0.0,
            "error": error_msg,
            "model_loaded": self.is_loaded,
            "processing_time_ms": 0,
            "interpretation": "Error during processing"
        }