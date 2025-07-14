import os
import base64
import logging
from ollama import Client
from googletrans import Translator

from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

class LocalLLM:
    def __init__(self, host='http://127.0.0.1:11434'):
        self.client = Client(host=host)
        self.model_name = 'llava:7b'
        self.translator = Translator()

    def _translate_to_english(self, text):
        try:
            return self.translator.translate(text, src='bn', dest='en').text
        except Exception as e:
            logger.error(f"Translation to English failed: {str(e)}")
            return text

    def _translate_to_bangla(self, text):
        try:
            return self.translator.translate(text, src='en', dest='bn').text
        except Exception as e:
            logger.error(f"Translation to Bangla failed: {str(e)}")
            return text

    def _build_prompt(self, base_instruction, prompt, user_info=None):
        context = ""
        if user_info:
            if user_info.get('age'):
                context += f"The patient is {user_info['age']} years old. "
            if user_info.get('gender'):
                context += f"The patient's gender is {user_info['gender']}. "
        return f"You are Dr. Jhatka, a professional medical assistant. {context}{base_instruction}\n\nPatient: {prompt}\n\nDr. Jhatka:"



    def _encode_image(self, image_path_or_bytes):
        try:
            image = None

            if isinstance(image_path_or_bytes, bytes):
                image = Image.open(BytesIO(image_path_or_bytes))
            elif isinstance(image_path_or_bytes, str) and os.path.exists(image_path_or_bytes):
                image = Image.open(image_path_or_bytes)
            else:
                logger.error(f"Invalid image path or bytes: {image_path_or_bytes}")
                return None

            # Resize image to max 512x512 to reduce processing time
            image.thumbnail((512, 512))

            buffer = BytesIO()
            image.save(buffer, format='JPEG')
            buffer.seek(0)
            return base64.b64encode(buffer.read()).decode('utf-8')

        except Exception as e:
            logger.error(f"Image encoding failed: {str(e)}")
            return None


    def process_text_only(self, prompt, user_info=None, language="en"):
        try:
            if language == 'bn':
                prompt = self._translate_to_english(prompt)

            full_prompt = self._build_prompt(
                "Please provide helpful medical information based on the patient's query.",
                prompt,
                user_info
            )

            response = self.client.chat(model=self.model_name, messages=[{'role': 'user', 'content': full_prompt}])
            response_text = response.get('message', {}).get('content', '').strip()

            if "Dr. Jhatka:" in response_text:
                response_text = response_text.split("Dr. Jhatka:")[-1].strip()

            if not response_text:
                return "আমি দুঃখিত, আমি আপনার অনুরোধটি প্রক্রিয়া করতে পারিনি।" if language == 'bn' else "I'm sorry, I couldn't process your request."

            return self._translate_to_bangla(response_text) if language == 'bn' else response_text

        except Exception as e:
            logger.error(f"Error processing text query: {str(e)}")
            return "আমি দুঃখিত, আমি আপনার অনুরোধটি প্রক্রিয়া করতে সমস্যায় পড়েছি।" if language == 'bn' else "I'm sorry, I encountered an issue processing your request."

    def process_image_query(self, image_path_or_bytes, prompt="", user_info=None, language="en"):
        try:
            if language == 'bn':
                prompt = self._translate_to_english(prompt)

            full_prompt = self._build_prompt(
                "Please analyze the patient's medical image and provide a helpful response.",
                prompt,
                user_info
            )

            encoded_image = self._encode_image(image_path_or_bytes)
            if not encoded_image:
                return "ছবি প্রক্রিয়া করতে ব্যর্থ হয়েছে।" if language == 'bn' else "Failed to process image."

            response = self.client.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': full_prompt}],
                images=[encoded_image]
            )

            response_text = response.get('message', {}).get('content', '').strip()
            if "Dr. Jhatka:" in response_text:
                response_text = response_text.split("Dr. Jhatka:")[-1].strip()

            if not response_text:
                return "আমি দুঃখিত, আমি আপনার অনুরোধটি প্রক্রিয়া করতে পারিনি।" if language == 'bn' else "I'm sorry, I couldn't process your request."

            return self._translate_to_bangla(response_text) if language == 'bn' else response_text

        except Exception as e:
            logger.error(f"Error processing image query: {str(e)}")
            return "আমি দুঃখিত, আমি আপনার অনুরোধটি প্রক্রিয়া করতে সমস্যায় পড়েছি।" if language == 'bn' else "I'm sorry, I encountered an issue processing your request."
