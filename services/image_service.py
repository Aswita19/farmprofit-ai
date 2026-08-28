from PIL import Image
import numpy as np


def prepare_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image = image.resize((224, 224))

    image_array = np.array(image)

    return image, image_array


def analyze_field_image(image_array):
    """
    Placeholder for future computer vision model.

    Later replace this with:
    TensorFlow / PyTorch / ONNX model inference.
    """

    return {
        "health_score": 82,
        "condition": "Generally Healthy",
        "stress_probability": 0.18,
        "disease_probability": 0.12,
        "notes": "No significant visible stress detected."
    }
