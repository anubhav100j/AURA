# Backend Node.js Server for Gemini Voice Prompts

This directory contains a Node.js server that processes voice prompts using the Google Gemini API. It's designed to take an audio file, correct any stutters or repetitions in the speech, and then generate a helpful response to the user's query.

## Setup

1.  **Install Dependencies:**
    Navigate to the `backend` directory and install the required npm packages.
    ```bash
    cd backend
    npm install
    ```

2.  **Set Environment Variables:**
    Create a `.env` file in the `backend` directory. This file will store your Google API key.
    ```
    cp .env.example .env
    ```
    Open the `.env` file and replace `YOUR_API_KEY` with your actual Google API key.
    ```
    # .env
    GOOGLE_API_KEY=YOUR_API_KEY
    ```

## Running the Server

To start the server, run the following command from the `backend` directory:

```bash
npm start
```

The server will start on `http://localhost:3000` by default.

## API Endpoint

### POST /api/voice-prompt

This endpoint accepts a `POST` request with an audio file to be processed.

-   **Request:** `multipart/form-data`
-   **Field:** `audio` (containing the audio file)

**Example cURL Request:**

```bash
curl -X POST -F "audio=@/path/to/your/audiofile.wav" http://localhost:3000/api/voice-prompt
```

-   **Success Response (200 OK):**
    ```json
    {
      "response": "You asked: [corrected query]. Here is the answer: [Gemini's answer]."
    }
    ```

-   **Error Response (400 Bad Request):**
    If no audio file is uploaded.
    ```json
    {
      "error": "No audio file uploaded."
    }
    ```

-   **Error Response (500 Internal Server Error):**
    If the server fails to process the request.
    ```json
    {
      "error": "Failed to process your request. Please check the server logs."
    }
    ```