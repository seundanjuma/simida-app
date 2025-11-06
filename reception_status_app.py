import tkinter as tk
import requests

SERVER_URL = "http://192.168.0.10:5000"  # ← change this to your server's IP


class ReceptionistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Receptionist Dashboard")
        self.root.geometry("240x180")
        self.root.configure(bg="#cccccc")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "#cccccc")

        # Container (rounded style)
        self.container = tk.Frame(
            self.root, bg="#ffffff", bd=0, highlightthickness=1, relief="solid"
        )
        self.container.pack(expand=True, fill="both", padx=3, pady=3)
        self.container.config(highlightbackground="#aaaaaa")

        # Title bar
        self.header = tk.Frame(self.container, bg="#eeeeee", height=25)
        self.header.pack(fill="x", side="top")

        # Close/minimise buttons
        self.close_btn = tk.Button(
            self.header,
            text="×",
            command=self.root.destroy,
            bd=0,
            bg="#eeeeee",
            activebackground="#ff5555",
            font=("Arial", 10, "bold"),
            padx=5,
            pady=0,
        )
        self.close_btn.pack(side="right", padx=3)

        self.min_btn = tk.Button(
            self.header,
            text="–",
            command=self.minimize,
            bd=0,
            bg="#eeeeee",
            activebackground="#aaaaaa",
            font=("Arial", 10, "bold"),
            padx=5,
            pady=0,
        )
        self.min_btn.pack(side="right")

        # Title
        self.title_label = tk.Label(
            self.container, text="doctor status", font=("Arial", 12, "bold"), bg="#ffffff"
        )
        self.title_label.pack(pady=(5, 0))

        # Status frame
        self.status_frame = tk.Frame(self.container, bg="#ffffff")
        self.status_frame.pack(fill="both", expand=True, pady=(5, 5))

        # Make entire window draggable
        for widget in (self.root, self.container, self.header, self.status_frame):
            widget.bind("<Button-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)

        self.refresh_data()

    def draw_status_circle(self, parent, color):
        """Draw a larger coloured circle."""
        canvas = tk.Canvas(parent, width=40, height=40, bg="#ffffff", highlightthickness=0)
        circle = canvas.create_oval(5, 5, 35, 35, fill=color, outline=color)
        return canvas, circle

    def animate_change(self, canvas, circle, new_color):
        """Slight scale animation on status change (no cumulative shrink)."""
        canvas.itemconfig(circle, fill=new_color, outline=new_color)
        for _ in range(2):
            canvas.scale(circle, 20, 20, 0.9, 0.9)
            canvas.update()
            canvas.after(50)
        for _ in range(2):
            canvas.scale(circle, 20, 20, 1.1, 1.1)
            canvas.update()
            canvas.after(50)
        canvas.scale(circle, 20, 20, 1.0, 1.0)

    def refresh_data(self):
        """Fetch live doctor statuses from the server."""
        # clear frame
        for widget in self.status_frame.winfo_children():
            widget.destroy()

        try:
            response = requests.get(f"{SERVER_URL}/get_status", timeout=2)
            data = response.json() if response.status_code == 200 else {}
        except Exception:
            data = {}

        # draw each doctor row
        for doctor, status in data.items():
            row = tk.Frame(self.status_frame, bg="#ffffff")
            row.pack(fill="x", pady=6, padx=10)

            color = "green" if status == "available" else "red"
            circle_canvas, circle_item = self.draw_status_circle(row, color)
            circle_canvas.pack(side="left", padx=(0, 10))

            label = tk.Label(row, text=doctor, font=("Arial", 11), bg="#ffffff")
            label.pack(side="left")

            self.animate_change(circle_canvas, circle_item, color)

        self.root.after(2000, self.refresh_data)

    def minimize(self):
        self.root.iconify()

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        x = event.x_root - self.offset_x
        y = event.y_root - self.offset_y
        self.root.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ReceptionistApp(root)
    root.mainloop()
