from flask import Blueprint, render_template, jsonify, request
from app.weather import (
    CITIES, fetch_city_weather, get_weather_for_cities, WeatherAPIError, CARD_GRADIENTS
)

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/api/weather")
def api_weather():
    region = request.args.get("region", "all")
    search = request.args.get("search", "").strip().lower()
    unit   = request.args.get("unit", "C")
    units  = "imperial" if unit == "F" else "metric"

    filtered = [
        c for c in CITIES
        if (region == "all" or c["region"] == region)
        and (not search or search in c["name"].lower() or search in c["country"].lower())
    ]

    cities_with_weather = get_weather_for_cities(filtered, units=units)

    for city in cities_with_weather:
        city["display_temp"] = (
            f"{city['temp_f']}°F" if unit == "F" else f"{city['temp_c']}°C"
        )
        city["feels_like"] = (
            f"{city['feels_like_f']}°F" if unit == "F" else f"{city['feels_like_c']}°C"
        )

    return jsonify({"cities": cities_with_weather, "total": len(cities_with_weather)})


@main.route("/api/weather/<city_name>")
def api_city(city_name):
    unit  = request.args.get("unit", "C")
    units = "imperial" if unit == "F" else "metric"

    try:
        weather = fetch_city_weather(city_name, units=units)
        city = next(
            (c for c in CITIES if c["name"].lower() == city_name.lower()),
            {"name": city_name, "country": "", "region": ""}
        )
        weather["display_temp"] = (
            f"{weather['temp_f']}°F" if unit == "F" else f"{weather['temp_c']}°C"
        )
        return jsonify({**city, **weather})
    except WeatherAPIError as exc:
        return jsonify({"error": str(exc)}), 503


@main.route("/health")
def health():
    return jsonify({"status": "ok", "city_count": len(CITIES)})
