import os
import struct
import json
import pvporcupine
import pyaudio
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import actions

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the Gemini API
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("Error: GOOGLE_API_KEY is not set in the .env file.")

def listen_for_wake_word(gmail_service):
    """
    Continuously listens for the wake word "Hey AURA" using Porcupine.
    Once the wake word is detected, it triggers the command recording.
    """
    if not PORCUPINE_ACCESS_KEY:
        print("Error: PORCUPINE_ACCESS_KEY is not set in the .env file.")
        return

    try:
        porcupine = pvporcupine.create(
            access_key=PORCUPINE_ACCESS_KEY,
            keywords=['hey aura'] # You can add more keywords here
        )
    except pvporcupine.PorcupineError as e:
        print(f"Error initializing Porcupine: {e}")
        print("Please ensure your PORCUPINE_ACCESS_KEY is valid.")
        return

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for wake word: 'Hey AURA'...")

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Wake word detected! Listening for your command...")
                record_and_process_command(gmail_service)
                print("Listening for wake word: 'Hey AURA'...")

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if pa:
            pa.terminate()

def record_and_process_command(gmail_service):
    """
    Records audio from the microphone, converts it to text, and sends it
    to the Gemini API for interpretation into a structured command.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1.0
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say your command:")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Timeout: No command heard.")
            return

    try:
        command_text = r.recognize_google(audio)
        print(f"You said: {command_text}")
        interpret_command(command_text, gmail_service)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def interpret_command(command_text, service):
    """
    Sends the transcribed command to the Gemini API to be converted into a
    structured JSON object representing a function call.
    """
    if not GOOGLE_API_KEY:
        print("Cannot interpret command, GOOGLE_API_KEY is not configured.")
        return

    try:
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        You are a helpful AI assistant that converts natural language commands into structured JSON objects.
        The user said: "{command_text}"

        Based on the user's command, create a JSON object with two keys: "action" and "parameters".
        The "action" should be one of the following predefined functions:
        'create_file', 'write_to_file', 'list_files', 'read_file', 'delete_file', 'create_directory', 'search_files',
        'create_file_with_visual_context', 'list_emails', 'read_email', 'summarize_email', 'draft_email'.

        The "parameters" should be a dictionary containing the necessary arguments for that function.
        For example:
        - "create a file named report.txt" -> {{"action": "create_file", "parameters": {{"filepath": "report.txt"}}}}
        - "create a file for this project" -> {{"action": "create_file_with_visual_context", "parameters": {{"command": "create a file for this project"}}}}
        - "create a new folder called project_files" -> {{"action": "create_directory", "parameters": {{"directory_path": "project_files"}}}}
        - "search for a file named budget" -> {{"action": "search_files", "parameters": {{"query": "budget"}}}}
        - "list my recent emails" -> {{"action": "list_emails", "parameters": {{"count": 5}}}}
        - "draft an email to jane.doe@example.com" -> {{"action": "draft_email", "parameters": {{"to_address": "jane.doe@example.com"}}}}

        Return only the JSON object, with no other text or explanation.
        """

        response = model.generate_content(prompt)

        # Clean up the response to get a valid JSON string
        json_response_str = response.text.strip().replace('`', '').replace('json', '')

        # Parse the JSON string into a Python dictionary
        command_json = json.loads(json_response_str)

        print("Interpreted Command (JSON):")
        print(command_json)

        # Execute the command
        execute_action(command_json, service)

    except json.JSONDecodeError:
        print("Error: Failed to decode the JSON response from the AI.")
        print(f"Received: {response.text}")
    except Exception as e:
        print(f"An error occurred while interpreting the command: {e}")

def execute_action(command_json, service=None):
    """
    Executes the action specified in the command JSON by calling the
    corresponding function from the actions module.
    """
    action_name = command_json.get("action")
    parameters = command_json.get("parameters", {})

    action_func = actions.ACTION_MAP.get(action_name)

    if action_func:
        try:
            # If the action is email-related, inject the service object into the parameters
            if "email" in action_name:
                parameters["service"] = service

            # For visual context, we need to pass the original command text
            if action_name == "create_file_with_visual_context":
                parameters["command"] = command_text

            # Pass parameters to the function using dictionary unpacking
            result = action_func(**parameters)
            print(f"Action Result: {result}")
        except TypeError as e:
            print(f"Error: Invalid parameters for action '{action_name}': {e}")
        except Exception as e:
            print(f"An error occurred during action execution: {e}")
    else:
        print(f"Error: Unknown action '{action_name}'.")

import auth

# ... (previous code)

if __name__ == "__main__":
    print("Initializing AURA...")
    print("Checking Google Authentication status...")
    gmail_service = auth.get_gmail_service()

    if not gmail_service:
        print("\nAURA requires Google authentication to access features like email.")
        print("Please follow the setup instructions in README.md to provide credentials.")
        print("Exiting application.")
    else:
        print("Authentication successful. AURA is ready.")
        # The main listening loop starts only after successful authentication
        listen_for_wake_word(gmail_service)