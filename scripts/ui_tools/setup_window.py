"""
First-run setup window for IntelliSearch V2 .exe
Collects GitHub tokens and client key on first launch
"""

import tkinter as tk
from tkinter import messagebox
import os
import secrets
from pathlib import Path


class SetupWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("IntelliSearch V2 — First Run Setup")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Dark theme colors
        bg_color = "#0B0C12"
        fg_color = "#F5F3EE"
        accent_color = "#C9A84C"
        
        self.root.configure(bg=bg_color)
        
        # Title
        title = tk.Label(
            self.root,
            text="IntelliSearch V2",
            font=("Sora", 24, "bold"),
            bg=bg_color,
            fg=accent_color
        )
        title.pack(pady=20)
        
        subtitle = tk.Label(
            self.root,
            text="First Run Configuration",
            font=("Sora", 12),
            bg=bg_color,
            fg=fg_color
        )
        subtitle.pack()
        
        # Main frame
        frame = tk.Frame(self.root, bg=bg_color)
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # GitHub Token A
        tk.Label(frame, text="GitHub Token A (GPT-4o)", bg=bg_color, fg=fg_color, font=("Sora", 10, "bold")).pack(anchor="w", pady=(10, 5))
        self.token_a = tk.Entry(frame, show="*", font=("Sora", 9), bg="#1F1F27", fg=fg_color, border=1)
        self.token_a.pack(fill=tk.X, pady=(0, 10))
        
        # GitHub Token B
        tk.Label(frame, text="GitHub Token B (Llama 3.1)", bg=bg_color, fg=fg_color, font=("Sora", 10, "bold")).pack(anchor="w", pady=(10, 5))
        self.token_b = tk.Entry(frame, show="*", font=("Sora", 9), bg="#1F1F27", fg=fg_color, border=1)
        self.token_b.pack(fill=tk.X, pady=(0, 10))
        
        # Client Key
        tk.Label(frame, text="Client Key (or auto-generate)", bg=bg_color, fg=fg_color, font=("Sora", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        client_key_frame = tk.Frame(frame, bg=bg_color)
        client_key_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.client_key = tk.Entry(client_key_frame, font=("Sora", 9), bg="#1F1F27", fg=fg_color, border=1)
        self.client_key.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        generate_btn = tk.Button(
            client_key_frame,
            text="Generate",
            font=("Sora", 9),
            bg=accent_color,
            fg="#0B0C12",
            border=0,
            command=self.generate_client_key,
            padx=15
        )
        generate_btn.pack(side=tk.LEFT)
        
        # Help link
        help_label = tk.Label(
            frame,
            text="Need help? Visit: https://github.com/settings/tokens",
            bg=bg_color,
            fg="#888",
            font=("Sora", 8),
            justify=tk.LEFT
        )
        help_label.pack(anchor="w", pady=10)
        
        # Buttons
        button_frame = tk.Frame(frame, bg=bg_color)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Sora", 10),
            bg="#2A2A32",
            fg=fg_color,
            border=0,
            command=self.root.quit,
            padx=20,
            pady=10
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = tk.Button(
            button_frame,
            text="Save & Continue",
            font=("Sora", 10),
            bg=accent_color,
            fg="#0B0C12",
            border=0,
            command=self.save,
            padx=20,
            pady=10
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
    
    def generate_client_key(self):
        """Generate a random client key"""
        key = "sk-" + secrets.token_hex(32)
        self.client_key.delete(0, tk.END)
        self.client_key.insert(0, key)
    
    def save(self):
        """Save configuration to .env file"""
        token_a = self.token_a.get().strip()
        token_b = self.token_b.get().strip()
        client_key = self.client_key.get().strip()
        
        if (not token_a and not token_b) or not client_key:
            messagebox.showerror("Validation", "Provide at least one token and a client key")
            return

        # If only one token is provided, reuse it for both model calls.
        if token_a and not token_b:
            token_b = token_a
        if token_b and not token_a:
            token_a = token_b
        
        # Write .env file
        env_content = f"""GITHUB_TOKEN={token_a}
    GITHUB_TOKEN_A={token_a}
GITHUB_TOKEN_B={token_b}
GITHUB_MODELS_BASE_URL=https://models.github.ai/inference
CHROMA_PERSIST_DIR=./chroma_storage
CHROMA_COLLECTION_NAME=intellisearch_v2_corpus
CLIENT_KEY={client_key}
GPT4O_MODEL=gpt-4o
LLAMA_MODEL=Meta-Llama-3.1-405B-Instruct
TOP_K_RETRIEVAL=15
SIMILARITY_THRESHOLD=0.70
CHUNK_SIZE=512
CHUNK_OVERLAP=64
"""
        
        # Save to current directory or next to .exe
        env_path = Path(".env")
        env_path.write_text(env_content)
        
        messagebox.showinfo("Success", "Configuration saved! App will start shortly...")
        self.root.quit()


def main():
    """Check if .env exists, show setup if not"""
    if Path(".env").exists():
        # Skip setup if already configured
        return
    
    root = tk.Tk()
    app = SetupWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
