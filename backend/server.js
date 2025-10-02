const express = require('express');
const multer = require('multer');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const dotenv = require('dotenv');
const fs = require('fs');
const path = require('path');

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

// Ensure the 'uploads' directory exists
const uploadDir = 'uploads';
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir);
}

// Configure multer for file storage
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, uploadDir);
    },
    filename: function (req, file, cb) {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
    }
});
const upload = multer({ storage: storage });

// Initialize the Google Gemini AI client
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);

// Helper function to convert a file to a generative part for the API
function fileToGenerativePart(filePath, mimeType) {
    return {
        inlineData: {
            data: Buffer.from(fs.readFileSync(filePath)).toString("base64"),
            mimeType
        },
    };
}

// API endpoint for processing voice prompts
app.post('/api/voice-prompt', upload.single('audio'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No audio file uploaded.' });
    }

    const audioFilePath = req.file.path;

    try {
        // Use a model that supports audio input, like a Gemini 1.5 model
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro-latest" });

        const audioPart = fileToGenerativePart(audioFilePath, req.file.mimetype);

        const prompt = `
            Please listen to the following audio recording carefully. The user may stutter or have repetitions in their speech.
            Your task is to first transcribe the audio into clear, fluent text, correcting any stutters or repetitions to reflect the user's intended query.
            After producing the corrected transcription, please provide a direct and helpful response to that query.
            Combine the corrected query and your answer into a single, coherent response. For example: "You asked: [corrected query]. Here is the answer: [your answer]."
        `;

        const result = await model.generateContent([prompt, audioPart]);
        const response = await result.response;
        const text = response.text();

        res.json({ response: text });

    } catch (error) {
        console.error('Error processing voice prompt:', error);
        res.status(500).json({ error: 'Failed to process your request. Please check the server logs.' });
    } finally {
        // Clean up the uploaded file from the server
        fs.unlink(audioFilePath, (err) => {
            if (err) {
                console.error("Error deleting uploaded file:", err);
            }
        });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});