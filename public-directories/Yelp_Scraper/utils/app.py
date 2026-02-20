import tkinter as tk
import csv
import os
from time import sleep


def pause_for_user():
    root = tk.Tk()
    root.title("Scraper Paused")
    root.resizable(False, False)
    root.configure(bg="#f4f6f8")

    WIDTH, HEIGHT = 520, 220

    # Center window
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w // 2) - (WIDTH // 2)
    y = (screen_h // 2) - (HEIGHT // 2)
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    # Card container
    card = tk.Frame(root, bg="white", padx=30, pady=25, relief="groove", bd=1)
    card.pack(expand=True)

    # Title
    tk.Label(
        card,
        text="⏸ Scraper Paused",
        font=("Segoe UI", 16, "bold"),
        bg="white"
    ).pack(pady=(0, 10))

    # Message
    tk.Label(
        card,
        text=(
            "The scraper is currently paused.\n\n"
            "Please add the search keyword and location,\n"
            "then click the Restart button to start the scraper again."
        ),
        font=("Segoe UI", 10),
        fg="#555",
        bg="white",
        justify="center"
    ).pack(pady=(0, 20))

    # Restart button
    tk.Button(
        card,
        text="Restart Scraper",
        font=("Segoe UI", 10, "bold"),
        width=26,
        bg="#4CAF50",
        fg="white",
        activebackground="#43A047",
        relief="flat",
        command=root.destroy
    ).pack()

    root.mainloop()


def confirm_dialog(title: str, header: str, message: str) -> bool:
    result = {"value": False}

    root = tk.Tk()
    root.title(title)
    root.resizable(False, False)
    root.configure(bg="#f4f6f8")

    WIDTH, HEIGHT = 520, 240

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w // 2) - (WIDTH // 2)
    y = (screen_h // 2) - (HEIGHT // 2)
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    card = tk.Frame(root, bg="white", padx=30, pady=25, relief="groove", bd=1)
    card.pack(expand=True)

    tk.Label(
        card,
        text=header,
        font=("Segoe UI", 16, "bold"),
        bg="white"
    ).pack(pady=(0, 10))

    tk.Label(
        card,
        text=message,
        font=("Segoe UI", 10),
        fg="#555",
        bg="white",
        justify="center"
    ).pack(pady=(0, 20))

    btn_frame = tk.Frame(card, bg="white")
    btn_frame.pack()

    def on_yes():
        result["value"] = True
        root.destroy()

    def on_no():
        root.destroy()

    tk.Button(
        btn_frame,
        text="Continue",
        font=("Segoe UI", 10, "bold"),
        width=14,
        bg="#4CAF50",
        fg="white",
        activebackground="#43A047",
        relief="flat",
        command=on_yes
    ).pack(side="left", padx=8)

    tk.Button(
        btn_frame,
        text="Stop Scraper",
        font=("Segoe UI", 10),
        width=14,
        bg="#E53935",
        fg="white",
        activebackground="#D32F2F",
        relief="flat",
        command=on_no
    ).pack(side="left", padx=8)

    root.mainloop()
    return result["value"]


def type_like_human(element, text, delay=0.1):
    for char in text:
        element.send_keys(char)
        sleep(delay)


def write_dict_to_csv(file_path: str, data: dict):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file_exists = os.path.isfile(file_path)

    headers = []
    rows = []

    if file_exists:
        with open(file_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)

    all_headers = list(dict.fromkeys(headers + list(data.keys())))
    rewrite = all_headers != headers

    mode = "w" if rewrite else "a"

    with open(file_path, mode, encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_headers)

        if rewrite:
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        elif not file_exists:
            writer.writeheader()

        writer.writerow(data)