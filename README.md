# AURA 💡
**Smart Glasses AI Assistant**

A multimodal AI system that combines voice + vision inputs with an agentic AI backend to perform real-world tasks hands-free (inspired by Jarvis & Meta glasses).

## 🚀 Features

### Core Capabilities
- **🎤 Voice Recognition**: Hands-free voice commands using speech recognition
- **📷 Computer Vision**: Real-time webcam integration for visual context
- **🤖 Multimodal AI**: Combines voice and visual inputs using Google Gemini Pro Vision
- **🧠 Agentic AI**: Autonomous AI agents that can work independently and make decisions
- **🔧 LangChain Integration**: Advanced agent workflows with tool integration
- **💻 Code Generation**: Analyzes UI images and generates corresponding HTML/CSS code
- **🔄 Git Integration**: Automatic code generation and Git workflow automation
- **🌐 Web Interface**: Modern web-based camera interface for visual prompts

### Technical Stack
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Electron.js
- **Backend**: Python 3.12+ with OpenCV, Speech Recognition
- **AI Integration**: Google Gemini Pro Vision API, LangChain
- **Agentic AI**: Autonomous agents with tool integration
- **Desktop App**: Electron.js with Node.js 20.19.0
- **Version Control**: Git with automated workflow

## 🧠 Agentic AI Capabilities

AURA features advanced agentic AI that can work autonomously, similar to Culey's approach:

### 🤖 Autonomous Agents
- **Self-Directing**: AI agents that can plan and execute tasks independently
- **Tool Integration**: Access to search, code generation, and automation tools
- **Decision Making**: Agents can make informed decisions based on context
- **Multi-Step Workflows**: Complex task execution without human intervention

### 🔧 Agent Tools & Capabilities
- **Web Search**: DuckDuckGo integration for real-time information
- **Code Generation**: Automatic HTML/CSS generation from visual inputs
- **File Management**: Autonomous file creation and organization
- **Git Operations**: Automated version control and repository management
- **API Integration**: Seamless connection with external services

### 🎯 Agentic Workflows
- **Multimodal Processing**: Agents process voice + vision inputs simultaneously
- **Context Awareness**: Agents maintain context across multiple interactions
- **Task Decomposition**: Complex tasks broken down into manageable steps
- **Autonomous Execution**: Agents work independently to complete objectives

## 📋 Prerequisites

### System Requirements
- **macOS**: 10.15+ (Catalina or later)
- **Architecture**: Apple Silicon (M1/M2/M3) or Intel x64
- **Node.js**: 20.19.0
- **npm**: 10.8.2
- **Python**: 3.12+ (recommended: use pyenv for version management)

### API Keys Required
- **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/anubhav100j/AURA.git
cd AURA
```

### 2. Python Environment Setup (Recommended: pyenv)
```bash
# Install pyenv (if not already installed)
brew install pyenv

# Add to your shell profile (~/.zshrc or ~/.bash_profile)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Reload shell
source ~/.zshrc

# Install Python 3.12.8
pyenv install 3.12.8
pyenv global 3.12.8
```

### 3. Install Python Dependencies
```bash
# Install required Python packages
pip install google-generativeai opencv-python speechrecognition pillow python-dotenv gitpython

# Or create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Node.js Environment Setup
```bash
# Install Node.js 20.19.0 (using nvm recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20.19.0
nvm use 20.19.0

# Install npm dependencies
cd app
npm install
```

### 5. Environment Configuration
```bash
# Create .env file in project root
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## 🚀 Usage

### Web Interface
1. Open `index.html` in your browser
2. Click "Use Webcam" to access your camera
3. Click "Capture Image" to take a photo
4. Enter your text prompt
5. Click "Send to AI" to process

### Python Multimodal Pipeline
```bash
# Run the full multimodal AI pipeline
python input.py
```

This will:
1. Capture an image from your webcam
2. Record your voice command
3. Process both inputs with Gemini AI
4. Generate HTML/CSS code
5. Open the result in your browser
6. Optionally commit to Git

### Desktop App (Electron)
```bash
cd app
npm start
```

## 📁 Project Structure

```
AURA/
├── app/                    # Electron desktop application
│   ├── package.json        # Node.js dependencies and scripts (Node 20.19.0, npm 10.8.2)
│   ├── main.js            # Electron main process
│   ├── index.html         # Desktop app interface
│   ├── node_modules/      # Node.js dependencies
│   └── package-lock.json  # Dependency lock file
├── backend/               # Python backend services
│   └── main_api.py        # Main API endpoints (under development)
├── input.py               # Main multimodal AI pipeline with LangChain agents
├── requirements.txt       # Python dependencies
├── input_image.jpg        # Captured webcam images
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

### 🔧 Current Components

**Frontend (Electron App)**
- `app/package.json` - Node.js configuration with engine requirements
- `app/main.js` - Electron main process for desktop app
- `app/index.html` - Desktop application interface

**Backend (Python)**
- `input.py` - Core multimodal AI pipeline with LangChain agents
- `backend/main_api.py` - API endpoints (in development)
- `requirements.txt` - Python dependencies including LangChain

**AI & Agentic Features**
- **Multimodal Processing**: Voice + Vision input processing
- **LangChain Integration**: Agent-based AI workflows
- **Autonomous Decision Making**: AI agents that can work independently
- **Tool Integration**: Search, code generation, and automation tools

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Git Configuration
The system can automatically commit generated code to your repositories. Configure your Git settings:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 🎯 Use Cases

### Development
- **UI Prototyping**: Capture design mockups and generate code
- **Rapid Development**: Convert visual concepts to working prototypes
- **Accessibility**: Hands-free development for accessibility needs

### Productivity
- **Smart Glasses Simulation**: Experience next-gen AI assistant capabilities
- **Multimodal Interaction**: Combine voice and visual inputs naturally
- **Automated Workflows**: Streamline development processes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the ISC License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**Python Installation Issues on Apple Silicon:**
```bash
# Use arch command for native arm64 installation
arch -arm64 pyenv install 3.12.8
```

**Webcam Permission Issues:**
- Ensure camera permissions are granted in System Preferences
- Try refreshing the browser page

**API Key Issues:**
- Verify your Gemini API key is correctly set in `.env`
- Check API quota and billing status

**Node.js Version Issues:**
```bash
# Use nvm to manage Node.js versions
nvm install 20.19.0
nvm use 20.19.0
```

## 🔮 Future Roadmap

### 🧠 Agentic AI Enhancements
- [ ] **Multi-Agent Systems**: Multiple specialized agents working together
- [ ] **Advanced Planning**: Hierarchical task planning and execution
- [ ] **Memory Systems**: Long-term and working memory for agents
- [ ] **Learning Capabilities**: Agents that improve from experience
- [ ] **Tool Ecosystem**: Expanded tool library for agents

### 🚀 Platform Features
- [ ] **Real-time Processing**: Live video and audio streaming
- [ ] **Advanced Voice Commands**: Natural language understanding
- [ ] **Mobile Integration**: iOS/Android companion apps
- [ ] **Cloud Deployment**: Scalable cloud infrastructure
- [ ] **Plugin Architecture**: Extensible agent capabilities

### 🔧 Technical Improvements
- [ ] **Enhanced AI Models**: Integration with latest AI models
- [ ] **Performance Optimization**: Faster processing
- [ ] **Security**: Enhanced privacy and security features
- [ ] **API Development**: RESTful API for external integrations

## 📞 Support

For support, email your-email@example.com or create an issue on GitHub.

---

**Built with ❤️ for the future of AI-assisted development**
