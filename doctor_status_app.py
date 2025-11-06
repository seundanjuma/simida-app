import tkinter as tk
import time
import threading
import json
import os

# identify this doctor's office
DOCTOR_NAME = "Dr. A"  # change to "Dr. B" on the second PC

# path to shared file (make sure both PCs point to the same file)
STATUS_FILE = r"\\RHYC-VIDEO\simida\doctor_status.json"  # update Z:\ to your mapped network drive


class SimidaApp:
    def __init__(self, root):
        self.root = root
        self.is_green = False  # starts as red (occupied)
        self.sync_interval = 5  # seconds

        # window setup
        self.root.title("Simida")
        self.root.geometry("120x120")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg="#cccccc")
        self.root.wm_attributes("-transparentcolor", "#cccccc")

        # frame
        self.frame = tk.Frame(self.root, bg="#cccccc")
        self.frame.pack(expand=True, fill="both")

        # circular button
        self.button = tk.Canvas(self.frame, width=100, height=100, bg="#cccccc", highlightthickness=0)
        self.button.pack(pady=10)
        self.button_circle = self.button.create_oval(
            5, 5, 95, 95,
            fill="red",
            outline="#880000",
            width=2
        )

        # bind interactions
        self.button.bind("<Button-1>", self.animate_click)
        self.button.bind("<Enter>", self.on_hover)
        self.button.bind("<Leave>", self.on_leave)

        # title bar
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

        # make draggable anywhere
        for widget in (self.title_bar, self.frame, self.button):
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<B1-Motion>", self.on_move)

        # start background sync pulse
        threading.Thread(target=self.auto_refresh, daemon=True).start()

    def animate_click(self, event):
        for scale in [0.94, 1.0]:
            self.scale_button(scale)
            self.root.update()
            time.sleep(0.07)
        self.toggle_status()

    def scale_button(self, scale):
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
        self.is_green = not self.is_green
        color = "green" if self.is_green else "red"
        outline = "#006600" if self.is_green else "#880000"
        self.button.itemconfig(self.button_circle, fill=color, outline=outline)
        self.update_status_file()

    def update_status_file(self):
        """writes this doctor's status to the shared JSON"""
        data = {}
        if os.path.exists(STATUS_FILE):
            try:
                with open(STATUS_FILE, "r") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        data[DOCTOR_NAME] = "available" if self.is_green else "occupied"
        with open(STATUS_FILE, "w") as f:
            json.dump(data, f)

    def on_hover(self, event):
        color = "#cc0000" if not self.is_green else "#00cc00"
        self.button.itemconfig(self.button_circle, fill=color)

    def on_leave(self, event):
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
        """adds a small animation pulse periodically"""
        while True:
            time.sleep(self.sync_interval)
            for width in [3, 2]:
                self.button.itemconfig(self.button_circle, width=width)
                self.root.update()
                time.sleep(0.05)


if __name__ == "__main__":
    root = tk.Tk()
    app = SimidaApp(root)
    root.mainloop()
