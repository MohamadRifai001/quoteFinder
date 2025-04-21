import json
import os
from config import GOOGLE_API_KEY
from ai_service import configure_ai, generate_ai_response
from chat_ui import ChatUI
from pdf_processor import scan_and_collect_pages
# Safety check
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()

# Configure the model
model = configure_ai(GOOGLE_API_KEY, temperature=0)

# configure input folder
input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/input_pdfs")

# Prompt engineering + AI logic
def handle_user_prompt(user_prompt):
    try:
        # Do your prompt engineering here:
        full_prompt = f"""
        your task is to perform the following actions:
        1. Identify a list of the main keywords from the Essay Question or topic delimited by ```
        2. For each keyword, find the top 5 synonyms from the thesaurus.
        give the list of the keywords along with the top 5 synonyms for each keyword.
        3. Ensure that the synonyms are relevant to the given topic.
        4. Provide a list of keywords and their synonyms as lowercase words separated by commas.
        Do not include any introductory phrases, headings, bullet points, or other formatting.
        ```{user_prompt}```
        """

        keywordResponse = generate_ai_response(model, full_prompt)
        keywords = keywordResponse.split(",") # turns it into a list
        keywords = [kw.strip().lower() for kw in keywords] # removes white space and makes it lowercase
        keywords = list(set(keywords)) # removes duplicates incase there are any

        print(json.dumps(keywords, indent=2))   # print for debug

        filtered_pages = scan_and_collect_pages(input_folder, keywords)

        print(json.dumps(filtered_pages, indent=2)) #print for debug

        full_promp2 = f"""
        your task is to perform the following actions:
        1. Scan through each page of the given JSON object delimited by --- and find relevant quotes.
        2. For each quote remember the original page number and the source file name.
        3. Ensure that the quotes are no more than 3 sentences long.
        4. Ensure that the quotes DO NOT contain "\n" or "\r\n" characters.
        5. if no quote was found for the text, simply replace the text with "no quote found"
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

