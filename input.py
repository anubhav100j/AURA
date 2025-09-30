import cv2
import speech_recognition as sr
from PIL import Image
import os

# For Gemini API multimodal prompt
import google.generativeai as genai
from gemini_client import model  # Ensure this matches your installed Gemini SDK

# For LangChain and Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import AgentType, initialize_agent

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
        print(f"Speech recognition failed. Please check your microphone and internet connection.")
        exit()

# --------- 3. Gemini API Setup & Multimodal Prompt ---------
with open('input_image.jpg', 'rb') as f:
    image_bytes = f.read()

prompt = f"Analyze this image and respond to the following voice prompt: {speech_text}"

try:
    response = model.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_bytes
                        }
                    }
                ]
            }
        ]
    )
    output_content = response.text
    print("Gemini Response:\n", output_content)
except Exception as e:
    print(f"Gemini API call failed: {e}")
    exit()

# --------- 4. (Optional) LangChain Agent Setup ---------
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
ddg_search = DuckDuckGoSearchResults()

agent = initialize_agent(
    tools=[ddg_search],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# You can use the agent for text-based queries if needed
# output = agent.invoke("What's the latest news in AI?")
# print(output.get('output'))
