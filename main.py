import customtkinter as ctk
from tkinter import messagebox
import tkinter.font as tkFont
import ctypes
import os

from weather import get_weather
from database import create_table, save_search, get_history

# load custom font
font_path = os.path.abspath("fonts/Z01-Umoe002 Regular.ttf")

ctypes.windll.gdi32.AddFontResourceW(font_path)

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WeatherApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("ဥတုရာသီ")
        self.geometry("1000x700")
        self.minsize(800, 600)

        self.configure(fg_color="#101827")

        # Initialize database
        create_table()

        self.create_header()
        self.create_search()
        self.create_weather_section()
        self.create_details()
        self.create_history()

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(fill="x", padx=35, pady=25)

        title = ctk.CTkLabel(
            header,
            text="ဥတုရာသီ",
            font=("Z01-Umoe002", 30),
            text_color="#FFFFFF"
        )
        title.pack(side="left")

        subtitle = ctk.CTkLabel(
            header,
            text="ရာသီဥတုပြ ဇယား",
            font=("Z01-Umoe002", 11),
            text_color="#94A3B8"
        )
        subtitle.pack(side="right")

    def create_search(self):

        search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        search_frame.pack(fill="x", padx=35, pady=10)

        self.city_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="မြို့အမည်ရိုက်ထည့်ပါ...",
            height=45,
            font=("Z01-Umoe002", 14),
            corner_radius=10
        )
        self.city_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0,10)
        )
        search_buttom = ctk.CTkButton(
            search_frame,
            text="ရှာဖွေမည်",
            font=("Z01-Umoe002", 14, "bold"),
            width=120,
            height=45,
            command=self.search_weather
        )
        search_buttom.pack(side="right")

    def create_weather_section(self):
        self.weather_frame = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            corner_radius=20
        )
        self.weather_frame.pack(
            fill="x",
            padx=35,
            pady=20
        )

        self.city_label = ctk.CTkLabel(
            self.weather_frame,
            text="မြို့အမည်",
            font=("Z01-Umoe002", 22, "bold")
        )
        self.city_label.pack(pady=(30, 5))

        self.temperature_label = ctk.CTkLabel(
            self.weather_frame,
            text="--°C",
            font=("Z01-Umoe002", 65, "bold")
        )
        self.temperature_label.pack(pady=5)

        self.description_label = ctk.CTkLabel(
            self.weather_frame,
            text="Your weather information will appear here",
            font=("Z01-Umoe002", 14),
            text_color="#94A3B8"
        )
        self.description_label.pack(pady=(5, 30))

    def create_details(self):

        details_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        details_frame.pack(
            fill="x",
            padx=35,
            pady=10
        )

        self.detail_labels = {}

        details = [
            ("စိုထိုင်းစ", "humidity"),
            ("လေတိုက်နှုန်း", "wind_speed"),
            ("ဖိအား", "pressure")
        ]

        for title, key in details:

            card = ctk.CTkFrame(
                details_frame,
                fg_color="#1E293B",
                corner_radius=15
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=("Z01-Umoe002", 13),
                text_color="#94A3B8"
            ).pack(pady=(20, 5))

            value = ctk.CTkLabel(
                card,
                text="--",
                font=("Z01-Umoe002", 20, "bold")
            )
            value.pack(pady=(5, 20))

            self.detail_labels[key] = value

    def create_history(self):

        history_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        history_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=20
        )

        ctk.CTkLabel(
            history_frame,
            text="လတ်တလော ရှာဖွေထားသည့်မြို့များ",
            font=("Z01-Umoe002", 18, "bold")
        ).pack(anchor="w", pady=10)

        self.history_label = ctk.CTkLabel(
            history_frame,
            text="လတ်တလော ရှာဖွေထားခြင်းမရှိပါ။",
            font=("Z01-Umoe002", 13),
            text_color="#94A3B8"
        )
        self.history_label.pack(anchor="w")

    def search_weather(self):

        city = self.city_entry.get().strip()

        if not city:
            messagebox.showwarning(
                "Warning",
                "မြို့အမည် ရိုက်ထည့်ပါ။"
            )
            return

        try:

            data = get_weather(city)

            self.city_label.configure(
                text=f"{data['city']}, {data['country']}"
            )

            self.temperature_label.configure(
                text=f"{data['temperature']:.1f}°C"
            )

            self.description_label.configure(
                text=data["description"].title()
            )

            self.detail_labels["humidity"].configure(
                text=f"{data['humidity']}%"
            )

            self.detail_labels["wind_speed"].configure(
                text=f"{data['wind_speed']} m/s"
            )

            self.detail_labels["pressure"].configure(
                text=f"{data['pressure']} hPa"
            )

            save_search(
                data["city"],
                data["temperature"],
                data["description"]
            )

            self.update_history()

        except Exception as error:

            messagebox.showerror(
                "Weather Error",
                str(error)
            )

    def update_history(self):

        records = get_history()

        history_text = "\n".join(
            f"{record['city']} - "
            f"{record['temperature']}°C - "
            f"{record['description']}"
            for record in records[:5]
        )

        self.history_label.configure(
            text=history_text or "No recent searches"
        )


if __name__ == "__main__":

    app = WeatherApp()
    app.mainloop()
