import cv2
import speech_recognition as sr
from gemini_client import model
from PIL import Image
import os

# --------- 1. Capture Webcam Image ---------
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
ret, frame = cap.read()

if not ret:
    cap.release()
    print("Trying camera index 1...")
    cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)
    ret, frame = cap.read()

if ret:
    cv2.imwrite('input_image.jpg', frame)
    print("Webcam image saved.")
else:
    print("Error capturing image from webcam. Exiting.")
    exit()

cap.release()

# --------- 2. Record Audio & Speech Recognition ---------
r = sr.Recognizer()
speech_text = ""
with sr.Microphone() as source:
    print("Say something for Gemini analysis:")
    audio = r.listen(source)
    try:
        speech_text = r.recognize_google(audio)
        print("You said:", speech_text)
    except Exception as e:
        print("--- SPEECH RECOGNITION ERROR ---")
        print(e)
        print("---------------------------------")
        print(f"Speech recognition failed. Please check your microphone and internet connection.")
        exit()

# --------- 3. Gemini API Setup & Multimodal Prompt ---------
img = Image.open('input_image.jpg')
prompt = f"Analyze this image and respond to the following voice prompt: {speech_text}"

try:
    response = model.generate_content([prompt, img])
    output_content = response.text
    print("Gemini Response:\n", output_content)
except Exception as e:
    print(f"Gemini API call failed: {e}")
    exit()