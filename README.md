# Voice Assistant

A sophisticated Python-based voice assistant designed to perform a wide range of tasks through voice commands, utilizing Google Text-to-Speech for high-quality speech output to streamline daily operations.

## Features

- **Voice Recognition**: Advanced speech-to-text using Google Speech Recognition.
- **Natural Speech**: High-quality text-to-speech with Google TTS.
- **WhatsApp Integration**: Send messages to contacts via voice commands.
- **Web Automation**: Perform Google searches, play YouTube videos, and open websites.
- **Wikipedia Search**: Retrieve information from Wikipedia.
- **Music Control**: Play music on Spotify and control media playback.
- **Weather Information**: Access current weather conditions.
- **Screenshot Capture**: Capture and save screenshots with custom names.
- **System Monitoring**: Monitor battery status and system information.
- **Contact Management**: Manage contacts with aliases for easy access.
- **Entertainment**: Provide jokes and other entertainment features.
- **System Control**: Adjust volume, manage files, and perform system operations.
- **Internet Speed Test**: Test internet connection speed.
- **Configurable**: Customizable settings via JSON configuration files.

## Requirements

- Python 3.7 or higher
- Stable internet connection (required for TTS and select features)
- Microphone for voice input
- Speakers or headphones for audio output

## Installation

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
   - The application automatically generates `config.json` and `contacts.json` on first run.
   - Alternatively, manually create them using the provided examples.

## Project Structure

```
Voice-Assistant/
├── main.py                 # Main application file
├── config.json            # Configuration settings
├── contacts.json          # Contact information
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── assistant.log          # Application logs
└── screenshots/           # Screenshot storage (created automatically)
```

## Configuration

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

## Usage

1. **Start the assistant:**
```bash
python main.py
```

2. **Activate the assistant:**
   - Say "wake up" or "hey assistant" to initiate interaction.
   - The assistant will respond and await commands.

3. **Give voice commands:**
   - Speak clearly into the microphone.
   - Wait for the assistant's response.
   - Use natural language for commands.

## Voice Commands

### Information and Search
- "search wikipedia for [topic]" - Retrieve Wikipedia information.
- "google search [query]" - Perform a Google search.
- "what's the weather" - Access weather information.
- "what's the time" - Retrieve current time and date.

### Media and Entertainment
- "play [song/video] on youtube" - Play YouTube content.
- "open spotify" - Launch Spotify.
- "pause" - Pause current media.
- "tell me a joke" - Hear a random joke.

### Communication
- "send whatsapp message" - Send WhatsApp messages.
- "send message to [contact]" - Send a message to a specific contact.

### System Control
- "take screenshot" - Capture the screen.
- "check battery" - Monitor battery status.
- "volume up/down/mute" - Adjust system volume.
- "test internet speed" - Test internet connection speed.

### Web Navigation
- "open youtube" - Access YouTube.
- "open google" - Access Google.
- "open [website]" - Open specified websites.

### Conversation
- "hello" - Greet the assistant.
- "how are you" - Inquire about assistant status.
- "what can you do" - List available capabilities.
- "rest" - Put assistant in sleep mode.
- "goodbye" - Exit the application.

## Troubleshooting

### Common Issues
1. **Microphone not working:**
   - Verify microphone permissions.
   - Ensure the microphone is not muted.
   - Test the microphone with other applications.
2. **Speech recognition errors:**
   - Speak clearly at a normal pace.
   - Ensure a stable internet connection.
   - Minimize background noise interference.
3. **TTS not working:**
   - Confirm internet connectivity.
   - Check speaker or headphone connections.
   - Ensure audio drivers are updated.
4. **Import errors:**
   - Install all dependencies: `pip install -r requirements.txt`.
   - Verify Python version compatibility.

### Debugging
- Review `assistant.log` for detailed error messages.
- Enable verbose logging by adjusting the log level in the code.
- Test individual components separately.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Text-to-Speech for high-quality speech synthesis.
- SpeechRecognition library for robust voice input processing.
- Python libraries that enabled this project.

## Future Enhancements

- Expand voice command repertoire.
- Implement offline speech recognition.
- Develop a graphical user interface.
- Integrate with smart home devices.
- Add calendar and reminder functionalities.
- Implement voice authentication.
- Support multiple languages.
- Develop a mobile application version.

## Support

For issues or questions:
1. Review the troubleshooting section.
2. Check existing GitHub issues.
3. Create a new issue with detailed information.
4. Contact the maintainers.

## Attribution

Developed by Raghav Bhatia.
