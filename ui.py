import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import requests

# Load the pre-trained model
model = load_model("fruit_quality_classifier.h5")
print("Model loaded successfully.")

# Define image size (same as used during training)
image_size = (192, 256)
class_names = ["Bad", "Good", "Mixed"]

# API URL and key
api_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
api_key = "579b464db66ec23bdd0000016fbfcefc53914cc969e972033b8e2bee"

# Function to fetch rates from API
def fetch_rates():
    try:
        params = {
            "api-key": api_key,
            "format": "json",
            "limit": 1
        }
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        rates = []
        for record in data.get("records", []):
            min_price = float(record.get("min_price", 0))
            max_price = float(record.get("max_price", 0))
            rates.append((min_price, max_price))
        return rates if rates else [(0, 0)]
    except Exception as e:
        print(f"Error fetching rates: {e}")
        return [(0, 0)]

# Function to get the appropriate rate based on quality
def get_rate(quality):
    rates = fetch_rates()
    if quality == "Good":
        return f"Current Market Price (approximate): {max(rates, key=lambda x: x[1])[1]}"
    elif quality == "Mixed":
        return f"Current Market Price (approximate): {min(rates, key=lambda x: x[0])[0]}"
    else:  # Bad
        return "Current Market Price (approximate): 0"

# Function to predict fruit quality
def predict_fruit_quality(image_path):
    img = image.load_img(image_path, target_size=image_size)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]
    return predicted_class

# Function to load and display image, then predict quality
def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        # Display selected image
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

        # Predict fruit quality
        quality = predict_fruit_quality(file_path)
        rate = get_rate(quality)
        result_label.config(text=f"Predicted Quality: {quality}\n{rate}")

# Create the GUI window
root = tk.Tk()
root.title("Fruit Quality Classifier")
root.configure(bg="#1e1e1e")
root.state('zoomed')

# Define styles for dark mode
def dark_mode_style(widget, **kwargs):
    widget.configure(bg="#1e1e1e", fg="#ffffff", **kwargs)

# Image display label
image_label = Label(root, bg="#1e1e1e")
image_label.pack(pady=10)

# Prediction result label
result_label = Label(root, text="Prediction will appear here.", font=("Arial", 14))
dark_mode_style(result_label)
result_label.pack(pady=10)

# Load Image button
load_button = Button(root, text="Load Image", command=load_image, font=("Arial", 12), bg="#3c3c3c", fg="#ffffff", activebackground="#575757", activeforeground="#ffffff")
load_button.pack(pady=10)

# Exit button
exit_button = Button(root, text="Exit", command=root.quit, font=("Arial", 12), bg="#3c3c3c", fg="#ffffff", activebackground="#575757", activeforeground="#ffffff")
exit_button.pack(pady=10)

# Run the GUI application
root.mainloop()
