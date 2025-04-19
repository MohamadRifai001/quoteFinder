import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class ChatUI:
    def __init__(self, on_submit_callback):
        self.on_submit = on_submit_callback

        self.root = tk.Tk()
        self.root.title("Simple Gemini AI Chat")

        self._configure_styles()
        self._build_widgets()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _configure_styles(self):
        style = ttk.Style(self.root)
        style.configure("TButton", padding=5, font=('Arial', 10))
        style.configure("TEntry", padding=5, font=('Arial', 10), foreground="#003366")
        style.configure("TScrolledtext.Vertical.TScrollbar", troughcolor="lightgray")
        style.configure("TScrolledtext.Horizontal.TScrollbar", troughcolor="lightgray")

    def _build_widgets(self):
        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, font=('Consolas', 10))
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.output_text.tag_configure("user", foreground="#228B22")
        self.output_text.tag_configure("ai", foreground="#1E3A8A")

        self.input_entry = ttk.Entry(self.root, style="TEntry")
        self.input_entry.pack(padx=10, pady=5, fill=tk.X)

        self.send_button = tk.Button(self.root, text="Submit", bg="#4CAF50", fg="white",
                                     font=('Arial', 10), padx=10, pady=5, command=self._handle_submit)
        self.send_button.pack()

    def _handle_submit(self):
        prompt = self.input_entry.get()
        if prompt:
            self.input_entry.delete(0, tk.END)
            self.display_message("You", prompt, tag="user")
            self.on_submit(prompt)  # Tell the app logic: "User submitted this"

    def display_message(self, sender, message, tag=None):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{sender}: {message}\n\n", tag)
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()