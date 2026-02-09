from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import tensorflow as tf

# -----------------------------
# Create Flask app
# -----------------------------
app = Flask(__name__)
CORS(app)   # allows frontend to talk to backend

# -----------------------------
# Load trained CNN model
# -----------------------------
MODEL_PATH = "fruit_model.h5"

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print("❌ Error loading model:", e)

IMG_SIZE = 224   # must match your training image size

# -----------------------------
# Image Preprocessing Function
# -----------------------------
def preprocess_image(image_file):
    file_bytes = np.frombuffer(image_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # resize to model size
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

    # normalize pixels
    img = img / 255.0

    # add batch dimension
    img = np.expand_dims(img, axis=0)

    return img

# -----------------------------
# Price Estimation Logic
# -----------------------------
def estimate_price(quality):
    price_map = {
        "Good": "₹120 per kg",
        "Average": "₹80 per kg",
        "Bad": "₹40 per kg"
    }
    return price_map.get(quality, "Price not available")

# -----------------------------
# Prediction API
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # preprocess image
    img = preprocess_image(file)

    # model prediction
    prediction = model.predict(img)

    # get class index
    class_index = np.argmax(prediction)

    quality_classes = ["Bad", "Average", "Good"]
    predicted_quality = quality_classes[class_index]

    # estimate price
    estimated_price = estimate_price(predicted_quality)

    return jsonify({
        "quality": predicted_quality,
        "rate": estimated_price
    })

# -----------------------------
# Run Flask server
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
