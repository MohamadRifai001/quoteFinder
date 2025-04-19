import google.generativeai as genai

def configure_ai(api_key, temperature=0):
    """Configures the AI model with the given API key."""
    genai.configure(api_key=api_key)
    generation_config = {
        "temperature": temperature,
    }
    return genai.GenerativeModel('gemini-2.0-flash', generation_config=generation_config)

def generate_ai_response(model, prompt):
    """Generates a response from the AI model."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error generating AI response: {e}")