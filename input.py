import cv2
import speech_recognition as sr
from gemini_client import model
from PIL import Image
import git
import os
import webbrowser

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
prompt = f"Analyze this UI image for {speech_text} and generate HTML/CSS code for my project."

try:
    response = model.generate_content([prompt, img])
    output_content = response.text
    print("Gemini Response:\n", output_content)
except Exception as e:
    print(f"Gemini API call failed: {e}")
    exit()

# --------- 4. Write Output to HTML File ---------
filename = 'output.html'
with open(filename, 'w', encoding="utf-8") as f:
    f.write(output_content)
print(f"Output written to {filename}")

# --------- 5. Preview HTML in Browser ---------
file_path = os.path.abspath(filename)
webbrowser.open('file://' + file_path)

# --------- 6. Basic HTML Structure Check ---------
with open(filename, 'r', encoding="utf-8") as f:
    html = f.read()
    if "<html" in html.lower() and "<body" in html.lower():
        print("Basic HTML structure detected.")
    else:
        print("Warning: HTML structure may be incomplete.")

# --------- 7. User Confirmation Before Git Actions ---------
confirm = input("Push generated code to GitHub? (y/n): ")
if confirm.lower() == 'y':
    try:
        repo = git.Repo(search_parent_directories=True)
        repo.git.add(filename)
        repo.git.commit('-m', 'Add Gemini AI generated UI')
        repo.git.push()
        print("Success: Pushed to GitHub.")
    except Exception as e:
        print(f"Git operation failed: {e}")
else:
    print("Action canceled by user.")
