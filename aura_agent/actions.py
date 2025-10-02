import os
import email_client
import gui
import threading
import vision

# --- File System Actions ---

def create_file(filepath):
    """Creates an empty file at the specified path."""
    try:
        with open(filepath, 'w') as f:
            pass
        return f"Successfully created file: {filepath}"
    except Exception as e:
        return f"Error creating file: {e}"

def write_to_file(filepath, content):
    """Writes content to a file, overwriting it if it exists."""
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote to file: {filepath}"
    except Exception as e:
        return f"Error writing to file: {e}"

def list_files(directory="."):
    """Lists all files and directories in a specified directory."""
    try:
        files = os.listdir(directory)
        if not files:
            return "The directory is empty."
        return "Files in directory:\n" + "\n".join(files)
    except FileNotFoundError:
        return f"Error: Directory not found at '{directory}'"
    except Exception as e:
        return f"Error listing files: {e}"

def read_file(filepath):
    """Reads the content of a file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return f"Content of {filepath}:\n{content}"
    except FileNotFoundError:
        return f"Error: File not found at '{filepath}'"
    except Exception as e:
        return f"Error reading file: {e}"

def delete_file(filepath):
    """Deletes a file at the specified path."""
    try:
        os.remove(filepath)
        return f"Successfully deleted file: {filepath}"
    except FileNotFoundError:
        return f"Error: File not found at '{filepath}'"
    except Exception as e:
        return f"Error deleting file: {e}"

def create_directory(directory_path):
    """Creates a new directory at the specified path."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        return f"Successfully created directory: {directory_path}"
    except Exception as e:
        return f"Error creating directory: {e}"

def search_files(query, start_path="."):
    """Searches for files containing the query in their name."""
    try:
        matches = []
        for root, dirs, files in os.walk(start_path):
            for name in files + dirs:
                if query.lower() in name.lower():
                    matches.append(os.path.join(root, name))
        if not matches:
            return f"No files or directories found matching '{query}'."
        return "Found the following matches:\n" + "\n".join(matches)
    except Exception as e:
        return f"Error searching for files: {e}"

def create_file_with_visual_context(command):
    """Creates a file by first asking the vision model for a suggested path based on screen context."""
    print("Capturing screen for visual context...")
    screenshot_path = vision.capture_screen()
    if not screenshot_path:
        return "Failed to capture screen."

    try:
        suggested_path = vision.get_visual_context_suggestion(command, screenshot_path)
        if suggested_path:
            # Now, create the file at the suggested path
            return create_file(suggested_path)
        else:
            return "Could not determine a file path from visual context."
    finally:
        # Clean up the screenshot file
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

# --- Email Actions ---

def list_emails(service, count=5):
    """Lists recent emails from the user's Gmail account."""
    if not service:
        return "Gmail service is not available. Please check authentication."
    return email_client.list_emails(service, count)

def read_email(service, message_id):
    """Reads the content of a specific email."""
    if not service:
        return "Gmail service is not available. Please check authentication."
    email_content = email_client.read_email(service, message_id)
    if isinstance(email_content, dict):
        return f"From: {email_content['from']}\nSubject: {email_content['subject']}\n\n{email_content['body']}"
    return email_content

def summarize_email(service, message_id):
    """Summarizes the content of a specific email."""
    if not service:
        return "Gmail service is not available. Please check authentication."
    email_content = email_client.read_email(service, message_id)
    if isinstance(email_content, dict):
        summary = email_client.summarize_text(email_content['body'])
        return f"Summary of email from {email_content['from']} about '{email_content['subject']}':\n{summary}"
    return email_content

def draft_email(to_address="", subject="", body=""):
    """Opens a GUI window to draft an email, running in a separate thread."""
    print("Opening email draft window...")
    # Run the GUI in a separate thread to avoid blocking the main agent loop
    gui_thread = threading.Thread(target=gui.open_email_draft_window, args=(to_address, subject, body))
    gui_thread.daemon = True
    gui_thread.start()
    return "Email draft window opened. Please check your screen."

# A dictionary to map action strings to function objects
ACTION_MAP = {
    # File System
    "create_file": create_file,
    "write_to_file": write_to_file,
    "list_files": list_files,
    "read_file": read_file,
    "delete_file": delete_file,
    "create_directory": create_directory,
    "search_files": search_files,
    "create_file_with_visual_context": create_file_with_visual_context,
    # Email
    "list_emails": list_emails,
    "read_email": read_email,
    "summarize_email": summarize_email,
    "draft_email": draft_email,
}