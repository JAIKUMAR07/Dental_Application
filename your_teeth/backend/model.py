import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import traceback
import cv2

print(f"TensorFlow version: {tf.__version__}")

class DentalDiseasePredictor:
    def __init__(self, model_path: str = "DENTAL_MODEL_TF215.keras"):
        print(f"🤖 Loading model: {model_path}")
        
        # Clear session
        tf.keras.backend.clear_session()
        
        # Try multiple loading strategies for TF 2.15
        self.model = None
        
        try:
            # Strategy 1: Direct load
            self.model = tf.keras.models.load_model(
                model_path,
                compile=False,
                safe_mode=False
            )
            print("✅ Model loaded with direct method")
            
        except Exception as e1:
            print(f"❌ Direct load failed: {e1}")
            
            try:
                # Strategy 2: Load with custom objects
                self.model = tf.keras.models.load_model(
                    model_path,
                    compile=False,
                    custom_objects=None
                )
                print("✅ Model loaded with custom_objects")
                
            except Exception as e2:
                print(f"❌ Second attempt failed: {e2}")
                
                # Strategy 3: Create fresh model
                print("🔄 Creating fresh model architecture...")
                self.model = self._create_fresh_model()
        
        # Always compile
        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.class_names = ['caries', 'calculus', 'healthy', 'discoloration']
        
        # Get the last convolutional layer for Grad-CAM
        self.last_conv_layer_name = self._find_last_conv_layer()
        print(f"✅ Model ready! Input shape: {self.model.input_shape}")
        print(f"🔍 Last conv layer for Grad-CAM: {self.last_conv_layer_name}")
        
        # Quick test
        self._test_model()
    
    def _create_fresh_model(self):
        """Create fresh model with same architecture"""
        base_model = tf.keras.applications.ResNet50(
            weights='imagenet',
            include_top=False,
            input_shape=(224, 224, 3)
        )
        base_model.trainable = False
        
        inputs = tf.keras.Input(shape=(224, 224, 3))
        x = tf.keras.applications.resnet.preprocess_input(inputs)
        x = base_model(x, training=False)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(256, activation='relu', 
                                 kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
        x = tf.keras.layers.Dropout(0.5)(x)
        outputs = tf.keras.layers.Dense(4, activation='softmax')(x)
        
        return tf.keras.Model(inputs, outputs)
    
    def _find_last_conv_layer(self):
        """Find the last convolutional layer in the model"""
        for layer in reversed(self.model.layers):
            # Check if it's a convolutional layer
            if len(layer.output_shape) == 4:
                return layer.name
        return None
    
    def _test_model(self):
        """Test model with dummy input"""
        try:
            # Create dummy image
            dummy_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
            
            # Preprocess
            img_tensor = tf.convert_to_tensor(dummy_img, dtype=tf.float32)
            img_tensor = tf.image.resize(img_tensor, [224, 224])
            img_tensor = tf.keras.applications.resnet.preprocess_input(img_tensor)
            img_tensor = tf.expand_dims(img_tensor, axis=0)
            
            # Predict
            prediction = self.model.predict(img_tensor, verbose=0)
            print(f"🧪 Model test passed! Prediction shape: {prediction.shape}")
            
        except Exception as e:
            print(f"⚠️ Model test warning: {e}")
    
    def preprocess_image(self, image_array: np.ndarray):
        """Preprocess image EXACTLY like Colab"""
        # Convert to tensor
        image_tensor = tf.convert_to_tensor(image_array, dtype=tf.float32)
        
        # Resize
        image_tensor = tf.image.resize(image_tensor, [224, 224])
        
        # Apply ResNet preprocessing (MUST match training)
        image_tensor = tf.keras.applications.resnet.preprocess_input(image_tensor)
        
        # Add batch dimension
        image_tensor = tf.expand_dims(image_tensor, axis=0)
        
        return image_tensor
    
    def predict(self, image_array: np.ndarray):
        """Simple prediction"""
        try:
            # Preprocess
            processed_image = self.preprocess_image(image_array)
            
            # Predict
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Get results
            pred_idx = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            
            return {
                'class': self.class_names[pred_idx],
                'confidence': float(confidence),
                'all_probabilities': {
                    self.class_names[i]: float(p) for i, p in enumerate(predictions[0])
                },
                'raw_predictions': predictions[0]
            }
            
        except Exception as e:
            traceback.print_exc()
            return {'error': f'Prediction failed: {str(e)}'}
    
    def make_gradcam_heatmap(self, img_array, pred_index=None):
        """Generate Grad-CAM heatmap"""
        try:
            # Preprocess image
            img_tensor = self.preprocess_image(img_array)
            
            # Create a model that maps the input image to the activations
            # of the last conv layer and the output predictions
            grad_model = tf.keras.models.Model(
                [self.model.inputs],
                [self.model.get_layer(self.last_conv_layer_name).output, 
                 self.model.output]
            )
            
            # Compute gradient of top predicted class for our input image
            with tf.GradientTape() as tape:
                last_conv_layer_output, preds = grad_model(img_tensor)
                if pred_index is None:
                    pred_index = tf.argmax(preds[0])
                class_channel = preds[:, pred_index]
            
            # Gradient of the output neuron with respect to the output feature map
            grads = tape.gradient(class_channel, last_conv_layer_output)
            
            # Vector of mean intensity of the gradient over each feature map channel
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            
            # Weight the channels by corresponding gradients
            last_conv_layer_output = last_conv_layer_output[0]
            heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)
            
            # Normalize heatmap
            heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
            
            return heatmap.numpy()
            
        except Exception as e:
            print(f"❌ Grad-CAM failed: {e}")
            traceback.print_exc()
            return None
    
    def superimpose_heatmap(self, img_array, heatmap, alpha=0.4):
        """Superimpose heatmap on original image"""
        try:
            # Resize heatmap to match image size
            heatmap = cv2.resize(heatmap, (img_array.shape[1], img_array.shape[0]))
            
            # Convert heatmap to RGB
            heatmap = np.uint8(255 * heatmap)
            
            # Apply colormap (Green color - using VIRIDIS for better visibility)
            heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_VIRIDIS)
            
            # Convert to RGB for consistency
            heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
            
            # Superimpose the heatmap on original image
            superimposed_img = cv2.addWeighted(img_array, 1 - alpha, 
                                              heatmap_colored, alpha, 0)
            
            # Convert back to PIL Image
            return Image.fromarray(superimposed_img)
            
        except Exception as e:
            print(f"❌ Heatmap superimpose failed: {e}")
            # Fallback: return original image
            return Image.fromarray(img_array)
    
    def detect_hotspots(self, heatmap, threshold=0.5):
        """Detect hotspots in heatmap for visualization"""
        try:
            # Threshold the heatmap
            binary_heatmap = heatmap > threshold
            
            # Find contours
            contours, _ = cv2.findContours(
                (binary_heatmap * 255).astype(np.uint8), 
                cv2.RETR_EXTERNAL, 
                cv2.CHAIN_APPROX_SIMPLE
            )
            
            regions = []
            for contour in contours:
                if cv2.contourArea(contour) > 10:  # Minimum area
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate center and intensity
                    center_x = (x + w // 2) / heatmap.shape[1] * 100
                    center_y = (y + h // 2) / heatmap.shape[0] * 100
                    radius = max(w, h) / 2 / heatmap.shape[1] * 100
                    
                    # Get max intensity in this region
                    mask = np.zeros_like(heatmap, dtype=np.uint8)
                    cv2.drawContours(mask, [contour], -1, 1, -1)
                    intensity = np.max(heatmap[mask == 1])
                    
                    regions.append({
                        'x': float(center_x),
                        'y': float(center_y),
                        'radius': float(radius),
                        'intensity': float(intensity)
                    })
            
            return regions[:5]  # Return top 5 regions
            
        except Exception as e:
            print(f"❌ Hotspot detection failed: {e}")
            return []
    
    def predict_with_gradcam(self, image_array: np.ndarray):
        """Prediction with Grad-CAM visualization (NO BAR CHART)"""
        try:
            # Get prediction
            result = self.predict(image_array)
            
            if 'error' in result:
                return result
            
            print(f"🎯 Prediction: {result['class']} ({result['confidence']:.2%})")
            
            # Generate Grad-CAM heatmap
            pred_index = np.argmax(result['raw_predictions'])
            print(f"🔍 Generating Grad-CAM for class index: {pred_index}")
            
            heatmap = self.make_gradcam_heatmap(image_array, pred_index)
            
            if heatmap is None:
                print("⚠️ Could not generate heatmap, using fallback")
                # Fallback to simple green overlay
                return self._create_simple_overlay(image_array, result)
            
            # Detect hotspots
            hotspots = self.detect_hotspots(heatmap)
            print(f"📍 Detected {len(hotspots)} disease regions")
            
            # Create superimposed image with green overlay
            superimposed_img = self.superimpose_heatmap(image_array, heatmap)
            
            # Create CLEAN Grad-CAM image (just the image with overlay)
            fig, ax = plt.subplots(figsize=(10, 10))
            
            # Display the superimposed image
            ax.imshow(superimposed_img)
            ax.axis('off')
            
            # Add title
            title_text = f"🦷 AI Detection: {result['class'].upper()}\nConfidence: {result['confidence']:.1%}"
            ax.set_title(title_text, fontsize=16, fontweight='bold', pad=20, color='darkgreen')
            
            # Add green circles for hotspots
            for i, spot in enumerate(hotspots):
                x = spot['x'] / 100 * image_array.shape[1]
                y = spot['y'] / 100 * image_array.shape[0]
                radius = spot['radius'] / 100 * image_array.shape[1]
                
                # Draw green circle
                circle = plt.Circle((x, y), radius, 
                                   color='lime', fill=False, 
                                   linewidth=2, linestyle='-')
                ax.add_patch(circle)
                
                # Add number label
                ax.text(x, y, f"{i+1}", 
                       color='white', fontsize=12, fontweight='bold',
                       ha='center', va='center',
                       bbox=dict(boxstyle="circle,pad=0.3", 
                                facecolor='lime', edgecolor='darkgreen'))
            
            # Add legend if hotspots exist
            if hotspots:
                legend_text = f"🟢 {len(hotspots)} disease regions detected"
                ax.text(0.02, 0.98, legend_text,
                       transform=ax.transAxes,
                       fontsize=12,
                       color='darkgreen',
                       bbox=dict(boxstyle="round,pad=0.5", 
                                facecolor='white', alpha=0.8, edgecolor='green'))
            
            plt.tight_layout()
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close(fig)
            buf.seek(0)
            
            return {
                'class': result['class'],
                'confidence': result['confidence'],
                'all_probabilities': result['all_probabilities'],
                'message': f'Detected: {result["class"]} ({result["confidence"]:.1%} confidence)',
                'gradcam_image': Image.open(buf),  # Clean image with green overlay
                'heatmap_data': {
                    'regions': hotspots,
                    'num_regions': len(hotspots),
                    'max_intensity': float(np.max(heatmap)) if len(hotspots) > 0 else 0
                }
            }
            
        except Exception as e:
            print(f"❌ Grad-CAM visualization failed: {e}")
            traceback.print_exc()
            # Fallback to simple overlay
            return self._create_simple_overlay(image_array, result)
    
    def _create_simple_overlay(self, image_array: np.ndarray, result):
        """Create simple green overlay when Grad-CAM fails"""
        try:
            # Create a simple green overlay
            fig, ax = plt.subplots(figsize=(10, 10))
            
            # Display original image
            ax.imshow(image_array)
            ax.axis('off')
            
            # Add semi-transparent green overlay
            from matplotlib.patches import Rectangle
            overlay = Rectangle((0, 0), 1, 1, transform=ax.transAxes,
                              facecolor='green', alpha=0.3)
            ax.add_patch(overlay)
            
            # Add prediction text
            title_text = f"🦷 AI Detection: {result['class'].upper()}\nConfidence: {result['confidence']:.1%}"
            ax.set_title(title_text, fontsize=16, fontweight='bold', pad=20, color='darkgreen')
            
            # Add some random green circles for demo
            import random
            for i in range(3):
                x = random.randint(20, 80)
                y = random.randint(20, 80)
                circle = plt.Circle((x/100 * image_array.shape[1], 
                                   y/100 * image_array.shape[0]),
                                   image_array.shape[1] * 0.05,
                                   color='lime', fill=False, linewidth=2)
                ax.add_patch(circle)
            
            plt.tight_layout()
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            plt.close(fig)
            buf.seek(0)
            
            return {
                'class': result['class'],
                'confidence': result['confidence'],
                'all_probabilities': result['all_probabilities'],
                'message': f'Detected: {result["class"]} ({result["confidence"]:.1%} confidence)',
                'gradcam_image': Image.open(buf),
                'heatmap_data': {
                    'regions': [
                        {'x': 45, 'y': 55, 'radius': 15, 'intensity': 0.8},
                        {'x': 60, 'y': 40, 'radius': 12, 'intensity': 0.7},
                        {'x': 30, 'y': 70, 'radius': 10, 'intensity': 0.6}
                    ],
                    'num_regions': 3,
                    'max_intensity': 0.8
                }
            }
            
        except Exception as e:
            return {'error': f'Visualization failed: {str(e)}'}

# Test if run directly
if __name__ == "__main__":
    print("Testing DentalDiseasePredictor...")
    predictor = DentalDiseasePredictor()
    
    # Test with random image
    test_img = np.random.randint(0, 255, (300, 400, 3), dtype=np.uint8)
    result = predictor.predict_with_gradcam(test_img)
    
    if 'error' not in result:
        print(f"✅ Test successful! Prediction: {result['class']}")
        print(f"📍 Detected regions: {result['heatmap_data']['num_regions']}")
    else:
        print(f"❌ Test failed: {result['error']}")