import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import time
from pathlib import Path
from typing import Dict, Any, List

# Disable TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

class DentalDiseasePredictor:
    def __init__(self):
        """Initialize model predictor for 4-class dental disease classification"""
        self.model = None
        self.is_loaded = False
        self.class_names = ['caries', 'calculus', 'healthy', 'discoloration']
        self.class_colors = {
            'caries': '#ff6b6b',        # Red
            'calculus': '#ffa500',      # Orange
            'healthy': '#51cf66',       # Green
            'discoloration': '#4ecdc4'  # Teal
        }
        self.class_icons = {
            'caries': '🦷',
            'calculus': '💎',
            'healthy': '✅',
            'discoloration': '🎨'
        }
        self.class_descriptions = {
            'caries': 'Tooth decay or cavities',
            'calculus': 'Tartar buildup on teeth',
            'healthy': 'No visible dental issues',
            'discoloration': 'Stains or color changes'
        }
        self.img_size = (224, 224)
        
        # Force CPU usage
        tf.config.set_visible_devices([], 'GPU')
        
        # Try to load model
        model_path = Path(__file__).parent / "models" / "DENTAL_MODEL_BEST.keras"
        
        if model_path.exists():
            try:
                print(f"🔄 Loading dental disease model from: {model_path}")
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
        """Load the trained ResNet50 model"""
        try:
            # Load with minimal configuration
            self.model = keras.models.load_model(
                model_path,
                compile=False
            )
            
            # Simple compilation
            self.model.compile(
                optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )
            
            # Warm up
            dummy_input = np.ones((1, 224, 224, 3), dtype=np.float32) * 0.5
            _ = self.model.predict(dummy_input, verbose=0, batch_size=1)
            
            self.is_loaded = True
            print(f"✅ Dental disease model loaded successfully!")
            print(f"   Classes: {self.class_names}")
            print(f"   Input shape: {self.model.input_shape}")
            
        except Exception as e:
            print(f"❌ Error in load_model: {e}")
            self._create_lightweight_model()
    
    def _create_lightweight_model(self):
        """Create lightweight model for testing"""
        from tensorflow.keras import layers
        
        print("🛠️ Creating lightweight dental model for testing...")
        
        self.model = keras.Sequential([
            layers.Input(shape=(224, 224, 3)),
            layers.Rescaling(1./255),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(4, activation='softmax')  # 4 classes
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.is_loaded = False
        print("✅ Lightweight dental model created")
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for ResNet50 model"""
        try:
            # Read image
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize
            img = img.resize(self.img_size)
            
            # Convert to numpy array
            img_array = np.array(img, dtype=np.float32)
            
            # Apply ResNet50 preprocessing
            img_array = tf.keras.applications.resnet.preprocess_input(img_array)
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")
    
    def predict(self, image_path: str) -> Dict[str, Any]:
        """Make prediction on dental image"""
        start_time = time.time()
        
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                return self._error_result("Image file not found")
            
            # Get file size (max 10MB)
            file_size = os.path.getsize(image_path) / (1024 * 1024)
            if file_size > 10:
                return self._error_result("Image too large (max 10MB)")
            
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            
            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0, batch_size=1)
            
            # Get results
            predicted_idx = np.argmax(predictions[0])
            predicted_class = self.class_names[predicted_idx]
            confidence = float(predictions[0][predicted_idx])
            
            # Get all probabilities
            all_probabilities = {
                self.class_names[i]: float(prob) 
                for i, prob in enumerate(predictions[0])
            }
            
            # Sort by probability
            sorted_probs = dict(sorted(all_probabilities.items(), key=lambda x: x[1], reverse=True))
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000
            
            # Prepare result
            result = {
                "prediction": predicted_class,
                "confidence": round(confidence * 100, 2),
                "all_probabilities": sorted_probs,
                "top_probabilities": list(sorted_probs.items())[:3],  # Top 3
                "icon": self.class_icons[predicted_class],
                "color": self.class_colors[predicted_class],
                "description": self.class_descriptions[predicted_class],
                "processing_time_ms": round(processing_time, 2),
                "model_loaded": self.is_loaded,
                "error": None
            }
            
            return result
            
        except Exception as e:
            return self._error_result(str(e))
    
    def predict_batch(self, image_paths: List[str]) -> List[Dict[str, Any]]:
        """Predict multiple images"""
        results = []
        for path in image_paths:
            results.append(self.predict(path))
        return results
    
    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        """Create error result"""
        return {
            "prediction": "Error",
            "confidence": 0.0,
            "error": error_msg,
            "model_loaded": self.is_loaded,
            "processing_time_ms": 0,
            "description": "Error during processing"
        }
    
    def get_class_info(self, class_name: str) -> Dict[str, Any]:
        """Get information about a disease class"""
        return {
            "name": class_name,
            "icon": self.class_icons.get(class_name, "❓"),
            "color": self.class_colors.get(class_name, "#666666"),
            "description": self.class_descriptions.get(class_name, "Unknown condition")
        }