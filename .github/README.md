# ChatNova AI

A commercial-grade multi-model AI chat application that combines the power of OpenAI GPT, Anthropic Claude, and Google Gemini into one seamless experience.

![ChatNova AI Logo](assets/logo.svg)

## 🚀 Features

- **Multi-AI Integration**: Support for OpenAI GPT-5, Anthropic Claude, and Google Gemini
- **AI Personas**: Four specialized modes - Creative Writer, Code Assistant, Business Expert, Research Pro
- **Document Processing**: Upload and chat with PDF, DOCX, TXT, and CSV files
- **Chat Management**: Create, rename, delete, and switch between multiple conversation threads
- **Export Functionality**: Download conversations as TXT or PDF files
- **Modern UI**: Clean, responsive interface with midnight blue and electric cyan theme
- **Persistent History**: All conversations are saved locally in your browser session
- **Customizable Settings**: API key management, model selection, theme toggle

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup Steps

1. **Clone or download the application:**
   ```bash
   # If you have the source code
   cd chatnova-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install streamlit openai anthropic google-genai PyPDF2 python-docx pandas reportlab fpdf
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py --server.port 5000
   ```

4. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

## ⚙️ Configuration

### API Keys
You'll need API keys from at least one of the following providers:

1. **OpenAI**: Get your key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. **Anthropic**: Get your key from [https://console.anthropic.com/](https://console.anthropic.com/)
3. **Google Gemini**: Get your key from [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### Environment Variables (Optional)
You can set API keys as environment variables:
```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export GEMINI_API_KEY="your-gemini-key"
