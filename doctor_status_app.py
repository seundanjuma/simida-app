import tkinter as tk
import time
import threading

class SimidaApp:
    def __init__(self, root):
        self.root = root
        self.is_green = False  # starts as red (occupied)
        self.sync_interval = 5  # seconds

        # Window setup
        self.root.title("Simida")
        self.root.geometry("120x120")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg="#cccccc")
        self.root.wm_attributes("-transparentcolor", "#cccccc")

        # Frame
        self.frame = tk.Frame(self.root, bg="#cccccc")
        self.frame.pack(expand=True, fill="both")

        # Canvas button (circular)
        self.button = tk.Canvas(self.frame, width=100, height=100, bg="#cccccc", highlightthickness=0)
        self.button.pack(pady=10)

        self.button_circle = self.button.create_oval(
            5, 5, 95, 95,
            fill="red",
            outline="#880000",
            width=2
        )

        # Bind interactions
        self.button.bind("<Button-1>", self.animate_click)
        self.button.bind("<Enter>", self.on_hover)
        self.button.bind("<Leave>", self.on_leave)

        # Title bar
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

        # Window drag
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)

        # Start auto-refresh (simulate sync)
        threading.Thread(target=self.auto_refresh, daemon=True).start()

    def animate_click(self, event):
        """Scale button down slightly, then back up."""
        for scale in [0.94, 1.0]:
            self.scale_button(scale)
            self.root.update()
            time.sleep(0.07)
        self.toggle_status()

    def scale_button(self, scale):
        """Resize the circle smoothly."""
        self.button.delete(self.button_circle)
        size = 90 * scale
        offset = (100 - size) / 2
        color = "green" if self.is_green else "red"
        outline = "#006600" if self.is_green else "#880000"
        self.button_circle = self.button.create_oval(
            offset, offset, offset + size, offset + size,
            fill=color,
            outline=outline,
            width=2
        )

    def toggle_status(self):
        """Toggle between red (busy) and green (free)."""
        self.is_green = not self.is_green
        color = "green" if self.is_green else "red"
        outline = "#006600" if self.is_green else "#880000"
        self.button.itemconfig(self.button_circle, fill=color, outline=outline)

    def on_hover(self, event):
        """Subtle darken on hover (~10%)."""
        color = "#cc0000" if not self.is_green else "#00cc00"
        self.button.itemconfig(self.button_circle, fill=color)

    def on_leave(self, event):
        """Restore normal color."""
        color = "green" if self.is_green else "red"
        outline = "#006600" if self.is_green else "#880000"
        self.button.itemconfig(self.button_circle, fill=color, outline=outline)

    def minimize(self):
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

    def auto_refresh(self):
        """Simulate backend sync every few seconds."""
        while True:
            time.sleep(self.sync_interval)
            print("[Auto-refresh] Syncing status...")
            # Subtle pulse animation
            for width in [3, 2]:
                self.button.itemconfig(self.button_circle, width=width)
                self.root.update()
                time.sleep(0.05)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimidaApp(root)
    root.mainloop()
