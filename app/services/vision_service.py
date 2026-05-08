import cv2
import numpy as np
from PIL import Image
import io
import random  # Remove this when real model is added

# TODO: Uncomment when YOLOv8 weights are downloaded
# from ultralytics import YOLO
# model = YOLO("yolov8n.pt")  # auto-downloads on first run

# TODO: Uncomment for CLIP brand compliance
# from transformers import CLIPProcessor, CLIPModel
# import torch
# clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
# clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def analyze_glow_sign(image_bytes: bytes) -> dict:
    """
    Detects glow sign boards in an image.
    TODO: Replace mock with real YOLOv8 detection
    """
    # Convert bytes to image
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        return {"score": 0.0, "flags": ["could_not_read_image"]}
    
    # TODO: Real detection
    # results = model(img)
    # boards_detected = [r for r in results[0].boxes if r.cls == 0]  # class 0 = sign board
    # score = min(len(boards_detected) * 30, 100)  # simple scoring
    
    # MOCK RESPONSE (remove when model is ready)
    score = random.uniform(70, 95)
    flags = []
    if score < 75:
        flags.append("glow_sign_not_visible")
    
    return {"score": round(score, 1), "flags": flags}


def analyze_branding_compliance(image_bytes: bytes) -> dict:
    """
    Checks in-shop branding against brand guidelines using CLIP.
    TODO: Replace mock with real CLIP model
    """
    # TODO: Real CLIP compliance check
    # image = Image.open(io.BytesIO(image_bytes))
    # inputs = clip_processor(
    #     text=["brand logo visible", "no brand logo", "proper signage"],
    #     images=image, return_tensors="pt", padding=True
    # )
    # outputs = clip_model(**inputs)
    # probs = outputs.logits_per_image.softmax(dim=1)
    # brand_score = float(probs[0][0]) * 100
    
    # MOCK RESPONSE
    score = random.uniform(65, 92)
    flags = []
    if score < 70:
        flags.append("missing_logo_banner")
    if score < 80:
        flags.append("incorrect_brand_colors")
    
    return {"score": round(score, 1), "flags": flags}


def analyze_store_image(image_bytes: bytes) -> dict:
    """
    Scores overall store image: cleanliness, layout, visual consistency.
    TODO: Replace mock with real ensemble model
    """
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        return {"score": 0.0, "flags": ["could_not_read_image"]}
    
    # TODO: Real analysis
    # brightness = img.mean()
    # sharpness = cv2.Laplacian(img, cv2.CV_64F).var()
    # score based on these + color histogram matching vs brand palette
    
    # MOCK RESPONSE
    score = random.uniform(72, 96)
    flags = []
    if score < 78:
        flags.append("store_looks_cluttered")
    
    return {"score": round(score, 1), "flags": flags}


def analyze_grooming(image_bytes: bytes) -> dict:
    """
    Checks champion grooming and appearance standards.
    TODO: Replace mock with MediaPipe face detection + DeepFace
    """
    # TODO: Real grooming check
    # import mediapipe as mp
    # import deepface
    # face_results = mp.solutions.face_detection.FaceDetection().process(img)
    # for each face: check uniform color, ID card visible, beard compliance
    
    # MOCK RESPONSE
    score = random.uniform(70, 95)
    flags = []
    if score < 80:
        flags.append("ID_card_not_visible")
    if score < 75:
        flags.append("non_standard_uniform")
    
    compliant = score >= 80
    return {"score": round(score, 1), "flags": flags, "compliant": compliant}