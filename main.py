import tkinter as tk
import tkinter.font as tkFont
import ctypes
import os

# load custom font
font_path = os.path.abspath("fonts/Z01-Umoe002 Regular.ttf")

ctypes.windll.gdi32.AddFontResourceW(font_path)

# create app window

root = tk.Tk()

# window settings
root.title("Weather Application")
root.geometry("800x600")
root.configure(bg="#1e293b")

# app title
title = tk.Label(
    root,
    text="ရာသီဥတု အပ်ပလီကေးရှင်း",
    font=("Z01-Umoe002", 24),
    bg="#1e293b",
    fg="white"
)

title.pack(pady=30)

message = tk.Label(
    root,
    text="ကြိုဆိုပါတယ်။ သင့်မြို့ရဲ့ ရာသီဥတုကို တိုက်ရိုက်ရှာဖွေကြည့်ရှုနိုင်ပါတယ်",
    font=("Z01-Umoe002", 14),
    bg="#1e293b",
    fg="white"
)

message.pack(pady=10)

root.mainloop()