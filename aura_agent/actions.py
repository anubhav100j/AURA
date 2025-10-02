import os

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

# A dictionary to map action strings to function objects
ACTION_MAP = {
    "create_file": create_file,
    "write_to_file": write_to_file,
    "list_files": list_files,
    "read_file": read_file,
    "delete_file": delete_file,
}