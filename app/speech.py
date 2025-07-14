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
        self.tts_engine.setProperty('rate', 150)     # Speech speed
        self.tts_engine.setProperty('volume', 0.9)   # Volume (0.0 to 1.0)

    def speech_to_text(self, audio_file_path, language="en-US"):
        try:
            is_temp = False

            # Convert MP3 to WAV if necessary
            if audio_file_path.endswith('.mp3'):
                sound = AudioSegment.from_mp3(audio_file_path)
                wav_path = audio_file_path.replace('.mp3', '_temp.wav')
                sound.export(wav_path, format="wav")
                audio_file_path = wav_path
                is_temp = True

            # Use speech_recognition to transcribe
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                transcription = self.recognizer.recognize_google(audio, language=language)

            logger.info(f"Transcribed text: {transcription} (language: {language})")

            # Clean up temporary WAV file
            if is_temp and os.path.exists(audio_file_path):
                os.remove(audio_file_path)

            return transcription if transcription else "Speech transcription failed."

        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand the audio.")
            return "Could not understand the audio."
        except sr.RequestError as e:
            logger.error(f"Google Speech Recognition API error: {e}")
            return "Speech recognition service error."
        except Exception as e:
            logger.error(f"Error in speech-to-text: {e}")
            return "Speech transcription failed."

    def detect_language(self, audio_file_path, language_hint="en"):
        """
        Placeholder function for future language detection from audio.
        Currently returns the given hint (defaults to 'en').
        """
        return language_hint

    def text_to_speech(self, text, output_path, language="en"):

        try:
            if not text.strip():
                logger.warning("Empty text received for TTS.")
                return None

            logger.info(f"Generating speech for text: {text[:50]}... (language: {language}) → {output_path}")
            self.tts_engine.save_to_file(text, output_path)
            self.tts_engine.runAndWait()
            return output_path

        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return None

# Create singleton instance
speech_service = SpeechService()
