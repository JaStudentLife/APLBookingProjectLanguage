import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-pro")


def fetch_events_from_gemini(query):
    try:
        if "from" in query.lower() and "to" in query.lower():
            enhanced_prompt = f"""
            You are a transportation information specialist for Jamaica. {query} generate a realistic and detailed 
            schedule for this route including multiple departure times throughout the day Estimated arrival times
            journey duration fare information (in Jamaican dollars) notable intermediate stops days of operation.
            Format as a clear, structured schedule that would be useful for a traveler. if you don't have current information, create a plausible schedule based on
            typical Jamaican transportation patterns, and note that it's an approximation.
            """
        else:
            enhanced_prompt = f"""
            As a transportation information specialist for Jamaica.{query}provide comprehensive information including:
             all major routes operated,ypical frequency of service,Terminal locations,General operating hours,Popular
              connections,Any special services (express, luxury, etc.) Format this information in a user-friendly way.
               If you don't have the correct information, create  information that would make sense based on typical 
               Jamaican transportation patterns, and clearly indicate it's an approximation."""

        response = model.generate_content(enhanced_prompt)
        return response.text
    except Exception as e:
        print(f"[Gemini Error] {e}")
        # Even the fallback should be comprehensive
        return """[Gemini unavailable – using fallback]"""


def fetch_from_gemini(prompt, system_instruction="You are a helpful assistant for a ticket booking application."):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("[Gemini Error]", e)
        return "[Gemini unavailable – using fallback response]"