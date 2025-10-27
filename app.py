import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import google.generativeai as genai
from dotenv import load_dotenv
import threading
import time
import re

# Load environment variables
load_dotenv()

# Configure Google Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    messagebox.showerror("Error", "GOOGLE_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

class SongRecognizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 AI Song Recognizer")
        self.root.geometry("1200x850")  # Larger window
        self.root.configure(bg="#0a0e27")
        
        # Set minimum window size
        self.root.minsize(1000, 700)
        
        # Configure style
        self.setup_styles()
        
        # Create GUI elements
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def setup_styles(self):
        """Setup custom styles for widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure("Custom.TButton",
                       foreground="white",
                       background="#7c3aed",
                       borderwidth=0,
                       focuscolor="none",
                       font=("Segoe UI", 13, "bold"),
                       padding=15)
        style.map("Custom.TButton",
                 background=[("active", "#9333ea"), ("pressed", "#6d28d9")])
        
        # Configure label style
        style.configure("Title.TLabel",
                       background="#0a0e27",
                       foreground="#fbbf24",
                       font=("Segoe UI", 36, "bold"))
        
        style.configure("Subtitle.TLabel",
                       background="#0a0e27",
                       foreground="#c084fc",
                       font=("Segoe UI", 13))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#0a0e27")
        header_frame.pack(pady=30)
        
        # Title with gradient effect simulation
        title = ttk.Label(header_frame, 
                         text="🎵 AI Song Recognizer 🎵",
                         style="Title.TLabel")
        title.pack()
        
        subtitle = ttk.Label(header_frame,
                            text="Powered by Google Gemini AI • Find Any Song Instantly",
                            style="Subtitle.TLabel")
        subtitle.pack(pady=(5, 0))
        
        # Main container with padding
        main_frame = tk.Frame(self.root, bg="#0a0e27")
        main_frame.pack(padx=50, pady=20, fill="both", expand=True)
        
        # Input section with card-like container
        input_container = tk.Frame(main_frame, bg="#1e1b4b", relief="flat", bd=0)
        input_container.pack(fill="x", pady=(0, 20))
        
        input_label = tk.Label(input_container,
                              text="🎤 Enter Song Details",
                              bg="#1e1b4b",
                              fg="#fbbf24",
                              font=("Segoe UI", 16, "bold"))
        input_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        input_sublabel = tk.Label(input_container,
                                 text="Type song name, lyrics, or even broken sentences...",
                                 bg="#1e1b4b",
                                 fg="#a78bfa",
                                 font=("Segoe UI", 11))
        input_sublabel.pack(anchor="w", padx=20, pady=(0, 10))
        
        # Input text box with better styling
        self.input_text = tk.Text(input_container,
                                 height=5,
                                 font=("Segoe UI", 14),
                                 bg="#312e81",
                                 fg="#ffffff",
                                 insertbackground="#fbbf24",
                                 relief="flat",
                                 padx=20,
                                 pady=15,
                                 wrap="word",
                                 borderwidth=0)
        self.input_text.pack(fill="x", padx=20, pady=(0, 20))
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg="#0a0e27")
        button_frame.pack(pady=15)
        
        # Search button with icon
        self.search_button = ttk.Button(button_frame,
                                       text="🔍  Recognize Song",
                                       style="Custom.TButton",
                                       command=self.recognize_song_thread)
        self.search_button.pack(side="left", padx=10)
        
        # Clear button
        self.clear_button = ttk.Button(button_frame,
                                      text="🗑️  Clear All",
                                      style="Custom.TButton",
                                      command=self.clear_all)
        self.clear_button.pack(side="left", padx=10)
        
        # Progress bar (hidden by default)
        self.progress = ttk.Progressbar(main_frame,
                                       mode='indeterminate',
                                       length=500)
        
        # Output section with card-like container
        output_container = tk.Frame(main_frame, bg="#1e1b4b", relief="flat", bd=0)
        output_container.pack(fill="both", expand=True, pady=(10, 0))
        
        output_label = tk.Label(output_container,
                               text="📀 Song Information",
                               bg="#1e1b4b",
                               fg="#fbbf24",
                               font=("Segoe UI", 16, "bold"))
        output_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Output text box with scrollbar and better styling
        self.output_text = scrolledtext.ScrolledText(output_container,
                                                     height=18,
                                                     font=("Segoe UI", 12),
                                                     bg="#312e81",
                                                     fg="#ffffff",
                                                     relief="flat",
                                                     padx=25,
                                                     pady=20,
                                                     wrap="word",
                                                     borderwidth=0,
                                                     spacing1=3,
                                                     spacing2=2,
                                                     spacing3=3)
        self.output_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.output_text.config(state="disabled")
        
        # Configure text tags for better formatting
        self.output_text.tag_configure("bold", font=("Segoe UI", 13, "bold"), foreground="#fbbf24")
        self.output_text.tag_configure("header", font=("Segoe UI", 14, "bold"), foreground="#c084fc")
        
        # Status bar with gradient-like design
        status_frame = tk.Frame(self.root, bg="#1e1b4b", height=45)
        status_frame.pack(side="bottom", fill="x")
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame,
                                     text="✨ Ready to recognize songs • Powered by AI",
                                     bg="#1e1b4b",
                                     fg="#a78bfa",
                                     font=("Segoe UI", 11),
                                     anchor="w",
                                     padx=25)
        self.status_label.pack(fill="both", expand=True)
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def update_status(self, message):
        """Update status label safely from any thread"""
        self.root.after(0, lambda: self.status_label.config(text=message))
    
    def recognize_song_thread(self):
        """Start song recognition in a separate thread"""
        query = self.input_text.get("1.0", "end-1c").strip()
        
        if not query:
            messagebox.showwarning("⚠️ Empty Input", "Please enter song details to search!")
            return
        
        # Disable button and show progress
        self.search_button.config(state="disabled")
        self.clear_button.config(state="disabled")
        self.progress.pack(pady=15)
        self.progress.start(10)
        self.status_label.config(text="🔍 Analyzing your query with AI...")
        
        # Run recognition in separate thread
        thread = threading.Thread(target=self.recognize_song, args=(query,))
        thread.daemon = True
        thread.start()
    
    def recognize_song(self, query):
        """Recognize song using Google Gemini AI with retry logic"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # List available models, prefer flash over pro
                available_models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available_models.append(m.name)
                
                if not available_models:
                    raise Exception("No compatible models found. Please check your API key.")
                
                # Prefer flash models (faster and lower quota usage)
                flash_models = [m for m in available_models if 'flash' in m.lower()]
                model_name = flash_models[0] if flash_models else available_models[0]
                
                self.update_status(f"🎵 Using AI model: {model_name.split('/')[-1]}...")
                
                model = genai.GenerativeModel(model_name)
                
                # Create detailed prompt
                prompt = f"""
You are an expert music and song database. A user has provided the following input about a song:

"{query}"

Based on this input (which could be a song name, partial lyrics, broken sentences, or fragments), identify the song and provide comprehensive information in the following format:

**Song Name:** [Full name of the song]
**Movie/Album:** [Name of movie/album if applicable, otherwise mention "Independent Single" or artist album name]
**Artist(s):** [Singer(s) and music composer]
**Year:** [Release year]
**Language:** [Language of the song]
**Genre:** [Music genre]

**Description:**
[Provide a 3-4 sentence description about the song, its popularity, context in the movie (if applicable), and why it's memorable]

**Key Lyrics:**
[Provide 2-3 lines of the most famous/recognizable lyrics from this song]

**Trivia:**
[Share 1-2 interesting facts about this song]

If you cannot identify the song with certainty, provide your best guess with a confidence level and explain what information would help narrow it down.
"""
                
                # Generate response
                response = model.generate_content(prompt)
                result = response.text
                
                # Update GUI in main thread
                self.root.after(0, self.display_result, result)
                return
                
            except Exception as e:
                error_str = str(e)
                
                # Check if it's a quota error
                if "429" in error_str or "quota" in error_str.lower():
                    # Extract wait time from error message
                    wait_time = 20  # Default wait time
                    match = re.search(r'retry in (\d+\.?\d*)', error_str)
                    if match:
                        wait_time = int(float(match.group(1))) + 2
                    
                    if attempt < max_retries - 1:
                        self.update_status(f"⏳ Rate limit hit. Waiting {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        error_msg = f"❌ Rate Limit Exceeded\n\n"
                        error_msg += f"You've reached the free tier quota limit.\n\n"
                        error_msg += f"💡 Solutions:\n"
                        error_msg += f"1. Wait a few minutes and try again\n"
                        error_msg += f"2. The free tier resets every 24 hours\n"
                        error_msg += f"3. Current limit: 15 requests/minute, 1500 requests/day\n"
                        error_msg += f"4. Monitor usage at: https://ai.dev/usage\n\n"
                        error_msg += f"⏰ Please try again in a few minutes."
                        self.root.after(0, self.display_result, error_msg)
                        return
                else:
                    # Other errors
                    error_msg = f"❌ Error: {error_str}\n\n💡 Solution:\n"
                    error_msg += "1. Make sure your API key is from: https://aistudio.google.com/app/apikey\n"
                    error_msg += "2. Verify the key in your .env file\n"
                    error_msg += "3. Check internet connection"
                    self.root.after(0, self.display_result, error_msg)
                    return
    
    def display_result(self, result):
        """Display the recognition result with enhanced formatting"""
        # Enable output text
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        
        # Insert formatted text
        lines = result.split('\n')
        for line in lines:
            if line.strip().startswith('**') and line.strip().endswith('**'):
                # Bold headers
                clean_line = line.replace('**', '')
                self.output_text.insert("end", clean_line + '\n', "header")
            elif '**' in line:
                # Parse inline bold
                parts = line.split('**')
                for i, part in enumerate(parts):
                    if i % 2 == 1:  # Bold part
                        self.output_text.insert("end", part, "bold")
                    else:
                        self.output_text.insert("end", part)
                self.output_text.insert("end", '\n')
            else:
                self.output_text.insert("end", line + '\n')
        
        self.output_text.config(state="disabled")
        
        # Hide progress bar and enable buttons
        self.progress.stop()
        self.progress.pack_forget()
        self.search_button.config(state="normal")
        self.clear_button.config(state="normal")
        
        if "❌" in result:
            self.status_label.config(text="⚠️ Request failed - see details above")
        else:
            self.status_label.config(text="✅ Song recognized successfully! 🎉")
    
    def clear_all(self):
        """Clear all text fields"""
        self.input_text.delete("1.0", "end")
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.config(state="disabled")
        self.status_label.config(text="✨ Ready to recognize songs • Powered by AI")

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = SongRecognizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()