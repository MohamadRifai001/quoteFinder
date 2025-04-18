import os
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import google.generativeai as genai


# Get API key from environment variable
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()

# Configure the API key
genai.configure(api_key=GOOGLE_API_KEY)

# model, using gemini 2.0 flash since it is the best version available for free tier.
model = genai.GenerativeModel('gemini-2.0-flash')

# simple user input function
def get_user_input():
    """Gets text input from the user."""
    return input("You: ")

def generate_ai_response(prompt):
    """Sends the prompt to the Gemini model and returns the response."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

def main():
    """Main application loop."""
    print("Simple Gemini AI Chat Application")
    print("Type 'quit' to exit.")

    while True:
        user_prompt = get_user_input()
        if user_prompt.lower() == 'quit':
            break

        ai_response = generate_ai_response(user_prompt)
        print(f"AI: {ai_response}")

if __name__ == "__main__":
    main()