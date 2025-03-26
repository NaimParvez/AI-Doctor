import os
import logging
from ollama import Client
from PIL import Image
import base64
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class LocalLLM:
    def __init__(self, host='http://localhost:11434'):
        self.client = Client(host=host)
        self.model_name = 'llava:7b'
        self.host = host
        
    @retry(
        stop=stop_after_attempt(3),  # Retry up to 3 times
        wait=wait_exponential(multiplier=1, min=2, max=10),  # Exponential backoff: 2s, 4s, 8s
        retry=retry_if_exception_type(Exception),  # Retry on any exception
        before_sleep=lambda retry_state: logger.warning(
            f"Retrying connection to Ollama (attempt {retry_state.attempt_number}/3)..."
        )
    )
    def _chat_with_ollama(self, messages):
        """Helper method to handle Ollama chat with retry logic."""
        try:
            logger.info(f"Attempting to connect to Ollama at {self.host}")
            response = self.client.chat(model=self.model_name, messages=messages)
            return response
        except Exception as e:
            logger.error(f"Failed to connect to Ollama at {self.host}: {str(e)}")
            raise

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
                    user_context += f"The patient's medical history includes: {user_info['medical_history']} "
                else:
                    user_context += "The patient has no recorded medical history. "
                # Add previous conversation to the context
                previous_conversation = user_info.get('previous_conversation', [])
                conversation_context = "Previous conversation:\n"
                if previous_conversation:
                    for message in previous_conversation:
                        sender = "User" if message['sender'] == 'user' else "Doctor"
                        text_content = message['text'] or ""
                        image_info = f" (with image: {message['image_path']})" if message['image_path'] else ""
                        conversation_context += f"{sender} at {message['timestamp']}: {text_content}{image_info}\n"
                else:
                    conversation_context += "No previous conversation available.\n"
                user_context += conversation_context

                system_prompt = f"""You are Dr. Jhatka, a professional medical assistant. {user_context}
                Your goal is to make the user feel they are chatting with a real doctor who knows their background. Respond in a professional, empathetic, and conversational tone, as if you are chatting with the patient. Follow this exact response pattern:

                Hello [Username]! I’m Dr. Jhatka, and I’m here to assist you with your health concerns. I see that you are a [age]-year-old [gender]. Based on your medical history, I note that [medical_history]. Let me also recap our previous conversation: [summarize previous conversation, if any, in a concise sentence, e.g., "you mentioned having a cough last time"].

                I understand that [rephrase the user's query to show empathy, e.g., "you’re experiencing a cough, which must be quite uncomfortable"]. Let’s address this concern:

                - [Provide actionable advice tailored to the user’s age, gender, medical history, and previous conversation. Consider local healthcare practices and resources in Bangladesh.]
                - [Additional advice, ensuring it’s relevant and practical.]
                - [More advice if needed, with references to local resources like Upazila Health Complexes or pharmacies in Bangladesh.]

                Please take care, [Username]. How are you feeling now, or do you have any other concerns I can help with?

                Additional instructions:
                - Tailor suggestions for Bangladesh, considering local healthcare practices and resources.
                - Do not hallucinate. If unsure, suggest consulting a local doctor.
                - Use a professional yet approachable tone, avoiding overly technical jargon.
                - Ensure the advice is safe and considers the user’s medical history (e.g., allergies)."""
            else:
                system_prompt = """You are Dr. Jhatka, a professional medical assistant.
                Your goal is to make the user feel they are chatting with a real doctor. Respond in a professional, empathetic, and conversational tone, as if you are chatting with the patient. Follow this exact response pattern:

                Hello! I’m Dr. Jhatka, and I’m here to assist you with your health concerns. I don’t have your personal details, so my advice will be general.

                I understand that [rephrase the user's query to show empathy]. Let’s address this concern:

                - [Provide general actionable advice, considering local healthcare practices in Bangladesh.]
                - [Additional advice, ensuring it’s practical.]
                - [More advice if needed, with references to local resources.]

                Please take care. How are you feeling now, or do you have any other concerns I can help with?

                Additional instructions:
                - Tailor suggestions for Bangladesh, considering local healthcare practices and resources.
                - Do not hallucinate. If unsure, suggest consulting a local doctor.
                - Use a professional yet approachable tone, avoiding overly technical jargon."""
            
            full_prompt = f"{system_prompt}\n\nPatient: {prompt}\n\nDr. Jhatka:"
            logger.info(f"Sending prompt to LLaVA-7B: {full_prompt}")
            
            response = self._chat_with_ollama(messages=[
                {'role': 'user', 'content': full_prompt}
            ])
            response_text = response['message']['content'].split("Dr. Jhatka:")[-1].strip()
            logger.info(f"Received response: {response_text}")
            
            if not response_text or response_text.strip() == "":
                logger.warning("LLaVA-7B returned an empty response")
                return "I'm sorry, I couldn't process your request. Please try again or consult a local doctor."
            return response_text
        except Exception as e:
            logger.error(f"Error processing text query with Ollama: {str(e)}")
            return "I'm sorry, I encountered an issue processing your request."

    def process_image_query(self, image_data, prompt, user_info=None, language="en"):
        try:
            # Validate image file
            if isinstance(image_data, str) and os.path.exists(image_data):
                # Check if the file is a valid image
                try:
                    with Image.open(image_data) as img:
                        img.verify()  # Verify that it's a valid image
                except Exception as e:
                    logger.error(f"Invalid image file {image_data}: {str(e)}")
                    return "The uploaded file is not a valid image. Please upload a valid image file (e.g., PNG, JPG)."
                
                with open(image_data, 'rb') as f:
                    image_bytes = f.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            else:
                logger.warning(f"Invalid image path: {image_data}")
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
                    user_context += f"The patient's medical history includes: {user_info['medical_history']} "
                else:
                    user_context += "The patient has no recorded medical history. "
                # Add previous conversation to the context
                previous_conversation = user_info.get('previous_conversation', [])
                conversation_context = "Previous conversation:\n"
                if previous_conversation:
                    for message in previous_conversation:
                        sender = "User" if message['sender'] == 'user' else "Doctor"
                        text_content = message['text'] or ""
                        image_info = f" (with image: {message['image_path']})" if message['image_path'] else ""
                        conversation_context += f"{sender} at {message['timestamp']}: {text_content}{image_info}\n"
                else:
                    conversation_context += "No previous conversation available.\n"
                user_context += conversation_context

                system_prompt = f"""You are Dr. Jhatka, a professional medical assistant. {user_context}
                Your goal is to make the user feel they are chatting with a real doctor who knows their background. Respond in a professional, empathetic, and conversational tone, as if you are chatting with the patient. Follow this exact response pattern:

                Hello [Username]! I’m Dr. Jhatka, and I’m here to assist you with your health concerns. I see that you are a [age]-year-old [gender]. Based on your medical history, I note that [medical_history]. Let me also recap our previous conversation: [summarize previous conversation, if any, in a concise sentence, e.g., "you mentioned having a cough last time"].

                I understand that [rephrase the user's query to show empathy, e.g., "you’ve shared an image of a rash, which might be concerning for you"]. Let’s address this concern based on the image:

                - [Provide actionable advice based on the image, tailored to the user’s age, gender, medical history, and previous conversation. Consider local healthcare practices in Bangladesh.]
                - [Additional advice, ensuring it’s relevant and practical. Verify the image aligns with the user’s age and gender; if not, ask for clarification.]
                - [More advice if needed, with references to local resources like Upazila Health Complexes or pharmacies in Bangladesh.]

                Please take care, [Username]. How are you feeling now, or do you have any other concerns I can help with?

                Additional instructions:
                - Verify that the image aligns with the patient’s age and gender. If there are dissimilarities, ask for clarification before proceeding (e.g., "The image appears to show a child’s skin, but you are a 35-year-old male. Can you confirm if this image is of your skin?").
                - Tailor suggestions for Bangladesh, considering local healthcare practices and resources.
                - Do not hallucinate. If unsure, suggest consulting a local doctor.
                - Use a professional yet approachable tone, avoiding overly technical jargon.
                - Ensure the advice is safe and considers the user’s medical history (e.g., allergies)."""
            else:
                system_prompt = """You are Dr. Jhatka, a professional medical assistant.
                Your goal is to make the user feel they are chatting with a real doctor. Respond in a professional, empathetic, and conversational tone, as if you are chatting with the patient. Follow this exact response pattern:

                Hello! I’m Dr. Jhatka, and I’m here to assist you with your health concerns. I don’t have your personal details, so my advice will be general.

                I understand that [rephrase the user's query to show empathy]. Let’s address this concern based on the image:

                - [Provide general actionable advice based on the image, considering local healthcare practices in Bangladesh.]
                - [Additional advice, ensuring it’s practical.]
                - [More advice if needed, with references to local resources.]

                Please take care. How are you feeling now, or do you have any other concerns I can help with?

                Additional instructions:
                - Tailor suggestions for Bangladesh, considering local healthcare practices and resources.
                - Do not hallucinate. If unsure, suggest consulting a local doctor.
                - Use a professional yet approachable tone, avoiding overly technical jargon."""
            
            full_prompt = f"{system_prompt}\n\nPatient's question: {prompt}\n\nDr. Jhatka:"
            logger.info(f"Sending image prompt to LLaVA-7B: {full_prompt}")
            
            response = self._chat_with_ollama(messages=[
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
                return "I'm sorry, I couldn’t process your request. Please try again or consult a local doctor."
            return response_text
        except Exception as e:
            logger.error(f"Error processing image query with Ollama: {str(e)}")
            return "I'm sorry, I encountered an issue analyzing the image."

llm_service = LocalLLM(host=os.environ.get('OLLAMA_HOST', 'http://localhost:11434'))