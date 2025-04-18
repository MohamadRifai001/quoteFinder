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

def generate_ai_response(prompt, output_text):
    """Sends the prompt to the Gemini model and updates the output text area."""
    try:
        response = model.generate_content(prompt)
        output_text.config(state=tk.NORMAL)  # Enable editing
        output_text.insert(tk.END, f"AI: {response.text}\n\n")
        output_text.config(state=tk.DISABLED) # Disable editing
        output_text.see(tk.END)             # Scroll to the end
    except Exception as e:
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, f"Error generating response: {e}\n\n")
        output_text.config(state=tk.DISABLED)
        output_text.see(tk.END)

def send_prompt():
    """Gets user input, sends it to the AI, and displays the response."""
    user_prompt = input_entry.get()
    if user_prompt:
        input_entry.delete(0, tk.END)  # Clear the input field
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, f"You: {user_prompt}\n")
        output_text.config(state=tk.DISABLED)
        output_text.see(tk.END)
        generate_ai_response(user_prompt, output_text)

def on_closing():
    """Handles window closing."""
    if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
        root.destroy()

# Create the main window
root = tk.Tk()
root.title("Simple Gemini AI Chat")

# Output display area (scrolled text)
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Input entry field
input_entry = tk.Entry(root)
input_entry.pack(padx=10, pady=5, fill=tk.X)

# Send button
send_button = tk.Button(root, text="Send", command=send_prompt)
send_button.pack(pady=5)

# Handle window closing
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()