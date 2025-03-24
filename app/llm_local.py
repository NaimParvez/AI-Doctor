import os
import logging
from ollama import Client
from PIL import Image
import base64
from googletrans import Translator

logger = logging.getLogger(__name__)

class LocalLLM:
    def __init__(self, host='http://localhost:11434'):
        self.client = Client(host=host)
        self.model_name = 'llava:7b'
        self.translator = Translator()
        
    def process_text_only(self, prompt, user_info=None, language="en"):
        try:
            # Translate Bangla to English if needed
            original_language = language
            if language == 'bn':
                prompt = self.translator.translate(prompt, src='bn', dest='en').text
                logger.info(f"Translated Bangla prompt to English: {prompt}")

            if user_info:
                user_context = ""
                if user_info.get('age'):
                    user_context += f"The patient is {user_info['age']} years old. "
                if user_info.get('gender'):
                    user_context += f"The patient's gender is {user_info['gender']}. "
                system_prompt = f"""You are Dr. Jhatka, a professional medical assistant. {user_context}
                Please provide helpful medical information based on the patient's query."""
            else:
                system_prompt = """You are Dr. Jhatka, a professional medical assistant.
                Please provide helpful medical information based on the patient's query."""
            full_prompt = f"{system_prompt}\n\nPatient: {prompt}\n\nDr. Jhatka:"
            logger.info(f"Sending prompt to LLaVA-7B: {full_prompt}")
            
            response = self.client.chat(model=self.model_name, messages=[
                {'role': 'user', 'content': full_prompt}
            ])
            response_text = response['message']['content'].split("Dr. Jhatka:")[-1].strip()
            logger.info(f"Received response: {response_text}")
            
            # Translate response back to Bangla if needed
            if original_language == 'bn':
                response_text = self.translator.translate(response_text, src='en', dest='bn').text
                logger.info(f"Translated response to Bangla: {response_text}")

            if not response_text or response_text.strip() == "":
                logger.warning("LLaVA-7B returned an empty response")
                return "আমি দুঃখিত, আমি আপনার অনুরোধটি বাংলায় প্রক্রিয়া করতে পারিনি। অনুগ্রহ করে ইংরেজিতে চেষ্টা করুন বা স্থানীয় ডাক্তারের সাথে পরামর্শ করুন।" if original_language == 'bn' else "I'm sorry, I couldn't process your request in Bangla. Please try in English or consult a local doctor."
            return response_text
        except Exception as e:
            logger.error(f"Error processing text query with Ollama: {e}")
            return "আমি দুঃখিত, আমি আপনার অনুরোধটি প্রক্রিয়া করতে সমস্যায় পড়েছি।" if language == 'bn' else "I'm sorry, I encountered an issue processing your request."

    def process_image_query(self, image_data, prompt, user_info=None, language="en"):
        try:
            if isinstance(image_data, str) and os.path.exists(image_data):
                with open(image_data, 'rb') as f:
                    image_bytes = f.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            else:
                return "Invalid image format or path."

            # Translate Bangla to English if needed
            original_language = language
            if language == 'bn':
                prompt = self.translator.translate(prompt, src='bn', dest='en').text
                logger.info(f"Translated Bangla prompt to English: {prompt}")

            if user_info:
                user_context = ""
                if user_info.get('age'):
                    user_context += f"The patient is {user_info['age']} years old. "
                if user_info.get('gender'):
                    user_context += f"The patient's gender is {user_info['gender']}. "
                system_prompt = f"""You are Dr. Jhatka, a professional medical assistant. {user_context}
                Examine the uploaded medical image and provide insights based on what you see."""
            else:
                system_prompt = """You are Dr. Jhatka, a professional medical assistant.
                Examine the uploaded medical image and provide insights based on what you see."""
            full_prompt = f"{system_prompt}\n\nPatient's question: {prompt}\n\nDr. Jhatka:"
            logger.info(f"Sending image prompt to LLaVA-7B: {full_prompt}")
            
            response = self.client.chat(model=self.model_name, messages=[
                {
                    'role': 'user',
                    'content': full_prompt,
                    'images': [image_base64]
                }
            ])
            response_text = response['message']['content'].split("Dr. Jhatka:")[-1].strip()
            logger.info(f"Received image response: {response_text}")
            
            # Translate response back to Bangla if needed
            if original_language == 'bn':
                response_text = self.translator.translate(response_text, src='en', dest='bn').text
                logger.info(f"Translated response to Bangla: {response_text}")

            if not response_text or response_text.strip() == "":
                logger.warning("LLaVA-7B returned an empty response for image query")
                return "আমি দুঃখিত, আমি আপনার অনুরোধটি বাংলায় প্রক্রিয়া করতে পারিনি। অনুগ্রহ করে ইংরেজিতে চেষ্টা করুন বা স্থানীয় ডাক্তারের সাথে পরামর্শ করুন।" if original_language == 'bn' else "I'm sorry, I couldn't process your request in Bangla. Please try in English or consult a local doctor."
            return response_text
        except Exception as e:
            logger.error(f"Error processing image query with Ollama: {e}")
            return "আমি দুঃখিত, আমি ছবিটি বিশ্লেষণ করতে সমস্যায় পড়েছি।" if language == 'bn' else "I'm sorry, I encountered an issue analyzing the image."

llm_service = LocalLLM(host=os.environ.get('OLLAMA_HOST', 'http://localhost:11434'))