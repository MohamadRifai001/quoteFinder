import os
import tkinter as tk
from tkinter import ttk
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
        output_text.insert(tk.END, f"AI: {response.text}\n\n", "ai")
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
        output_text.insert(tk.END, f"You: {user_prompt}\n\n", "user")
        output_text.config(state=tk.DISABLED)
        output_text.see(tk.END)

        output_text.update_idletasks() ## Update the UI before generating the response

        generate_ai_response(user_prompt, output_text)

def on_closing():
    """Handles window closing."""
    if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
        root.destroy()

# Create the main window
root = tk.Tk()
root.title("Simple Gemini AI Chat")


#styles
style = ttk.Style(root)
style.configure("TButton", padding=5, font=('Arial', 10))
style.configure("TEntry", padding=5, font=('Arial', 10), foreground="#003366")
style.configure("TScrolledtext.Vertical.TScrollbar", troughcolor="lightgray")
style.configure("TScrolledtext.Horizontal.TScrollbar", troughcolor="lightgray")



# Output display area (scrolled text)
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=('Consolas', 10))
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# display output and input as different colors
output_text.tag_configure("user", foreground="#228B22")
output_text.tag_configure("ai", foreground="#1E3A8A")

# Input entry field
input_entry = ttk.Entry(root, style="TEntry")
input_entry.pack(padx=10, pady=5, fill=tk.X)

# Send button
send_button = tk.Button(root, text="Submit", bg="#4CAF50", fg="white", font=('Arial', 10), padx=10, pady=5, command=send_prompt)
send_button.pack()
#pady = 5

# Handle window closing
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()