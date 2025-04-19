from config import GOOGLE_API_KEY
from ai_service import configure_ai, generate_ai_response
from chat_ui import ChatUI

# Safety check
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()

# Configure the model
model = configure_ai(GOOGLE_API_KEY, temperature=0)

# Prompt engineering + AI logic
def handle_user_prompt(prompt):
    try:
        # Do your prompt engineering here:
        full_prompt = f" Answer this question: \n{prompt}"

        response = generate_ai_response(model, full_prompt)

        # Tell the UI to display it
        ui.display_message("AI", response, tag="ai")
    except Exception as e:
        ui.display_message("Error", str(e))

# Set up UI with callback
ui = ChatUI(on_submit_callback=handle_user_prompt)
ui.run()



# # code for calling the pdf_processor function

# input_folder = "../data/input_pdfs"
# keywords = ["keyword1", "keyword2", "..."]  # Replace with actual keywords
# filtered_pages = scan_and_filter_pdf(input_folder, keywords)

# # Print to console (for debug)
# print(json.dumps(filtered_pages, indent=2))