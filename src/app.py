import json
import os
from config import GOOGLE_API_KEY
from ai_service import configure_ai, generate_ai_response
from chat_ui import ChatUI
from pdf_processor import scan_and_embed_pdfs, semantic_search
# Safety check
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()

# Configure the model
model = configure_ai(GOOGLE_API_KEY, temperature=0)

# configure input folder
input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/input_pdfs")

scan_and_embed_pdfs(input_folder)

# cleans up the result so that it is formatted correctly for LLM
def format_for_llm(matches):
    formatted = []
    for doc, meta in zip(matches['documents'][0], matches['metadatas'][0]):
        formatted.append({
            "source_file": meta["source_file"],
            "page": meta["original_page"],
            "text": doc.strip()
        })
    return formatted





# Prompt engineering + AI logic
def handle_user_prompt(user_prompt):
    try:
        matches = semantic_search(user_prompt, top_k=5)
        filtered_pages = format_for_llm(matches)

        full_promp2 = f"""
        your task is to perform the following actions:
        1. Scan through each page of the given JSON object delimited by --- and find relevant quotes.
        2. For each quote remember the original page number and the source file name.
        3. Ensure that the quotes are no more than 3 sentences long.
        4. Ensure that the quotes DO NOT contain "\n" or "\r" characters.
        5. if no quote was found for the text, ignore that quote and move on to the next one.
        6. Select the 5 best quotes from all pages.
        7. return a JSON object similar to the inputed pages one where the text is replaced by the quote.


        Pages: ---{filtered_pages}---
        Topic: ```{user_prompt}```
        """

        response = generate_ai_response(model, full_promp2)

        # Tell the UI to display it
        ui.display_message("AI", response, tag="ai")
    except Exception as e:
        ui.display_message("Error", str(e))

# example prompt

# Identify a list of emotions that the writer of the \
# following review is expressing. Include no more than \
# five items in the list. Format your answer as a list of \
# lower-case words separated by commas.

# Set up UI with callback
ui = ChatUI(on_submit_callback=handle_user_prompt)
ui.run()

