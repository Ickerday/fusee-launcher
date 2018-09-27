import os
import tkinter as tk
from tkinter import ttk, messagebox

PAYLOAD_DIR: str = "payloads"


class MainApp(tk.Frame):

    def __init__(self, parent: tk.Tk, payload_list):
        self.payloads: list = payload_list
        self.current_payload: str = self.payloads[0]

        tk.Frame.__init__(self, parent)
        self.configure_parent(parent)
        self.init_window(parent)
        self.parent: tk.Tk = parent

    def configure_parent(self, parent: tk.Tk):
        parent.title("NX RCM Payload Launcher")
        geometry_config: str = self.calculate_geometry(parent.winfo_screenheight(),
                                                       parent.winfo_screenwidth())
        parent.geometry(geometry_config)
        parent.grid()
        parent.configure(background="gray91")
        parent.attributes('-topmost', True)

    @staticmethod
    def get_payloads_or_empty(payload_dir) -> list:
        found_payloads: list = []

        for entry in os.listdir(payload_dir):
            if not entry.startswith(".") and entry.endswith(".bin"):
                print(entry)
                found_payloads.append(entry)
        return found_payloads

    def set_payload(self, event: tk.Event) -> None:
        self.current_payload = self.payloads[event.widget.current()]

    def run_payload(self) -> None:
        if self.current_payload:
            print(f"Launching {self.current_payload}!")
            os.system(f'python3 fusee-launcher.py payloads/{str(self.current_payload)}')
        else:
            messagebox.showerror("Error", "No payload selected!")

    def init_window(self, master: tk.Tk) -> None:
        var = tk.StringVar(value="Payloads:")
        label = tk.Label(master, textvariable=var)
        label.pack(expand=True, anchor=tk.N)

        payload_combo = ttk.Combobox(master, values=self.payloads, state='readonly')
        payload_combo.current(0)
        payload_combo.pack(expand=True, anchor=tk.CENTER)
        payload_combo.bind("<<ComboboxSelected>>", self.set_payload)

        run_button = tk.Button(master, text="Run", command=self.run_payload)
        run_button.pack(expand=True, anchor=tk.S)

    @staticmethod
    def calculate_geometry(screen_height: int, screen_width: int, window_height: int = 100, window_width: int = 250):
        pos_x = int((screen_width / 2) - (window_width / 2))
        pos_y = int((screen_height / 2) - (window_height / 2))
        return f"{window_width}x{window_height}+{pos_x}+{pos_y}"


if __name__ == '__main__':
    payloads = []
    if os.path.isdir(PAYLOAD_DIR):
        payloads = MainApp.get_payloads_or_empty(PAYLOAD_DIR)

    if len(payloads) < 1:
        messagebox.showerror("Error", "The payloads/ folder is either empty or non-existent! " +
                             "Please see the README.md for instructions.")
        os.sys.exit(1)

    root = tk.Tk()
    MainApp(root, payloads).pack(side="top", fill="both", expand=True)
    root.mainloop()
