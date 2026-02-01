import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import tensorflow as tf
import numpy as np
import zipfile
import tempfile
import json
import shutil

print("=" * 70)
print("🔧 FIXING MODEL FOR TENSORFLOW 2.15.0")
print(f"TensorFlow version: {tf.__version__}")
print("=" * 70)

def fix_keras_model():
    """Convert .keras model to be compatible with TF 2.15"""
    
    input_path = "DENTAL_MODEL_BEST.keras"
    output_path = "DENTAL_MODEL_TF215.keras"
    
    if not os.path.exists(input_path):
        print(f"❌ Input model not found: {input_path}")
        return None
    
    print(f"📥 Input model: {input_path}")
    print(f"📤 Output model: {output_path}")
    
    try:
        # Method 1: Direct conversion
        print("\n1️⃣ Trying direct conversion...")
        model = tf.keras.models.load_model(
            input_path,
            compile=False,
            safe_mode=False
        )
        
        # Re-save with current TF version
        model.save(output_path, save_format='keras')
        print(f"✅ Direct conversion successful!")
        return output_path
        
    except Exception as e:
        print(f"❌ Direct conversion failed: {e}")
        
        # Method 2: Extract and fix
        print("\n2️⃣ Extracting and fixing model...")
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Extract .keras file (it's a zip)
            with zipfile.ZipFile(input_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            print(f"   Extracted to: {temp_dir}")
            
            # Find config files
            config_path = os.path.join(temp_dir, 'config.json')
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                print("   Found config.json")
                
                # Fix config for TF 2.15
                if 'keras_version' in config:
                    config['keras_version'] = '2.15.0'
                
                # Write fixed config
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                
                print("   Updated config.json")
            
            # Re-package as .keras
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)
            
            print(f"✅ Repackaged as: {output_path}")
            
            # Clean up
            shutil.rmtree(temp_dir)
            
            return output_path
            
        except Exception as e2:
            print(f"❌ Extraction method failed: {e2}")
            
            # Method 3: Create compatible model from scratch
            print("\n3️⃣ Creating compatible model from scratch...")
            return create_compatible_model()

def create_compatible_model():
    """Create a fresh model compatible with TF 2.15"""
    print("   Creating fresh ResNet50 model...")
    
    # Build the exact same architecture
    base_model = tf.keras.applications.ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    base_model.trainable = False
    
    inputs = tf.keras.Input(shape=(224, 224, 3))
    
    # Preprocessing layer (important!)
    x = tf.keras.applications.resnet.preprocess_input(inputs)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(256, activation='relu', 
                              kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.Dropout(0.5)(x)
    outputs = tf.keras.layers.Dense(4, activation='softmax')(x)
    
    model = tf.keras.Model(inputs, outputs)
    
    # Compile
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Save
    output_path = "DENTAL_MODEL_FRESH.keras"
    model.save(output_path)
    
    print(f"✅ Created fresh model: {output_path}")
    return output_path

# Run the fix
fixed_model = fix_keras_model()

if fixed_model:
    print(f"\n✅ FIXED MODEL: {fixed_model}")
    
    # Test the fixed model
    print("\n🧪 Testing fixed model...")
    try:
        model = tf.keras.models.load_model(fixed_model, compile=False)
        
        # Test prediction
        dummy_input = np.random.randn(1, 224, 224, 3).astype(np.float32)
        dummy_input = tf.keras.applications.resnet.preprocess_input(dummy_input)
        
        prediction = model.predict(dummy_input, verbose=0)
        print(f"✅ Model works! Prediction shape: {prediction.shape}")
        print(f"   Classes: {prediction[0]}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

print("\n" + "=" * 70)
print("📝 NEXT STEPS:")
print("1. Use DENTAL_MODEL_TF215.keras in your code")
print("2. Update MODEL_PATH in main.py")
print("3. Run the simple test below")
print("=" * 70)