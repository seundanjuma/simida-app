import tkinter as tk

class DoctorStatusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Doctor Status")
        self.root.geometry("80x80")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        self.status = "free"

        self.frame = tk.Frame(root, bg="green")
        self.frame.pack(expand=True, fill="both")

        self.frame.bind("<ButtonPress-1>", self.start_move)
        self.frame.bind("<B1-Motion>", self.do_move)
        self.frame.bind("<ButtonRelease-1>", self.toggle_status)
        self.frame.bind("<Double-Button-1>", lambda e: root.destroy())

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f"+{x}+{y}")

    def toggle_status(self, event=None):
        if self.status == "free":
            self.status = "busy"
            self.frame.config(bg="red")
        else:
            self.status = "free"
            self.frame.config(bg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = DoctorStatusApp(root)
    root.mainloop()
