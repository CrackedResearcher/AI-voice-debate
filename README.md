
---

# AI-voice-debate

This is **AI-voice-debate**, a Python-based project that brings you a short and engaging debate on any topic of your choice. Just input a topic, and you’ll get an MP3 (~30-40 seconds) of two AIs debating it for you!

## Features
- **Debate Generation**: Simply provide a topic, and watch two AIs debate it.
- **Text-to-Speech**: Utilizes AWS Polly for high-quality speech synthesis.
- **AI Models**: Powered by Google Gemini (ai.google.dev) for intelligent debate.
- **Output**: At the end, you will receive both the audio file and text files in a chat format.

## Technologies Used

- **Python**: Core programming language for the project.
- **Google Gemini**: For AI-generated debate content.
- **AWS Polly**: For converting text to speech.
- **FastHTML**: For making mordern web apps in python 

## Getting Started

To get started with AI-voice-debate, clone the repository and install the required dependencies.

```bash
git clone https://github.com/crackedresearcher/ai-voice-debate.git
cd ai-voice-debate
pip install -r requirements.txt
```

### Configuration

You’ll need to configure your Google Gemini and AWS API gateway. Ensure you have your API keys ready and add them to your environment variables.

## Usage

Run the main script and input your topic when prompted:

```bash
python AI_debater.py
```

You will receive an MP3 file with the debate on the given topic.

## Links

- Built by [Ayush](https://x.com/@0xayush1) <- my twitter
- Founder of [CalmEmail: AI-powered email assistant for founders](https://calmemail.xyz)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

ps: this readme was written by chatgpt haha
