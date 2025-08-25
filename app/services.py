

import hashlib
import os
import requests
import json
from dotenv import load_dotenv
import logging
try:
    import google.generativeai as genai
except ImportError:
    genai = None
try:
    import openai
except ImportError:
    openai = None
from PIL import Image
import io
import base64


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("content_moderator")


def hash_content(content: str) -> str:
    """Hash the content with SHA-256"""
    return hashlib.sha256(content.encode()).hexdigest()


def image_to_base64(url: str) -> str:
    """Convert image URL to base64 format"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        logger.error(f"Image download error: {e}")
        return ""


def moderate_text(text: str) -> dict:
    """Classify text using Gemini or OpenAI"""
    if GEMINI_API_KEY and genai:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
            Classify this text as toxic, spam, harassment, or safe.
            Return the answer in JSON format as follows:
            {{
                "classification": "toxic/spam/harassment/safe",
                "confidence": 0.0-1.0,
                "reasoning": "Reason here"
            }}
            Text: {text}
            """
            response = model.generate_content(prompt)
            llm_response = response.text
            result = json.loads(llm_response.strip("```json\n").strip("```"))
            return {
                "classification": result["classification"],
                "confidence": result["confidence"],
                "reasoning": result["reasoning"],
                "llm_response": llm_response
            }
        except Exception as e:
            logger.error(f"Gemini error: {e}")
    elif OPENAI_API_KEY and openai:
        try:
            openai.api_key = OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a content moderation assistant. Classify the text as toxic, spam, harassment, or safe."},
                    {"role": "user", "content": text}
                ]
            )
            content = response.choices[0].message.content.lower()
            if "toxic" in content:
                classification = "toxic"
            elif "spam" in content:
                classification = "spam"
            elif "harassment" in content:
                classification = "harassment"
            else:
                classification = "safe"
            return {
                "classification": classification,
                "confidence": 1.0,
                "reasoning": content,
                "llm_response": content
            }
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
    # Dummy fallback
    logger.warning("No LLM API key or module missing, using dummy classification.")
    if "toxic" in text.lower():
        return {"classification": "toxic", "confidence": 0.95, "reasoning": "The word 'toxic' was found.", "llm_response": "..."}
    return {"classification": "safe", "confidence": 1.0, "reasoning": "Text is safe.", "llm_response": "..."}


def moderate_image(image_url: str) -> dict:
    """Classify image using Gemini or dummy logic"""
    if GEMINI_API_KEY and genai:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            base64_image = image_to_base64(image_url)
            if not base64_image:
                return {
                    "classification": "safe",
                    "confidence": 0.9,
                    "reasoning": "Image could not be loaded, defaulting to safe",
                    "llm_response": "Image loading error"
                }
            prompt = f"""
            Classify this image as toxic, spam, harassment, or safe.
            Return the answer in JSON format as follows:
            {{
                "classification": "toxic/spam/harassment/safe",
                "confidence": 0.0-1.0,
                "reasoning": "Reason here"
            }}
            Image (base64): data:image/png;base64,{base64_image}
            """
            response = model.generate_content(prompt)
            llm_response = response.text
            result = json.loads(llm_response.strip("```json\n").strip("```"))
            return {
                "classification": result["classification"],
                "confidence": result["confidence"],
                "reasoning": result["reasoning"],
                "llm_response": llm_response
            }
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            pass
    # Dummy fallback
    if "bad" in image_url:
        return {"classification": "toxic", "confidence": 0.9, "reasoning": "The word 'bad' was found in the URL.", "llm_response": "..."}
    return {"classification": "safe", "confidence": 0.9, "reasoning": "Image is safe.", "llm_response": "..."}


def send_notification(channel: str, message: str):
    """Send notification to Slack or log it"""
    if channel == "slack":
        if SLACK_WEBHOOK:
            try:
                response = requests.post(SLACK_WEBHOOK, json={"text": message})
                response.raise_for_status()
                logger.info(f"Slack notification sent: {message}")
            except Exception as e:
                logger.error(f"Slack notification failed: {e}")
        else:
            logger.warning("SLACK_WEBHOOK_URL is not set in .env!")
    else:
        logger.info(f"[NOTIFY][{channel}] {message}")