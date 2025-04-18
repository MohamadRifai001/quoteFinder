import os
import google.generativeai as genai

# google api key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=GOOGLE_API_KEY)

# model, using gemini 2.0 flash since it is the best version available for free tier.
model = genai.GenerativeModel('gemini-2.0-flash')

prompt_parts = [
    "You are a helpful and concise assistant.",  # Similar to a system message
    "User: Explain the concept of photosynthesis in simple terms.",  # User message
]

generation_config_focused = {
    "temperature": 0,
}


response = model.generate_content(prompt_parts, generation_config=generation_config_focused)
print(response.text)





# Example of using the chat interface
# chat = model.start_chat()
# response = chat.send_message("Hello, I'm learning about the solar system.")
# print(f"Model: {response.text}")
# response = chat.send_message("Tell me an interesting fact about Jupiter.")
# print(f"Model: {response.text}")