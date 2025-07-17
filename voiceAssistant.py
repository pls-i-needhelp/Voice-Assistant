import os
import time
import json
import logging
import tempfile
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import wikipedia
import webbrowser
import pywhatkit as kit
import pyjokes
import pyautogui
import requests
from bs4 import BeautifulSoup
from pywikihow import search_wikihow
import psutil
import speedtest

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Contact:
    name: str
    phone: str
    aliases: list

class VoiceAssistant:
    def __init__(self, config_file: str = "config.json"):
        """Initialize the voice assistant with configuration."""
        self.config = self._load_config(config_file)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.contacts = self._load_contacts()
        self.temp_dir = tempfile.gettempdir()
        
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            logger.error(f"Failed to adjust for ambient noise: {e}")
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        default_config = {
            "timeout": 5,
            "phrase_time_limit": 8,
            "pause_threshold": 1.0,
            "language": "en-in",
            "tts_language": "en",
            "tts_slow": False,
            "speech_delay": 0.5  
        }
        
        try:
            if Path(config_file).exists():
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            else:
                with open(config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default config file: {config_file}")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
        
        return default_config
    
    def _load_contacts(self) -> Dict[str, Contact]:
        """Load contacts from external file for security."""
        contacts_file = "contacts.json"
        contacts = {}
        
        try:
            if Path(contacts_file).exists():
                with open(contacts_file, 'r') as f:
                    contacts_data = json.load(f)
                    for contact_data in contacts_data:
                        contact = Contact(**contact_data)
                        contacts[contact.name] = contact
            else:
                logger.warning(f"Contacts file not found: {contacts_file}")
        except Exception as e:
            logger.error(f"Error loading contacts: {e}")
        
        return contacts
    
    def speak(self, text: str):
        """Convert text to speech using gtts and playsound."""
        if not text:
            return
            
        print(f"[Assistant]: {text}")
        logger.info(f"Speaking: {text}")
        
        try:
            filename = os.path.join(self.temp_dir, f"voice_{uuid.uuid4()}.mp3")
            
            tts = gTTS(
                text=text, 
                lang=self.config.get('tts_language', 'en'), 
                slow=self.config.get('tts_slow', False)
            )
            
            tts.save(filename)
            
            playsound(filename)
            
            try:
                os.remove(filename)
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup audio file {filename}: {cleanup_error}")
            
            time.sleep(self.config.get('speech_delay', 0.5))
            
        except Exception as e:
            logger.error(f"Speech failed: {e}")
            print(f"[Speech Error]: {e}")
            print(f"[TTS FAILED]: {text}")
    
    def listen(self) -> Optional[str]:
        """Listen for voice input and return recognized text."""
        try:
            with self.microphone as source:
                print("Listening...")
                self.recognizer.pause_threshold = self.config['pause_threshold']
                audio = self.recognizer.listen(
                    source, 
                    timeout=self.config['timeout'],
                    phrase_time_limit=self.config['phrase_time_limit']
                )
            
            print("Recognizing...")
            query = self.recognizer.recognize_google(
                audio, 
                language=self.config['language']
            )
            print(f"You said: {query}")
            logger.info(f"Recognized: {query}")
            return query.lower()
            
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except Exception as e:
            logger.error(f"Listen error: {e}")
            return None
    
    def greet(self):
        """Greet the user based on time of day."""
        hour = datetime.now().hour
        
        if 0 <= hour < 12:
            greeting = "Good Morning Sir"
        elif 12 <= hour < 17:
            greeting = "Good Afternoon Sir"
        else:
            greeting = "Good Evening Sir"
        
        self.speak(greeting)
        self.speak("How can I help you today?")
    
    def get_contact_number(self, name: str) -> Optional[str]:
        """Get contact number by name or alias."""
        name = name.lower()
        
        if name in self.contacts:
            return self.contacts[name].phone
        
        for contact in self.contacts.values():
            if name in [alias.lower() for alias in contact.aliases]:
                return contact.phone
        
        return None
    
    def send_whatsapp_message(self):
        """Send WhatsApp message to a contact."""
        try:
            self.speak("Whom do you want to send the message to?")
            recipient = self.listen()
            
            if not recipient:
                self.speak("I didn't catch that. Please try again.")
                return
            
            if 'cancel' in recipient or 'leave' in recipient:
                self.speak("Message cancelled.")
                return
            
            phone_number = self.get_contact_number(recipient)
            
            if not phone_number:
                self.speak("Contact not found. Please check the name and try again.")
                return
            
            self.speak("What's the message?")
            message = self.listen()
            
            if not message:
                self.speak("No message received. Canceling.")
                return
            
            if 'cancel' in message or 'leave' in message:
                self.speak("Message cancelled.")
                return
            
            self.speak("Should I send the message?")
            confirmation = self.listen()
            
            if confirmation and 'yes' in confirmation or 'send' in confirmation:
                kit.sendwhatmsg_instantly(phone_number, message, 5)
                self.speak("Message sent successfully.")
            else:
                self.speak("Message cancelled.")
            
        except Exception as e:
            logger.error(f"WhatsApp message error: {e}")
            self.speak("Sorry, I couldn't send the message.")
    
    def play_youtube_video(self):
        """Play video on YouTube."""
        try:
            self.speak("What would you like to watch?")
            query = self.listen()
            
            if query and 'cancel' not in query:
                self.speak(f"Playing {query} on YouTube")
                kit.playonyt(query)
            else:
                self.speak("Cancelled YouTube search.")
                
        except Exception as e:
            logger.error(f"YouTube play error: {e}")
            self.speak("Sorry, I couldn't play the video.")
    
    def search_wikipedia(self, query: str):
        """Search Wikipedia for information."""
        try:
            self.speak("Searching Wikipedia...")
            clean_query = query.replace('wikipedia', '').strip()
            
            if not clean_query:
                self.speak("Please specify what to search for.")
                return
            
            results = wikipedia.summary(clean_query, sentences=3)
            self.speak("According to Wikipedia:")
            self.speak(results)
            
        except wikipedia.exceptions.DisambiguationError as e:
            self.speak("Multiple results found. Please be more specific.")
            logger.info(f"Wikipedia disambiguation: {e.options[:3]}")
        except wikipedia.exceptions.PageError:
            self.speak("No Wikipedia page found for that query.")
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            self.speak("Sorry, I couldn't search Wikipedia right now.")
    
    def get_weather(self, location: str = "current location"):
        """Get current weather information."""
        try:
            self.speak("Checking weather information...")
            
            if location == "current location":
                response = requests.get('https://ipinfo.io/', timeout=5)
                data = response.json()
                location = data.get('city', 'your location')
            
            query = f"weather in {location}"
            url = f"https://www.google.com/search?q={query}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            
            temp_element = soup.find("div", class_="BNeawe")
            if temp_element:
                temperature = temp_element.text
                self.speak(f"The current temperature in {location} is {temperature}")
            else:
                self.speak("Sorry, I couldn't fetch the weather information.")
                
        except Exception as e:
            logger.error(f"Weather error: {e}")
            self.speak("Sorry, I couldn't get the weather information.")
    
    def get_system_battery(self):
        """Get battery percentage and status."""
        try:
            battery = psutil.sensors_battery()
            if battery:
                percentage = int(battery.percent)
                self.speak(f"Battery is at {percentage} percent")
                
                if percentage >= 75:
                    self.speak("Battery level is excellent.")
                elif percentage >= 50:
                    self.speak("Battery level is good.")
                elif percentage >= 25:
                    self.speak("Battery level is moderate. Consider charging soon.")
                elif percentage >= 15:
                    self.speak("Battery is getting low. Please charge.")
                else:
                    self.speak("Battery is very low. Please charge immediately.")
            else:
                self.speak("Unable to get battery information.")
                
        except Exception as e:
            logger.error(f"Battery error: {e}")
            self.speak("Sorry, I couldn't check the battery status.")
    
    def take_screenshot(self):
        """Take and save a screenshot."""
        try:
            self.speak("What should I name the screenshot?")
            name = self.listen()
            
            if not name or 'cancel' in name:
                self.speak("Screenshot cancelled.")
                return
            
            name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            
            if not name:
                name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self.speak("Taking screenshot in 3 seconds...")
            time.sleep(3)
            
            screenshot = pyautogui.screenshot()
            filename = f"{name}.png"
            screenshot.save(filename)
            
            self.speak(f"Screenshot saved as {filename}")
            
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            self.speak("Sorry, I couldn't take the screenshot.")
    
    def control_volume(self, action: str):
        """Control system volume."""
        try:
            if 'up' in action or 'increase' in action:
                pyautogui.press('volumeup')
                self.speak("Volume increased")
            elif 'down' in action or 'decrease' in action:
                pyautogui.press('volumedown')
                self.speak("Volume decreased")
            elif 'mute' in action:
                pyautogui.press('volumemute')
                self.speak("Volume muted")
            else:
                self.speak("I didn't understand the volume command.")
                
        except Exception as e:
            logger.error(f"Volume control error: {e}")
            self.speak("Sorry, I couldn't control the volume.")
    
    def get_internet_speed(self):
        """Test internet speed."""
        try:
            self.speak("Testing internet speed. Please wait...")
            
            st = speedtest.Speedtest()
            st=speedtest.Speedtest()
            download_speed = int((st.download())/8000000)
            upload_speed=int((st.upload())/8000000)
            
            self.speak(f"Download speed is {download_speed:.2f} megabits per second")
            self.speak(f"Upload speed is {upload_speed:.2f} megabits per second")
            
        except Exception as e:
            logger.error(f"Speed test error: {e}")
            self.speak("Sorry, I couldn't test the internet speed.")
    
    def tell_joke(self):
        """Tell a random joke."""
        try:
            joke = pyjokes.get_joke()
            self.speak(joke)
        except Exception as e:
            logger.error(f"Joke error: {e}")
            self.speak("Sorry, I couldn't get a joke right now.")
    
    def get_current_time(self):
        """Get and speak current time."""
        try:
            current_time = datetime.now().strftime("%I:%M %p")
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"The time is {current_time}")
            self.speak(f"Today is {current_date}")
        except Exception as e:
            logger.error(f"Time error: {e}")
            self.speak("Sorry, I couldn't get the current time.")
    
    def process_command(self, command: str):
        """Process voice commands."""
        command = command.lower()
        
        try:
            if 'wikipedia' in command:
                self.search_wikipedia(command)
            
            elif any(word in command for word in ['spotify', 'music']):
                self.speak("What would you like to listen to?")
                query = self.listen()
                if query and 'cancel' not in query:
                    webbrowser.open(f"https://open.spotify.com/search/{query}/tracks")
                    self.speak("Opening Spotify")
            
            elif 'youtube' in command and 'open' in command:
                webbrowser.open("https://www.youtube.com/")
                self.speak("Opening YouTube")
            
            elif 'play on youtube' in command or 'youtube play' in command:
                self.play_youtube_video()
            
            elif 'google' in command and 'search' in command:
                self.speak("What should I search on Google?")
                query = self.listen()
                if query and 'cancel' not in query:
                    kit.search(query)
                    self.speak("Searching on Google")
            
            elif any(word in command for word in ['time', 'date']):
                self.get_current_time()
            
            elif 'whatsapp' in command or 'send message' in command:
                self.send_whatsapp_message()
            
            elif any(word in command for word in ['pause', 'stop playing']):
                pyautogui.press('space')
                self.speak("Paused")
            
            elif 'joke' in command:
                self.tell_joke()
            
            elif 'weather' in command:
                self.get_weather()
            
            elif 'battery' in command:
                self.get_system_battery()
            
            elif 'screenshot' in command:
                self.take_screenshot()
            
            elif 'volume' in command:
                self.control_volume(command)
            
            elif 'internet speed' in command or 'speed test' in command:
                self.get_internet_speed()
            
            elif 'hello' in command or 'hi' in command:
                self.speak("Hello! How can I help you?")
            
            elif 'how are you' in command:
                self.speak("I'm doing well, thank you for asking! How can I assist you today?")
            
            elif 'what can you do' in command:
                self.speak("I can help you with many things like searching Wikipedia, playing YouTube videos, sending WhatsApp messages, checking weather, battery status, taking screenshots, controlling volume, and much more!")
            
            elif any(word in command for word in ['rest', 'sleep', 'stop']):
                self.speak("Going to rest mode. Say 'wake up' to activate me again.")
                return False
            
            elif any(word in command for word in ['goodbye', 'exit', 'quit']):
                self.speak("Goodbye! Have a great day!")
                return False
            
            else:
                self.speak("I didn't understand that command. Please try again or say 'what can you do' to see available commands.")
                
        except Exception as e:
            logger.error(f"Command processing error: {e}")
            self.speak("Sorry, I encountered an error processing that command.")
        
        return True
    
    def run(self):
        logger.info("Voice Assistant started")
        self.greet()
        
        try:
            while True:
                try:
                    command = self.listen()
                    
                    if command:
                        if any(wake_word in command for wake_word in ['wake up', 'wakeup', 'hey assistant']):
                            self.speak("I'm awake and ready to help!")
                            self.speak("What can I do for you?")
                            while True:
                                user_input = self.listen()
                                if user_input:
                                    if not self.process_command(user_input):
                                        break
                                else:
                                    print("I'm still listening...")
                                    continue
                        
                        elif any(word in command for word in ['goodbye', 'exit', 'quit']):
                            self.speak("Goodbye! Have a great day!")
                            break
                        
                        else:
                            self.speak("Say 'wake up' to activate me.")
                    
                    else:
                        continue
                        
                except KeyboardInterrupt:
                    logger.info("Voice Assistant stopped by user")
                    self.speak("Goodbye!")
                    break
                except Exception as e:
                    logger.error(f"Main loop error: {e}")
                    continue
        
        finally:
            try:
                temp_files = [f for f in os.listdir(self.temp_dir) if f.startswith('voice_') and f.endswith('.mp3')]
                for temp_file in temp_files:
                    try:
                        os.remove(os.path.join(self.temp_dir, temp_file))
                    except:
                        pass
            except:
                pass

def main():
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
