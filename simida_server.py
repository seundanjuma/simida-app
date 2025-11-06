import tkinter as tk
import json
import os

STATUS_FILE = "doctor_status.json"


class ReceptionistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Receptionist Dashboard")
        self.root.geometry("300x400")
        self.root.configure(bg="#ffffff")

        self.title_label = tk.Label(
            root, text="Doctor Status", font=("Arial", 16, "bold"), bg="#ffffff"
        )
        self.title_label.pack(pady=10)

        self.status_frame = tk.Frame(root, bg="#ffffff")
        self.status_frame.pack(fill="both", expand=True)

        self.refresh_data()  # Initial load

    def draw_status_circle(self, parent, color):
        canvas = tk.Canvas(
            parent, width=30, height=30, bg="#ffffff", highlightthickness=0
        )
        canvas.create_oval(5, 5, 25, 25, fill=color, outline=color)
        return canvas

    def refresh_data(self):
        # Clear frame
        for widget in self.status_frame.winfo_children():
            widget.destroy()

        # Load data
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {}

        # Display doctors
        for doctor, status in data.items():
            row = tk.Frame(self.status_frame, bg="#ffffff")
            row.pack(fill="x", pady=5, padx=10)

            label = tk.Label(row, text=doctor, font=("Arial", 12), bg="#ffffff")
            label.pack(side="left")

            color = "green" if status == "available" else "red"
            circle = self.draw_status_circle(row, color)
            circle.pack(side="right")

        # Auto refresh every 2 seconds
        self.root.after(2000, self.refresh_data)


# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = ReceptionistApp(root)
    root.mainloop()
