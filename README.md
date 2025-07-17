# Voice Assistant

A powerful, feature-rich voice assistant built with Python that can perform various tasks through voice commands. This assistant uses Google Text-to-Speech for natural speech output and provides a wide range of functionalities to help automate your daily tasks.

## ✨ Features

- 🎯 **Voice Recognition**: Advanced speech-to-text using Google's speech recognition
- 🔊 **Natural Speech**: High-quality text-to-speech using Google TTS
- 📱 **WhatsApp Integration**: Send messages to contacts via voice commands
- 🌐 **Web Automation**: Search Google, play YouTube videos, open websites
- 📚 **Wikipedia Search**: Get information from Wikipedia
- 🎵 **Music Control**: Play music on Spotify, control media playback
- 🌤️ **Weather Information**: Get current weather conditions
- 📸 **Screenshot Capture**: Take and save screenshots with custom names
- 🔋 **System Monitoring**: Check battery status and system information
- 📞 **Contact Management**: Manage contacts with aliases for easy access
- 🎪 **Entertainment**: Tell jokes and provide entertainment
- 🔧 **System Control**: Control volume, manage files, and system operations
- 📊 **Internet Speed Test**: Test your internet connection speed
- ⚙️ **Configurable**: Customizable settings via JSON configuration


## 📋 Requirements

- Python 3.7 or higher
- Internet connection (for TTS and some features)
- Microphone for voice input
- Speakers/headphones for audio output


## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/pls-i-needhelp/Voice-Assistant.git
cd Voice-Assistant
```

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

3. **Set up configuration files:**
    - The application will automatically create `config.json` and `contacts.json` on first run
    - Or manually create them using the examples provided below

## 📁 Project Structure

```
Voice-Assistant/
├── main.py                 # Main application file
├── config.json            # Configuration settings
├── contacts.json          # Contact information
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── assistant.log         # Application logs
└── screenshots/          # Screenshot storage (created automatically)
```


## ⚙️ Configuration

### config.json

```json
{
  "timeout": 5,
  "phrase_time_limit": 8,
  "pause_threshold": 1.0,
  "language": "en-in",
  "tts_language": "en",
  "tts_slow": false,
  "speech_delay": 0.5
}
```


### contacts.json

```json
[
  {
    "name": "mom",
    "phone": "+1234567890",
    "aliases": ["mother", "mama", "mummy"]
  },
  {
    "name": "dad",
    "phone": "+1234567891",
    "aliases": ["father", "papa", "daddy"]
  },
  {
    "name": "myself",
    "phone": "+1234567892",
    "aliases": ["me", "self", "my number"]
  }
]
```


## 🎮 Usage

1. **Start the assistant:**
```bash
python main.py
```

2. **Activate the assistant:**
    - Say "wake up" or "hey assistant" to activate
    - The assistant will greet you and wait for commands
3. **Give voice commands:**
    - Speak clearly into your microphone
    - Wait for the assistant to respond
    - Use natural language for commands

## 🗣️ Voice Commands

### 📚 Information \& Search

- `"search wikipedia for [topic]"` - Search Wikipedia
- `"google search [query]"` - Search Google
- `"what's the weather"` - Get weather information
- `"what's the time"` - Get current time and date


### 🎵 Media \& Entertainment

- `"play [song/video] on youtube"` - Play YouTube videos
- `"open spotify"` - Open Spotify
- `"pause"` - Pause current media
- `"tell me a joke"` - Get a random joke


### 📱 Communication

- `"send whatsapp message"` - Send WhatsApp messages
- `"send message to [contact]"` - Send message to specific contact


### 🔧 System Control

- `"take screenshot"` - Capture screen
- `"check battery"` - Check battery status
- `"volume up/down/mute"` - Control system volume
- `"test internet speed"` - Test internet connection


### 🌐 Web Navigation

- `"open youtube"` - Open YouTube
- `"open google"` - Open Google
- `"open [website]"` - Open specific websites


### 💬 Conversation

- `"hello"` - Greet the assistant
- `"how are you"` - Ask about assistant status
- `"what can you do"` - Get list of capabilities
- `"rest"` - Put assistant in sleep mode
- `"goodbye"` - Exit the application


## 🔧 Troubleshooting

### Common Issues:

1. **Microphone not working:**
    - Check microphone permissions
    - Ensure microphone is not muted
    - Test microphone with other applications
2. **Speech recognition errors:**
    - Speak clearly and at normal pace
    - Ensure stable internet connection
    - Check if background noise is interfering
3. **TTS not working:**
    - Verify internet connection
    - Check speaker/headphone connections
    - Ensure audio drivers are updated
4. **Import errors:**
    - Install all requirements: `pip install -r requirements.txt`
    - Check Python version compatibility

### 🐛 Debugging:

- Check `assistant.log` for detailed error messages
- Enable verbose logging by changing log level in the code
- Test individual components separately


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Text-to-Speech for high-quality speech synthesis
- SpeechRecognition library for voice input processing
- All the amazing Python libraries that make this project possible


## 🔮 Future Enhancements

- [ ] Add more voice commands
- [ ] Implement offline speech recognition
- [ ] Add GUI interface
- [ ] Integrate with smart home devices
- [ ] Add calendar and reminder features
- [ ] Implement voice authentication
- [ ] Add multi-language support
- [ ] Create mobile app version


## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section
2. Look through existing issues on GitHub
3. Create a new issue with detailed information
4. Contact the maintainers

## 🌟 Show Your Support

If you find this project helpful, please give it a ⭐ on GitHub!

**Made with ❤️ by Raghav Bhatia**

*Happy Voice Controlling! 🎤*
