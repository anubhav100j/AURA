# AURA: AI-Powered Local Voice Assistant

AURA is a local AI agent that runs on your computer, listens for your voice commands, and performs actions on your local file system. It uses a wake word to activate, so it's always ready for your next command without needing constant interaction.

## Features

- **Wake Word Detection:** AURA listens for the "Hey AURA" wake word, so it only starts processing commands when you want it to.
- **Voice Command Recognition:** It uses Google's Speech-to-Text service to accurately transcribe your spoken commands.
- **Natural Language Understanding:** It leverages the Google Gemini API to understand your commands and convert them into structured actions.
- **Local File System Control:** It can perform a variety of file system operations, including:
    - Creating files (`create_file`)
    - Writing to files (`write_to_file`)
    - Listing files and directories (`list_files`)
    - Reading files (`read_file`)
    - Deleting files (`delete_file`)

## How It Works

1.  **Listening:** The agent continuously listens for the "Hey AURA" wake word using the `pvporcupine` engine.
2.  **Recording:** Once the wake word is detected, it records your voice command.
3.  **Transcription:** The recorded audio is sent to Google's Speech Recognition service to be converted into text.
4.  **Interpretation:** The transcribed text is sent to the Gemini Pro model with a specialized prompt, asking it to return a structured JSON object representing the action to be taken (e.g., `{"action": "create_file", "parameters": {"filepath": "my_notes.txt"}}`).
5.  **Execution:** The agent parses the JSON object and calls the corresponding function to perform the action on your local machine.

## Setup and Installation

### Prerequisites

- Python 3.7+
- A microphone connected to your computer.
- `portaudio` library. On Debian-based systems (like Ubuntu), you can install it with:
  ```bash
  sudo apt-get update && sudo apt-get install -y portaudio19-dev
  ```

### 1. Clone the Repository

Clone this repository to your local machine:
```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Install Dependencies

Install the required Python packages using the `requirements.txt` file:
```bash
pip install -r aura_agent/requirements.txt
```

### 3. Get API Keys and Credentials

This project requires API keys for Picovoice and Google, as well as OAuth 2.0 credentials for accessing Google services like Gmail.

-   **Porcupine Access Key:** For wake word detection. You can get a free key from the [Picovoice Console](https://console.picovoice.ai/).
-   **Google API Key (for Gemini):** For command interpretation with Gemini. You can create one from the [Google AI Studio](https://aistudio.google.com/app/apikey).
-   **Google OAuth 2.0 Credentials (for Gmail):** To allow AURA to access your Google account, you need to create OAuth 2.0 Client ID credentials.
    1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
    2.  Create a new project or select an existing one.
    3.  Enable the **Gmail API** for your project.
    4.  Go to "Credentials" in the APIs & Services section.
    5.  Click "Create Credentials" -> "OAuth client ID".
    6.  Select "Desktop app" as the application type.
    7.  After creation, click the "Download JSON" button for the client ID.
    8.  **Rename the downloaded file to `credentials.json` and place it inside the `aura_agent` directory.** This file is essential for the authentication process.

### 4. Configure Environment Variables

1.  Navigate to the `aura_agent` directory.
2.  Create a `.env` file. You can copy the example if one exists, or create a new file.
3.  Open the `.env` file and add your API keys:
    ```
    # aura_agent/.env
    PORCUPINE_ACCESS_KEY="YOUR_PORCUPINE_ACCESS_KEY"
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    ```

## Usage

To run the AURA agent, execute the `agent.py` script from the root directory of the project:

```bash
python aura_agent/agent.py
```

**First-Time Setup:** The first time you run the agent, a browser window will open, asking you to log in to your Google account and grant AURA permission to access the services it needs (e.g., Gmail). After you approve, a `token.json` file will be created in the `aura_agent` directory. This file stores your authorization, so you won't have to log in every time.

The script will initialize and you will see the message: "Listening for wake word: 'Hey AURA'...".

Now, you can activate the agent by saying **"Hey AURA"**, followed by a command.

### Example Commands

-   *"Hey AURA... create a file named shopping list dot txt."*
-   *"Hey AURA... write 'buy milk and eggs' to the file shopping list dot txt."*
-   *"Hey AURA... what's in the file shopping list dot txt?"*
-   *"Hey AURA... list all the files."*
-   *"Hey AURA... delete the shopping list file."*

The agent will print the transcribed command, the interpreted JSON action, and the result of the action to the console. To stop the agent, press `Ctrl+C` in the terminal.