const video = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const startCameraButton = document.getElementById('start-camera');
const captureImageButton = document.getElementById('capture-image');
const textPrompt = document.getElementById('text-prompt');
const sendPromptButton = document.getElementById('send-prompt');
const responseContainer = document.getElementById('response-container');

let stream;

startCameraButton.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        startCameraButton.disabled = true;
        captureImageButton.disabled = false;
    } catch (err) {
        console.error("Error accessing webcam: ", err);
        alert("Could not access the webcam. Please ensure you have a webcam enabled and have granted permission.");
    }
});

captureImageButton.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    video.style.display = 'none';
    canvas.style.display = 'block';

    captureImageButton.disabled = true;
    sendPromptButton.disabled = false;
    textPrompt.disabled = false;
});

sendPromptButton.addEventListener('click', async () => {
    const imageUrl = canvas.toDataURL('image/jpeg');
    const prompt = textPrompt.value;

    if (!prompt) {
        alert("Please enter a text prompt.");
        return;
    }

    // Disable UI
    sendPromptButton.disabled = true;
    textPrompt.disabled = true;
    responseContainer.textContent = 'Sending to AI...';

    // Mock Gemini API call
    try {
        const response = await mockGeminiApi(imageUrl, prompt);
        responseContainer.textContent = response;
    } catch (error) {
        console.error("Error sending to AI: ", error);
        responseContainer.textContent = 'An error occurred. Please try again.';
    }

    // Re-enable UI
    sendPromptButton.disabled = false;
    textPrompt.disabled = false;
});

// Mock Gemini API function
function mockGeminiApi(imageUrl, prompt) {
    console.log("Sending to mock Gemini API:");
    console.log("Image URL (first 50 chars):", imageUrl.substring(0, 50));
    console.log("Prompt:", prompt);

    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (prompt.toLowerCase().includes('error')) {
                reject('Mock API error!');
            } else {
                resolve(`Mock response: The image and the prompt '${prompt}' were received successfully.`);
            }
        }, 2000);
    });
}

// Stop the webcam stream when the user navigates away
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});