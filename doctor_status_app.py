import tkinter as tk
from tkinter import ttk

class SimidaApp:
    def __init__(self, root):
        self.root = root
        self.is_green = False  # starts as red (occupied)

        # Window setup
        self.root.title("Simida")
        self.root.geometry("120x120")
        self.root.overrideredirect(True)  # remove default window borders
        self.root.attributes("-topmost", True)  # always on top
        self.root.config(bg="#cccccc")

        # Make window circular
        self.root.wm_attributes("-transparentcolor", "#cccccc")

        # Create a frame to hold everything
        self.frame = tk.Frame(self.root, bg="#cccccc")
        self.frame.pack(expand=True, fill="both")

        # Create bevel-style circular button
        self.button = tk.Canvas(
            self.frame,
            width=100,
            height=100,
            bg="#cccccc",
            highlightthickness=0
        )
        self.button.pack(pady=10)
        self.button_circle = self.button.create_oval(
            5, 5, 95, 95,
            fill="red",
            outline="#880000",
            width=2
        )

        # Bind click to toggle
        self.button.bind("<Button-1>", self.toggle_status)

        # Add custom title bar (for close/minimize)
        self.title_bar = tk.Frame(self.root, bg="#dddddd", relief="raised", bd=1)
        self.title_bar.place(x=0, y=0, relwidth=1, height=20)

        self.close_btn = tk.Button(
            self.title_bar, text="×", command=self.root.destroy,
            bd=0, bg="#dddddd", activebackground="#ff5555", font=("Arial", 10, "bold")
        )
        self.close_btn.pack(side="right", padx=3)

        self.min_btn = tk.Button(
            self.title_bar, text="–", command=self.minimize,
            bd=0, bg="#dddddd", activebackground="#aaaaaa", font=("Arial", 10, "bold")
        )
        self.min_btn.pack(side="right")

        # Allow window dragging
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)

    def toggle_status(self, event):
        """Toggle between red (busy) and green (free)."""
        self.is_green = not self.is_green
        if self.is_green:
            self.button.itemconfig(self.button_circle, fill="green", outline="#006600")
        else:
            self.button.itemconfig(self.button_circle, fill="red", outline="#880000")

    def minimize(self):
        """Minimize the window."""
        self.root.iconify()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimidaApp(root)
    root.mainloop()
