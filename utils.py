# utils.py

import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def setup_gemini():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel("gemini-1.5-flash")


def get_technical_questions(prompt):
    try:
        model = setup_gemini()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Failed to generate questions: {str(e)}")


def get_fallback_response(user_input, context):
    """
    Get contextual fallback response from Gemini when input is unclear or off-topic.
    """
    try:
        model = setup_gemini()
        prompt = f"""
You are TalentScout – an intelligent hiring assistant helping conduct technical interviews.

A candidate has responded with: '{user_input}'  
Context: {context}

This input seems unclear or off-topic.  
Politely prompt the candidate to clarify or rephrase, while keeping the interview focused.
Avoid deviating from the technical interview purpose.
"""
        response = model.generate_content(prompt)
        return response.text
    except:
        return None


def is_unexpected_input(user_input):
    """
    Heuristic to detect off-topic, very short, or meaningless inputs.
    """
    if not user_input or len(user_input.strip()) < 2:
        return True
    if re.fullmatch(r"[^a-zA-Z0-9\s]+", user_input.strip()):
        return True  # Input is only symbols
    return False
