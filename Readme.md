# TaviGemChain 🤖

A smart research assistant that combines Google's Gemini AI with real-time web search capabilities to provide comprehensive, up-to-date answers to your questions.

## Features ✨

- **Real-time Web Search**: Automatically searches the web for relevant information using Tavily API
- **Content Extraction**: Scrapes and processes web content using Trafilatura
- **AI-Powered Responses**: Leverages Google's Gemini 2.0 Flash model for intelligent responses
- **Interactive Chat Interface**: Built with Chainlit for a smooth user experience
- **Streaming Responses**: Real-time response streaming for better UX

## Prerequisites 📋

- Python 3.8 or higher
- API keys for:
  - [Google Gemini API](https://makersuite.google.com/app/apikey)
  - [Tavily API](https://tavily.com/)

## Installation 🚀

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/chainlit-web-rag-bot.git
cd chainlit-web-rag-bot
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables:
```bash
cp .env.example .env
```

### 4. Edit `.env` file and add your API keys:
```env
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Usage 💬

Run the application:
```bash
chainlit run main.py -w
```

The chat interface will open in your browser at `http://localhost:8000`

## How It Works 🔍

1. **User Query**: You ask a question in the chat interface
2. **Web Search**: Tavily searches for relevant web pages
3. **Content Extraction**: Trafilatura extracts clean text from the URLs
4. **AI Processing**: Gemini processes your question with the web context
5. **Streaming Response**: The answer is streamed back to you in real-time

## Project Structure 📁

```
chainlit-web-rag-bot/
├── main.py           # Main application file
├── .env              # Environment variables (create from .env.example)
├── .env.example      # Template for environment variables
├── requirements.txt  # Python dependencies
├── README.md         # Project documentation
└── .gitignore        # Git ignore file
```

## Configuration ⚙️

You can adjust these settings in `main.py`:

- `max_results`: Number of web search results to process (default: 5)
- `chunk_size`: Size of text chunks for streaming (default: 5)
- `model`: Gemini model version (default: "gemini-2.0-flash-exp")

## Security 🔒

- **Never commit API keys**: Always use environment variables
- **Keep `.env` in `.gitignore`**: Prevent accidental key exposure
- **Rotate keys regularly**: If exposed, regenerate your API keys immediately

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- [Chainlit](https://github.com/Chainlit/chainlit) for the chat interface
- [Google Gemini](https://deepmind.google/technologies/gemini/) for the AI model
- [Tavily](https://tavily.com/) for web search API
- [Trafilatura](https://github.com/adbar/trafilatura) for web scraping

## Support 💪

If you find this project helpful, please give it a ⭐ on GitHub!

For issues or questions, please open an issue on the [GitHub repository](https://github.com/yourusername/chainlit-web-rag-bot/issues).
