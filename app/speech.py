import os
import logging
import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment

logger = logging.getLogger(__name__)

class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    
    def speech_to_text(self, audio_file_path, language="en-US"):
        try:
            # Convert MP3 to WAV if necessary
            if audio_file_path.endswith('.mp3'):
                sound = AudioSegment.from_mp3(audio_file_path)
                wav_path = audio_file_path.replace('.mp3', '.wav')
                sound.export(wav_path, format="wav")
                audio_file_path = wav_path

            # Use speech_recognition to transcribe
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                transcription = self.recognizer.recognize_google(audio, language=language)

            logger.info(f"Transcribed text: {transcription} (language: {language})")
            if audio_file_path.endswith('.wav') and 'temp' in audio_file_path:
                os.remove(audio_file_path)
            return transcription if transcription else "Speech transcription failed."
        except Exception as e:
            logger.error(f"Error in speech-to-text: {e}")
            return "Speech transcription failed."
    
    def detect_language(self, audio_file_path, language_hint="en"):
        # Since we're only supporting English, always return "en"
        return "en"
    
    def text_to_speech(self, text, output_path, language="en"):
        try:
            logger.info(f"Generating speech for text: {text} (language: {language})")
            self.tts_engine.save_to_file(text, output_path)
            self.tts_engine.runAndWait()
            return output_path
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return None

speech_service = SpeechService()