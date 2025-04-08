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

    def provide_syntax_correction(user_input):
        try:
            # Provide a detailed prompt to Gemini for correcting the syntax
            enhanced_prompt = f"""
            The user provided the following command that caused a syntax error: '{user_input}'.

            Here are examples of correct syntax for our custom language:
            - BOOK 2 TICKETS TO "Reggae Sumfest" ON "2025-05-15" AT "8:30 AM" FOR "Joy Reynolds"
            - CONFIRM "Reggae Sumfest" FOR "Joy Reynolds"
            - PAY "Reggae Sumfest" FOR "Joy Reynolds"
            - CANCEL "Reggae Sumfest" FOR "Joy Reynolds"
            - LIST "Knutsford Express" SCHEDULE
            - LIST "Knutsford Express" ROUTE FROM "Kingston" TO "Montego Bay"

            Common mistakes include:
            - Forgetting to use the word "ON" before the date (e.g., "BOOK 2 TICKETS TO Reggae Sumfest February 17, 2025")
            - Missing quotes around event names or service names (e.g., "LIST Knutsford Express SCHEDULE")

            Please analyze the user input and provide the corrected version of the command in the correct format. Be sure to:
            - Point out the error
            - Suggest the correct syntax
            - Provide a friendly, easy-to-understand explanation for the user.
            """

            response = model.generate_content(enhanced_prompt)
            return response.text
        except Exception as e:
            print(f"[Gemini Error] {e}")
            return "[Gemini unavailable – using fallback]"


def provide_syntax_correction(user_input):
    try:
        enhanced_prompt = f"""
        The user provided the following command that caused a syntax error: '{user_input}'.

        Here are examples of correct syntax for our custom language:BOOK 2 TICKETS TO "Reggae Sumfest" ON "2025-05-15" AT "8:30 AM" FOR "Joy Reynolds"
        ,CONFIRM "Reggae Sumfest" FOR "Joy Reynolds", PAY "Reggae Sumfest" FOR "Joy Reynolds"
        ,CANCEL "Reggae Sumfest" FOR "Joy Reynolds", LIST "Knutsford Express" SCHEDULE,
        LIST "Knutsford Express" ROUTE FROM "Kingston" TO "Montego Bay"
        Common mistakes include: Forgetting to use the word "ON" before the date (e.g., "BOOK 2 TICKETS TO Reggae Sumfest February 17, 2025")
        ,Missing quotes around event names or service names (e.g., "LIST Knutsford Express SCHEDULE")
        Please analyze the user input and provide the corrected version of the command in the correct format. Be sure to:
        Point out the erro,Suggest the correct syntax,Provide a friendly, easy-to-understand explanation for the user.
        """

        response = model.generate_content(enhanced_prompt)
        return response.text
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return "[Gemini unavailable – using fallback]"
