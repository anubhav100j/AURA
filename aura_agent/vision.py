from PIL import ImageGrab
import google.generativeai as genai

def capture_screen(filepath="screenshot.png"):
    """Captures the entire screen and saves it to a file."""
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(filepath, "PNG")
        return filepath
    except Exception as e:
        print(f"Error capturing screen: {e}")
        return None

def get_visual_context_suggestion(command, screenshot_path):
    """
    Uses a multimodal AI model to suggest a filepath based on visual context.

    Args:
        command (str): The user's voice command (e.g., "create a new file for my project").
        screenshot_path (str): The path to the screenshot image.

    Returns:
        A string containing the suggested filepath, or None if an error occurs.
    """
    try:
        # Use a model that supports image and text inputs
        model = genai.GenerativeModel('gemini-pro-vision')

        prompt = f"""
        Analyze the attached screenshot and the user's command to determine the best location and name for a new file.
        The user's command was: "{command}".

        Based on the visual context (e.g., open applications, folder structures, file contents), suggest a single, complete, and logical file path (e.g., 'documents/projects/my_app/new_feature.py').

        Return only the file path and nothing else.
        """

        screenshot_image = {"mime_type": "image/png", "data": open(screenshot_path, "rb").read()}

        response = model.generate_content([prompt, screenshot_image])

        suggested_path = response.text.strip()
        print(f"AI suggested path: {suggested_path}")
        return suggested_path

    except Exception as e:
        print(f"Error getting visual context suggestion: {e}")
        return None