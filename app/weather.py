import os
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5"

CITIES = [
    # India
    {"name": "Mumbai",      "country": "India",       "region": "india"},
    {"name": "Delhi",       "country": "India",       "region": "india"},
    {"name": "Bangalore",   "country": "India",       "region": "india"},
    {"name": "Chennai",     "country": "India",       "region": "india"},
    {"name": "Kolkata",     "country": "India",       "region": "india"},
    {"name": "Hyderabad",   "country": "India",       "region": "india"},
    {"name": "Pune",        "country": "India",       "region": "india"},
    {"name": "Jaipur",      "country": "India",       "region": "india"},
    {"name": "Ahmedabad",   "country": "India",       "region": "india"},
    {"name": "Surat",       "country": "India",       "region": "india"},
    {"name": "Lucknow",     "country": "India",       "region": "india"},
    {"name": "Kochi",       "country": "India",       "region": "india"},
    {"name": "Coimbatore",  "country": "India",       "region": "india"},
    {"name": "Srinagar",    "country": "India",       "region": "india"},
    {"name": "Nagpur",      "country": "India",       "region": "india"},
    # Asia
    {"name": "Tokyo",       "country": "Japan",       "region": "asia"},
    {"name": "Singapore",   "country": "Singapore",   "region": "asia"},
    {"name": "Dubai",       "country": "UAE",         "region": "asia"},
    {"name": "Bangkok",     "country": "Thailand",    "region": "asia"},
    {"name": "Seoul",       "country": "South Korea", "region": "asia"},
    # Europe
    {"name": "London",      "country": "UK",          "region": "europe"},
    {"name": "Paris",       "country": "France",      "region": "europe"},
    {"name": "Berlin",      "country": "Germany",     "region": "europe"},
    {"name": "Rome",        "country": "Italy",       "region": "europe"},
    {"name": "Madrid",      "country": "Spain",       "region": "europe"},
    # Americas
    {"name": "New York",    "country": "USA",         "region": "americas"},
    {"name": "Los Angeles", "country": "USA",         "region": "americas"},
    {"name": "Toronto",     "country": "Canada",      "region": "americas"},
    {"name": "Sao Paulo",   "country": "Brazil",      "region": "americas"},
    {"name": "Mexico City", "country": "Mexico",      "region": "americas"},
    # Africa & Oceania
    {"name": "Cairo",       "country": "Egypt",       "region": "africa"},
    {"name": "Lagos",       "country": "Nigeria",     "region": "africa"},
    {"name": "Sydney",      "country": "Australia",   "region": "oceania"},
    {"name": "Melbourne",   "country": "Australia",   "region": "oceania"},
]

WEATHER_ICON_MAP = {
    "clear sky":           "☀️",
    "few clouds":          "🌤️",
    "scattered clouds":    "⛅",
    "broken clouds":       "☁️",
    "overcast clouds":     "☁️",
    "light rain":          "🌦️",
    "moderate rain":       "🌧️",
    "heavy intensity rain":"🌧️",
    "thunderstorm":        "⛈️",
    "snow":                "❄️",
    "mist":                "🌫️",
    "fog":                 "🌫️",
    "haze":                "🌁",
    "drizzle":             "🌂",
    "shower rain":         "🌧️",
}

SKY_BACKGROUNDS = {
    "clear":        ["#1a6bcc", "#3a9fea", "#fde68a"],
    "clouds":       ["#4a5568", "#718096", "#a0aec0"],
    "rain":         ["#1a2a3a", "#2c4a6a", "#3d6b94"],
    "drizzle":      ["#2a3f5f", "#3d6b94", "#5a8ab0"],
    "thunderstorm": ["#0f1923", "#1e3547", "#2d5068"],
    "snow":         ["#1e2a4a", "#3d5a8c", "#6688c0"],
    "mist":         ["#3a3f50", "#5a6070", "#8090a0"],
    "fog":          ["#3a3f50", "#5a6070", "#8090a0"],
    "haze":         ["#4a4a3a", "#7a7a5a", "#aaa870"],
    "default":      ["#1a2a50", "#2d4a8a", "#3a5fa0"],
}

CARD_GRADIENTS = [
    "linear-gradient(135deg,rgba(29,78,216,.7),rgba(37,99,235,.4))",
    "linear-gradient(135deg,rgba(5,150,105,.7),rgba(4,120,87,.4))",
    "linear-gradient(135deg,rgba(124,58,237,.7),rgba(109,40,217,.4))",
    "linear-gradient(135deg,rgba(220,38,38,.6),rgba(185,28,28,.4))",
    "linear-gradient(135deg,rgba(217,119,6,.7),rgba(180,83,9,.4))",
    "linear-gradient(135deg,rgba(2,132,199,.7),rgba(3,105,161,.4))",
]


class WeatherAPIError(Exception):
    pass


def get_api_key():
    key = os.environ.get("OPENWEATHER_API_KEY", "")
    if not key:
        raise WeatherAPIError("OPENWEATHER_API_KEY environment variable is not set.")
    return key


def fetch_city_weather(city_name: str, units: str = "metric") -> dict:
    """Fetch current weather for a single city from OpenWeatherMap."""
    api_key = get_api_key()
    params = {"q": city_name, "appid": api_key, "units": units}

    try:
        response = requests.get(f"{BASE_URL}/weather", params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        raise WeatherAPIError(f"API error for {city_name}: {exc}") from exc
    except requests.exceptions.RequestException as exc:
        raise WeatherAPIError(f"Network error for {city_name}: {exc}") from exc

    data = response.json()
    return parse_city_weather(data)


def parse_city_weather(data: dict) -> dict:
    """Parse raw OpenWeatherMap response into our app format."""
    condition = data["weather"][0]["main"].lower()
    description = data["weather"][0]["description"].lower()
    temp_c = round(data["main"]["temp"])
    temp_f = round(temp_c * 9 / 5 + 32)

    icon = WEATHER_ICON_MAP.get(description, "🌡️")
    bg = SKY_BACKGROUNDS.get(condition, SKY_BACKGROUNDS["default"])

    return {
        "temp_c":      temp_c,
        "temp_f":      temp_f,
        "humidity":    data["main"]["humidity"],
        "wind":        round(data["wind"]["speed"] * 3.6),  # m/s → km/h
        "feels_like_c": round(data["main"]["feels_like"]),
        "feels_like_f": round(data["main"]["feels_like"] * 9 / 5 + 32),
        "desc":        data["weather"][0]["description"].title(),
        "icon":        icon,
        "bg":          bg,
        "condition":   condition,
        "visibility":  data.get("visibility", 0) // 1000,  # m → km
        "pressure":    data["main"]["pressure"],
    }


def get_weather_for_cities(cities: list, units: str = "metric") -> list:
    """Fetch weather for a list of city dicts. Skips cities on API error."""
    results = []
    for idx, city in enumerate(cities):
        try:
            weather = fetch_city_weather(city["name"], units)
            results.append({
                **city,
                **weather,
                "gradient": CARD_GRADIENTS[idx % len(CARD_GRADIENTS)],
            })
        except WeatherAPIError:
            pass  # skip unavailable cities gracefully
    return results
