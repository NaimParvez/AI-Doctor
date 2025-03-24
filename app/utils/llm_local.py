import os
import logging
from ollama import Client
from PIL import Image
import base64

logger = logging.getLogger(__name__)

class LocalLLM:
    def __init__(self, host='http://localhost:11434'):
        self.client = Client(host=host)
        self.model_name = 'llava:7b'
        
    def process_text_only(self, prompt, user_info=None, language="en"):
        try:
            if user_info:
                user_context = ""
                if user_info.get('username'):
                    user_context += f"The patient's username is {user_info['username']}. "
                if user_info.get('age'):
                    user_context += f"The patient is {user_info['age']} years old. "
                if user_info.get('gender'):
                    user_context += f"The patient's gender is {user_info['gender']}. "
                if user_info.get('medical_history'):
                    if user_info['medical_history']:
                        user_context += f"The patient's medical history includes: {', '.join(user_info['medical_history'])}. "
                    else:
                        user_context += "The patient has no recorded medical history. "
                system_prompt = f"""You are Dr. Jhatka, a professional medical assistant. {user_context}
                Please provide helpful medical information point to point based on the patient's query. Suggestions should be tailored for Bangladesh, considering local healthcare practices and resources. Do not hallucinate. If the user sends a picture, verify that it aligns with their age and gender, as they might provide another person's image. If you find any dissimilarities, ask the user for clarification before proceeding. Also, consider previous responses with the user and their medical history when providing advice."""
            else:
                system_prompt = """You are Dr. Jhatka, a professional medical assistant.
                Please provide helpful medical information point to point based on the patient's query. Suggestions should be tailored for Bangladesh, considering local healthcare practices and resources. Do not hallucinate. If the user sends a picture, verify that it aligns with their age and gender, as they might provide another person's image. If you find any dissimilarities, ask the user for clarification before proceeding. Also, consider previous responses with the user and their medical history when providing advice."""
            full_prompt = f"{system_prompt}\n\nPatient: {prompt}\n\nDr. Jhatka:"
            logger.info(f"Sending prompt to LLaVA-7B: {full_prompt}")
            
            response = self.client.chat(model=self.model_name, messages=[
                {'role': 'user', 'content': full_prompt}
            ])
            response_text = response['message']['content'].split("Dr. Jhatka:")[-1].strip()
            logger.info(f"Received response: {response_text}")
            
            if not response_text or response_text.strip() == "":
                logger.warning("LLaVA-7B returned an empty response")
                return "I'm sorry, I couldn't process your request. Please try again or consult a local doctor."
            return response_text
        except Exception as e:
            logger.error(f"Error processing text query with Ollama: {e}")
            return "I'm sorry, I encountered an issue processing your request."

    def process_image_query(self, image_data, prompt, user_info=None, language="en"):
        try:
            if isinstance(image_data, str) and os.path.exists(image_data):
                with open(image_data, 'rb') as f:
                    image_bytes = f.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            else:
                return "Invalid image format or path."

            if user_info:
                user_context = ""
                if user_info.get('username'):
                    user_context += f"The patient's username is {user_info['username']}. "
                if user_info.get('age'):
                    user_context += f"The patient is {user_info['age']} years old. "
                if user_info.get('gender'):
                    user_context += f"The patient's gender is {user_info['gender']}. "
                if user_info.get('medical_history'):
                    if user_info['medical_history']:
                        user_context += f"The patient's medical history includes: {', '.join(user_info['medical_history'])}. "
                    else:
                        user_context += "The patient has no recorded medical history. "
                system_prompt = f"""You are Dr. Jhatka, a professional medical assistant. {user_context}
                Examine the uploaded medical image and provide insights based on what you see. Suggestions should be tailored for Bangladesh, considering local healthcare practices and resources. Do not hallucinate. Verify that the image aligns with the patient's age and gender, as they might provide another person's image. If you find any dissimilarities, ask the user for clarification before proceeding. Also, consider previous responses with the user and their medical history when providing advice."""
            else:
                system_prompt = """You are Dr. Jhatka, a professional medical assistant.
                Examine the uploaded medical image and provide insights based on what you see. Suggestions should be tailored for Bangladesh, considering local healthcare practices and resources. Do not hallucinate. Verify that the image aligns with the patient's age and gender, as they might provide another person's image. If you find any dissimilarities, ask the user for clarification before proceeding. Also, consider previous responses with the user and their medical history when providing advice."""
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
            
            if not response_text or response_text.strip() == "":
                logger.warning("LLaVA-7B returned an empty response for image query")
                return "I'm sorry, I couldn't process your request. Please try again or consult a local doctor."
            return response_text
        except Exception as e:
            logger.error(f"Error processing image query with Ollama: {e}")
            return "I'm sorry, I encountered an issue analyzing the image."

llm_service = LocalLLM(host=os.environ.get('OLLAMA_HOST', 'http://localhost:11434'))