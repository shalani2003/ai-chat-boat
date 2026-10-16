
import tkinter as tk

# ---------------- COLORS ----------------
BG = "#F3F5FB"
WHITE = "#FFFFFF"
PRIMARY = "#6256E8"
DARK = "#24243A"
MUTED = "#85859A"
USER_BUBBLE = "#6256E8"
BOT_BUBBLE = "#FFFFFF"

# ---------------- CHATBOT RULES ----------------
# ---------------- CHATBOT KEYWORD RULES ----------------
rules = [
    {
        "keywords": ["how", "are", "you"],
        "answer": "I am fine. Thank you!"
    },
    {
        "keywords": ["your", "name"],
        "answer": "I am your friendly chatbot."
    },
    {
        "keywords": ["thank", "you"],
        "answer": "You are welcome!"
    },
    {
        "keywords": ["python"],
        "answer": "Python is a popular programming language."
    },
    {
        "keywords": ["bye"],
        "answer": "Goodbye! Have a nice day."
    },
    {
        "keywords": ["hello"],
        "answer": "Hi! Nice to meet you."
    },
    {
        "keywords": ["hi"],
        "answer": "Hello! How can I help you?"
    }
]

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("My Chatbot")
root.geometry("520x650")
root.minsize(400, 500)
root.configure(bg=BG)

# ---------------- HEADER ----------------
header = tk.Frame(root, bg=PRIMARY, height=85)
header.pack(fill="x")
header.pack_propagate(False)

title = tk.Label(
    header,
    text="✦  My Chatbot",
    font=("Segoe UI", 19, "bold"),
    bg=PRIMARY,
    fg=WHITE
)
title.pack(anchor="w", padx=22, pady=(15, 0))

subtitle = tk.Label(
    header,
    text="Your friendly rule-based assistant",
    font=("Segoe UI", 9),
    bg=PRIMARY,
    fg="#E6E3FF"
)
subtitle.pack(anchor="w", padx=25, pady=(2, 8))

# ---------------- CHAT AREA ----------------
chat_container = tk.Frame(root, bg=BG)
chat_container.pack(fill="both", expand=True, padx=12, pady=12)

canvas = tk.Canvas(
    chat_container,
    bg=BG,
    highlightthickness=0
)
scrollbar = tk.Scrollbar(
    chat_container,
    orient="vertical",
    command=canvas.yview
)

messages_frame = tk.Frame(canvas, bg=BG)

window_id = canvas.create_window(
    (0, 0),
    window=messages_frame,
    anchor="nw"
)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


def resize_messages(event):
    canvas.itemconfigure(window_id, width=event.width)


messages_frame.bind("<Configure>", update_scroll_region)
canvas.bind("<Configure>", resize_messages)


# ---------------- DISPLAY MESSAGES ----------------
def add_message(sender, message):
    is_user = sender == "You"

    row = tk.Frame(messages_frame, bg=BG)
    row.pack(fill="x", padx=8, pady=6)

    bubble_color = USER_BUBBLE if is_user else BOT_BUBBLE
    text_color = WHITE if is_user else DARK
    side = "right" if is_user else "left"

    bubble = tk.Frame(
        row,
        bg=bubble_color,
        padx=13,
        pady=9
    )
    bubble.pack(anchor="w" if not is_user else "e")

    name_label = tk.Label(
        bubble,
        text=sender,
        font=("Segoe UI", 9, "bold"),
        bg=bubble_color,
        fg="#E6E3FF" if is_user else PRIMARY
    )
    name_label.pack(anchor="w")

    message_label = tk.Label(
        bubble,
        text=message,
        font=("Segoe UI", 10),
        bg=bubble_color,
        fg=text_color,
        wraplength=300,
        justify="left"
    )
    message_label.pack(anchor="w", pady=(3, 0))

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(1.0)


# ---------------- SEND MESSAGE ----------------
def send_message(event=None):
    user_message = message_entry.get().strip()

    if not user_message:
        return

    add_message("You", user_message)
    message_entry.delete(0, tk.END)

    key = user_message.lower().strip("?!., ")

    if key in responses:
        reply = responses[key]
    else:
        reply = "Sorry, I don't know the answer to that question."

    add_message("Bot", reply)

    message_entry.focus_set()


# ---------------- CLEAR CHAT ----------------
def clear_chat():
    for widget in messages_frame.winfo_children():
        widget.destroy()

    add_message(
        "Bot",
        "Hello! Welcome to my chatbot. Type 'Hi' to get started."
    )


# ---------------- INPUT AREA ----------------
input_frame = tk.Frame(root, bg=WHITE, padx=12, pady=12)
input_frame.pack(fill="x", side="bottom")

message_entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 11),
    bg="#F3F5FB",
    fg=DARK,
    relief="flat",
    insertbackground=DARK
)
message_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=12,
    padx=(0, 8)
)

message_entry.bind("<Return>", send_message)

send_button = tk.Button(
    input_frame,
    text="Send ➤",
    command=send_message,
    font=("Segoe UI", 10, "bold"),
    bg=PRIMARY,
    fg=WHITE,
    activebackground="#5145D0",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=9
)
send_button.pack(side="right")

clear_button = tk.Button(
    root,
    text="Clear conversation",
    command=clear_chat,
    font=("Segoe UI", 9),
    bg=BG,
    fg=MUTED,
    relief="flat",
    cursor="hand2"
)
clear_button.pack(pady=(0, 7))

# ---------------- START APP ----------------
clear_chat()
message_entry.focus_set()

root.mainloop()
