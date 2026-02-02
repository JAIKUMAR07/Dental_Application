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
    """Predictor for 4-class dental disease classification"""
    
    def __init__(self):
        self.model = None
        self.is_loaded = False
        self.class_names = ['caries', 'calculus', 'healthy', 'discoloration']
        self.class_colors = {
            'caries': '#ff6b6b',
            'calculus': '#ffa500',
            'healthy': '#51cf66',
            'discoloration': '#4ecdc4'
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
        model_path = Path(__file__).parent.parent / "models" / "DENTAL_MODEL_BEST.keras"
        
        if model_path.exists():
            try:
                print(f"🔄 Loading dental disease model from: {model_path}")
                self.load_model(str(model_path))
            except Exception as e:
                print(f"❌ Error loading dental model: {e}")
                print("⚠️ Creating lightweight model for testing...")
                self._create_lightweight_model()
        else:
            print(f"⚠️ Dental model not found at: {model_path}")
            print("⚠️ Creating lightweight model for testing...")
            self._create_lightweight_model()
    
    def load_model(self, model_path: str):
        try:
            self.model = keras.models.load_model(model_path, compile=False)
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
            
        except Exception as e:
            print(f"❌ Error in load_model: {e}")
            self._create_lightweight_model()
    
    def _create_lightweight_model(self):
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
            layers.Dense(4, activation='softmax')
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.is_loaded = False
        print("✅ Lightweight dental model created")
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        try:
            img = Image.open(image_path)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img = img.resize(self.img_size)
            img_array = np.array(img, dtype=np.float32)
            img_array = tf.keras.applications.resnet.preprocess_input(img_array)
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")
    
    def predict(self, image_path: str) -> Dict[str, Any]:
        start_time = time.time()
        
        try:
            if not os.path.exists(image_path):
                return self._error_result("Image file not found")
            
            file_size = os.path.getsize(image_path) / (1024 * 1024)
            if file_size > 10:
                return self._error_result("Image too large (max 10MB)")
            
            processed_image = self.preprocess_image(image_path)
            predictions = self.model.predict(processed_image, verbose=0, batch_size=1)
            
            predicted_idx = np.argmax(predictions[0])
            predicted_class = self.class_names[predicted_idx]
            confidence = float(predictions[0][predicted_idx])
            
            all_probabilities = {
                self.class_names[i]: float(prob) 
                for i, prob in enumerate(predictions[0])
            }
            
            sorted_probs = dict(sorted(all_probabilities.items(), key=lambda x: x[1], reverse=True))
            processing_time = (time.time() - start_time) * 1000
            
            result = {
                "prediction": predicted_class,
                "confidence": round(confidence * 100, 2),
                "all_probabilities": sorted_probs,
                "top_probabilities": list(sorted_probs.items())[:3],
                "icon": self.class_icons[predicted_class],
                "color": self.class_colors[predicted_class],
                "description": self.class_descriptions[predicted_class],
                "processing_time_ms": round(processing_time, 2),
                "model_loaded": self.is_loaded,
                "model_type": "dental",
                "error": None
            }
            
            return result
            
        except Exception as e:
            return self._error_result(str(e))
    
    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        return {
            "prediction": "Error",
            "confidence": 0.0,
            "error": error_msg,
            "model_loaded": self.is_loaded,
            "processing_time_ms": 0,
            "description": "Error during processing",
            "model_type": "dental"
        }
    
    def get_class_info(self, class_name: str) -> Dict[str, Any]:
        return {
            "name": class_name,
            "icon": self.class_icons.get(class_name, "❓"),
            "color": self.class_colors.get(class_name, "#666666"),
            "description": self.class_descriptions.get(class_name, "Unknown condition")
        }


class GingivitisPredictor:
    """Predictor for gingivitis detection (binary classification)"""
    
    def __init__(self):
        self.model = None
        self.is_loaded = False
        self.class_names = ['Healthy', 'Gingivitis']
        self.class_colors = {
            'Healthy': '#51cf66',
            'Gingivitis': '#ff6b6b'
        }
        self.class_icons = {
            'Healthy': '✅',
            'Gingivitis': '⚠️'
        }
        self.class_descriptions = {
            'Healthy': 'Healthy gums - no signs of gingivitis',
            'Gingivitis': 'Gum inflammation detected'
        }
        self.img_size = (224, 224)
        self.confidence_threshold = 0.5
        
        # Force CPU usage
        tf.config.set_visible_devices([], 'GPU')
        
        # Try to load model
        model_path = Path(__file__).parent.parent / "models" / "GINGIVITIS_MODEL_AUGMENTED.keras"
        
        if model_path.exists():
            try:
                print(f"🔄 Loading gingivitis model from: {model_path}")
                self.load_model(str(model_path))
            except Exception as e:
                print(f"❌ Error loading gingivitis model: {e}")
                print("⚠️ Creating lightweight model for testing...")
                self._create_lightweight_model()
        else:
            print(f"⚠️ Gingivitis model not found at: {model_path}")
            print("⚠️ Creating lightweight model for testing...")
            self._create_lightweight_model()
    
    def load_model(self, model_path: str):
        try:
            self.model = keras.models.load_model(model_path, compile=False)
            self.model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            
            # Warm up
            dummy_input = np.ones((1, 224, 224, 3), dtype=np.float32) * 0.5
            _ = self.model.predict(dummy_input, verbose=0, batch_size=1)
            
            self.is_loaded = True
            print(f"✅ Gingivitis model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error in load_model: {e}")
            self._create_lightweight_model()
    
    def _create_lightweight_model(self):
        from tensorflow.keras import layers
        
        print("🛠️ Creating lightweight gingivitis model for testing...")
        
        self.model = keras.Sequential([
            layers.Input(shape=(224, 224, 3)),
            layers.Rescaling(1./255),
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
        
        self.is_loaded = False
        print("✅ Lightweight gingivitis model created")
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        try:
            img = Image.open(image_path)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img = img.resize(self.img_size)
            img_array = np.array(img, dtype=np.float32) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            raise Exception(f"Error loading image: {str(e)}")
    
    def predict(self, image_path: str) -> Dict[str, Any]:
        start_time = time.time()
        
        try:
            if not os.path.exists(image_path):
                return self._error_result("Image file not found")
            
            file_size = os.path.getsize(image_path) / (1024 * 1024)
            if file_size > 10:
                return self._error_result("Image too large (max 10MB)")
            
            processed_image = self.preprocess_image(image_path)
            prediction = self.model.predict(processed_image, verbose=0, batch_size=1)
            
            probability = float(prediction[0][0])
            
            if probability > self.confidence_threshold:
                predicted_class = self.class_names[1]  # Gingivitis
                confidence = probability
            else:
                predicted_class = self.class_names[0]  # Healthy
                confidence = 1 - probability
            
            processing_time = (time.time() - start_time) * 1000
            
            all_probabilities = {
                'Healthy': round((1 - probability) * 100, 2),
                'Gingivitis': round(probability * 100, 2)
            }
            
            result = {
                "prediction": predicted_class,
                "confidence": round(confidence * 100, 2),
                "all_probabilities": all_probabilities,
                "raw_probability": round(probability, 6),
                "healthy_probability": round((1 - probability) * 100, 2),
                "gingivitis_probability": round(probability * 100, 2),
                "icon": self.class_icons[predicted_class],
                "color": self.class_colors[predicted_class],
                "description": self.class_descriptions[predicted_class],
                "processing_time_ms": round(processing_time, 2),
                "model_loaded": self.is_loaded,
                "model_type": "gingivitis",
                "error": None,
                "interpretation": self._get_interpretation(confidence)
            }
            
            return result
            
        except Exception as e:
            return self._error_result(str(e))
    
    def _get_interpretation(self, confidence: float) -> str:
        if confidence > 0.9:
            return "High confidence prediction"
        elif confidence > 0.7:
            return "Moderate confidence prediction"
        elif confidence > 0.5:
            return "Low confidence prediction"
        else:
            return "Very low confidence - may need review"
    
    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        return {
            "prediction": "Error",
            "confidence": 0.0,
            "error": error_msg,
            "model_loaded": self.is_loaded,
            "processing_time_ms": 0,
            "interpretation": "Error during processing",
            "model_type": "gingivitis"
        }
    
    def get_class_info(self, class_name: str) -> Dict[str, Any]:
        return {
            "name": class_name,
            "icon": self.class_icons.get(class_name, "❓"),
            "color": self.class_colors.get(class_name, "#666666"),
            "description": self.class_descriptions.get(class_name, "Unknown condition")
        }
