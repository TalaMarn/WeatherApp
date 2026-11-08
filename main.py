
import customtkinter as ctk
from tkinter import messagebox

from weather import get_weather
from database import create_table, save_search, get_history

from config import (
    BACKGROUND,
    CARD_BACKGROUND,
    ACCENT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    FONT_TITLE,
    FONT_TEMPERATURE,
    FONT_HEADING,
    FONT_BODY,
    FONT_SMALL
)

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WeatherApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("ဥတုရာသီ")
        self.geometry("1000x750")
        self.minsize(850, 650)

        self.configure(fg_color=BACKGROUND)

        self.current_weather = None
        self.temperature_unit = "C"

        create_table()

        self.create_header()
        self.create_search()
        self.create_weather_section()
        self.create_details()
        self.create_history()

        self.update_history()

        # Press Enter to search
        self.city_entry.bind(
            "<Return>",
            lambda event: self.search_weather()
        )

    # -------------------------
    # HEADER
    # -------------------------

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(fill="x", padx=40, pady=(30, 20))

        title = ctk.CTkLabel(
            header,
            text="ဥတုရာသီ",
            font=FONT_TITLE,
            text_color=TEXT_PRIMARY
        )
        title.pack(side="left")

        subtitle = ctk.CTkLabel(
            header,
            text="သင့်အတွက် အချိန်နှင့်အညီဥတုသတင်းများ",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(side="right")

    # -------------------------
    # SEARCH BAR
    # -------------------------

    def create_search(self):

        search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        search_frame.pack(fill="x", padx=40, pady=10)

        self.city_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="မြို့အမည်ဖြစ်ရှာပါ...",
            height=50,
            font=FONT_BODY,
            corner_radius=12,
            border_width=1,
            border_color="#334155",
            fg_color=CARD_BACKGROUND
        )

        self.city_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 12)
        )

        self.search_button = ctk.CTkButton(
            search_frame,
            text="ရှာရန်",
            width=120,
            height=50,
            font=FONT_BODY,
            corner_radius=12,
            fg_color=ACCENT,
            hover_color="#4F46E5",
            command=self.search_weather
        )

        self.search_button.pack(side="right")

    # -------------------------
    # MAIN WEATHER DISPLAY
    # -------------------------

    def create_weather_section(self):

        self.weather_frame = ctk.CTkFrame(
            self,
            fg_color=CARD_BACKGROUND,
            corner_radius=24
        )

        self.weather_frame.pack(
            fill="x",
            padx=40,
            pady=20
        )

        # City
        self.city_label = ctk.CTkLabel(
            self.weather_frame,
            text="ဥတုရာသီ အပ်ပလီကေးရှင်းမှ ကြိုဆိုပါသည်",
            font=FONT_HEADING,
            text_color=TEXT_PRIMARY
        )

        self.city_label.pack(pady=(30, 5))

        # Weather icon
        self.icon_label = ctk.CTkLabel(
            self.weather_frame,
            text="🌤️",
            font=("Arial", 55)
        )

        self.icon_label.pack(pady=5)

        # Temperature
        self.temperature_label = ctk.CTkLabel(
            self.weather_frame,
            text="--°C",
            font=FONT_TEMPERATURE,
            text_color=TEXT_PRIMARY
        )

        self.temperature_label.pack(pady=5)

        # Weather description
        self.description_label = ctk.CTkLabel(
            self.weather_frame,
            text="သင့်မြို့အမည်ဖြင့် ရာသီဥတုအခြေအနေကို ရှာပါ",
            font=FONT_BODY,
            text_color=TEXT_SECONDARY
        )

        self.description_label.pack(pady=5)

        # Feels like
        self.feels_label = ctk.CTkLabel(
            self.weather_frame,
            text="Feels like --°C",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY
        )

        self.feels_label.pack(pady=(5, 25))

        # Temperature unit selector
        self.unit_selector = ctk.CTkSegmentedButton(
            self.weather_frame,
            values=["°C", "°F"],
            command=self.change_unit,
            selected_color=ACCENT,
            selected_hover_color="#4F46E5"
        )

        self.unit_selector.set("°C")
        self.unit_selector.pack(pady=(0, 25))

    # -------------------------
    # WEATHER DETAILS
    # -------------------------

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
            ("💧", "စိုထိုင်းစ", "humidity", "%"),
            ("🌬️", "လေတိုက်နှုန်း", "wind_speed", " m/s"),
            ("🌡️", "ဖိအား", "pressure", " hPa")
        ]

        for icon, title, key, unit in details:

            card = ctk.CTkFrame(
                details_frame,
                fg_color=CARD_BACKGROUND,
                corner_radius=16
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

            ctk.CTkLabel(
                card,
                text=icon,
                font=("Arial", 25)
            ).pack(pady=(18, 5))

            ctk.CTkLabel(
                card,
                text=title,
                font=FONT_SMALL,
                text_color=TEXT_SECONDARY
            ).pack(pady=5)

            value = ctk.CTkLabel(
                card,
                text="--",
                font=FONT_HEADING,
                text_color=TEXT_PRIMARY
            )

            value.pack(pady=(5, 20))

            self.detail_labels[key] = (value, unit)

    # -------------------------
    # SEARCH HISTORY
    # -------------------------

    def create_history(self):

        history_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        history_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=15
        )

        ctk.CTkLabel(
            history_frame,
            text="လတ်တလော ရှာဖွေမှုများ",
            font=FONT_HEADING,
            text_color=TEXT_PRIMARY
        ).pack(anchor="w", pady=(5, 10))

        self.history_label = ctk.CTkLabel(
            history_frame,
            text="လတ်တလော ရှာဖွေမှုများ မရှိသေးပါ",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY,
            justify="left"
        )

        self.history_label.pack(anchor="w")

    # -------------------------
    # WEATHER ICON
    # -------------------------

    def get_weather_icon(self, condition):

        icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Smoke": "🌫️",
            "Haze": "🌫️",
            "Dust": "🌫️",
            "Fog": "🌫️",
            "Sand": "🌫️",
            "Ash": "🌋",
            "Squall": "💨",
            "Tornado": "🌪️"
        }

        return icons.get(condition, "🌤️")

    # -------------------------
    # CHANGE TEMPERATURE UNIT
    # -------------------------

    def change_unit(self, value):

        self.temperature_unit = "C" if value == "°C" else "F"

        if self.current_weather:
            self.update_weather_display()

    def convert_temperature(self, temperature):

        if self.temperature_unit == "F":
            return (temperature * 9 / 5) + 32

        return temperature

    # -------------------------
    # UPDATE WEATHER DISPLAY
    # -------------------------

    def update_weather_display(self):

        data = self.current_weather

        temperature = self.convert_temperature(
            data["temperature"]
        )

        feels_like = self.convert_temperature(
            data["feels_like"]
        )

        unit = self.temperature_unit

        self.city_label.configure(
            text=f"{data['city']}, {data['country']}"
        )

        self.icon_label.configure(
            text=self.get_weather_icon(data["main"])
        )

        self.temperature_label.configure(
            text=f"{temperature:.1f}°{unit}"
        )

        self.description_label.configure(
            text=data["description"].title()
        )

        self.feels_label.configure(
            text=f"Feels like {feels_like:.1f}°{unit}"
        )

        self.detail_labels["humidity"][0].configure(
            text=f"{data['humidity']}%"
        )

        self.detail_labels["wind_speed"][0].configure(
            text=f"{data['wind_speed']} m/s"
        )

        self.detail_labels["pressure"][0].configure(
            text=f"{data['pressure']} hPa"
        )

    # -------------------------
    # SEARCH WEATHER
    # -------------------------

    def search_weather(self):

        city = self.city_entry.get().strip()

        if not city:
            messagebox.showwarning(
                "သတိ‌ပေးချက်",
                "ကျေးဇူးပြု၍ မြို့အမည်ကို ထည့်ပါ"
            )
            return

        self.search_button.configure(
            state="disabled",
            text="Loading..."
        )

        self.update_idletasks()

        try:

            data = get_weather(city)

            self.current_weather = data

            self.update_weather_display()

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

        finally:

            self.search_button.configure(
                state="normal",
                text="Search"
            )

    # -------------------------
    # UPDATE HISTORY
    # -------------------------

    def update_history(self):

        records = get_history()

        history_text = "\n".join(
            f"• {record['city']}  |  "
            f"{record['temperature']}°C  |  "
            f"{record['description'].title()}"
            for record in records[:5]
        )

        self.history_label.configure(
            text=history_text or "No recent searches"
        )


if __name__ == "__main__":

    app = WeatherApp()
    app.mainloop()
