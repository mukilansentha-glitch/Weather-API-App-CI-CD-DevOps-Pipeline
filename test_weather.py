import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from app import create_app
from app.weather import (
    parse_city_weather, get_weather_for_cities, WeatherAPIError,
    fetch_city_weather, get_api_key, CITIES, CARD_GRADIENTS,
)

MOCK_OWM_RESPONSE = {
    "weather": [{"main": "Clear", "description": "clear sky"}],
    "main": {
        "temp": 32.0,
        "feels_like": 35.0,
        "humidity": 65,
        "pressure": 1012,
    },
    "wind": {"speed": 4.5},
    "visibility": 10000,
}

MOCK_RAIN_RESPONSE = {
    "weather": [{"main": "Rain", "description": "heavy intensity rain"}],
    "main": {"temp": 22.0, "feels_like": 21.0, "humidity": 85, "pressure": 1005},
    "wind": {"speed": 8.0},
    "visibility": 5000,
}

MOCK_SNOW_RESPONSE = {
    "weather": [{"main": "Snow", "description": "snow"}],
    "main": {"temp": -3.0, "feels_like": -6.0, "humidity": 90, "pressure": 998},
    "wind": {"speed": 5.0},
    "visibility": 2000,
}


@pytest.fixture
def app():
    return create_app({"TESTING": True})


@pytest.fixture
def client(app):
    return app.test_client()


# ── parse_city_weather ────────────────────────────────────────────────────────

class TestParseCityWeather:

    def test_returns_required_keys(self):
        result = parse_city_weather(MOCK_OWM_RESPONSE)
        for k in ("temp_c","temp_f","humidity","wind","feels_like_c","feels_like_f","desc","icon","bg","condition","visibility","pressure"):
            assert k in result

    def test_temp_c_rounded(self):
        result = parse_city_weather(MOCK_OWM_RESPONSE)
        assert result["temp_c"] == 32

    def test_temp_f_conversion(self):
        result = parse_city_weather(MOCK_OWM_RESPONSE)
        assert result["temp_f"] == round(32 * 9/5 + 32)

    def test_wind_converted_to_kmh(self):
        result = parse_city_weather(MOCK_OWM_RESPONSE)
        assert result["wind"] == round(4.5 * 3.6)

    def test_visibility_converted_to_km(self):
        result = parse_city_weather(MOCK_OWM_RESPONSE)
        assert result["visibility"] == 10

    def test_clear_sky_icon(self):
        result = parse_city_weather(MOCK_OWM_RESPONSE)
        assert result["icon"] == "☀️"

    def test_rain_icon(self):
        result = parse_city_weather(MOCK_RAIN_RESPONSE)
        assert result["icon"] == "🌧️"

    def test_snow_icon(self):
        result = parse_city_weather(MOCK_SNOW_RESPONSE)
        assert result["icon"] == "❄️"

    def test_bg_is_list_of_three(self):
        result = parse_city_weather(MOCK_OWM_RESPONSE)
        assert isinstance(result["bg"], list) and len(result["bg"]) == 3

    def test_unknown_description_uses_default_icon(self):
        data = {**MOCK_OWM_RESPONSE, "weather": [{"main": "Smoke", "description": "volcanic ash"}]}
        result = parse_city_weather(data)
        assert result["icon"] == "🌡️"

    def test_negative_temp(self):
        result = parse_city_weather(MOCK_SNOW_RESPONSE)
        assert result["temp_c"] == -3

    def test_humidity_value(self):
        result = parse_city_weather(MOCK_OWM_RESPONSE)
        assert result["humidity"] == 65

    def test_pressure_value(self):
        result = parse_city_weather(MOCK_OWM_RESPONSE)
        assert result["pressure"] == 1012


# ── fetch_city_weather ────────────────────────────────────────────────────────

class TestFetchCityWeather:

    @patch("app.weather.requests.get")
    @patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test-key"})
    def test_successful_fetch(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = MOCK_OWM_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_city_weather("Chennai")
        assert result["temp_c"] == 32
        mock_get.assert_called_once()

    @patch("app.weather.requests.get")
    @patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test-key"})
    def test_http_error_raises_api_error(self, mock_get):
        import requests as req
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = req.exceptions.HTTPError("404")
        mock_get.return_value = mock_response

        with pytest.raises(WeatherAPIError):
            fetch_city_weather("UnknownCity")

    @patch("app.weather.requests.get")
    @patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test-key"})
    def test_network_error_raises_api_error(self, mock_get):
        import requests as req
        mock_get.side_effect = req.exceptions.ConnectionError("timeout")

        with pytest.raises(WeatherAPIError):
            fetch_city_weather("Chennai")

    def test_missing_api_key_raises_error(self):
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("OPENWEATHER_API_KEY", None)
            with pytest.raises(WeatherAPIError, match="OPENWEATHER_API_KEY"):
                get_api_key()


# ── get_weather_for_cities ────────────────────────────────────────────────────

class TestGetWeatherForCities:

    @patch("app.weather.fetch_city_weather")
    def test_returns_all_on_success(self, mock_fetch):
        mock_fetch.return_value = parse_city_weather(MOCK_OWM_RESPONSE)
        cities = [{"name": "Chennai", "country": "India", "region": "india"},
                  {"name": "Mumbai",  "country": "India", "region": "india"}]
        result = get_weather_for_cities(cities)
        assert len(result) == 2

    @patch("app.weather.fetch_city_weather")
    def test_skips_failed_cities(self, mock_fetch):
        mock_fetch.side_effect = [
            parse_city_weather(MOCK_OWM_RESPONSE),
            WeatherAPIError("API error"),
        ]
        cities = [{"name": "Chennai", "country": "India", "region": "india"},
                  {"name": "BadCity",  "country": "X",     "region": "india"}]
        result = get_weather_for_cities(cities)
        assert len(result) == 1
        assert result[0]["name"] == "Chennai"

    @patch("app.weather.fetch_city_weather")
    def test_gradient_added(self, mock_fetch):
        mock_fetch.return_value = parse_city_weather(MOCK_OWM_RESPONSE)
        cities = [{"name": "Chennai", "country": "India", "region": "india"}]
        result = get_weather_for_cities(cities)
        assert "gradient" in result[0]

    @patch("app.weather.fetch_city_weather")
    def test_gradient_cycles(self, mock_fetch):
        mock_fetch.return_value = parse_city_weather(MOCK_OWM_RESPONSE)
        cities = [{"name": f"City{i}", "country": "X", "region": "asia"} for i in range(len(CARD_GRADIENTS) + 2)]
        result = get_weather_for_cities(cities)
        assert result[0]["gradient"] == result[len(CARD_GRADIENTS)]["gradient"]


# ── API endpoints ─────────────────────────────────────────────────────────────

class TestHealthEndpoint:

    def test_returns_200(self, client):
        assert client.get("/health").status_code == 200

    def test_status_ok(self, client):
        data = client.get("/health").get_json()
        assert data["status"] == "ok"

    def test_city_count(self, client):
        data = client.get("/health").get_json()
        assert data["city_count"] == len(CITIES)


class TestIndexRoute:

    def test_returns_200(self, client):
        assert client.get("/").status_code == 200

    def test_returns_html(self, client):
        response = client.get("/")
        assert b"<html" in response.data or b"<!DOCTYPE" in response.data


class TestWeatherEndpoint:

    @patch("app.routes.get_weather_for_cities")
    def test_returns_200(self, mock_gw, client):
        mock_gw.return_value = []
        assert client.get("/api/weather").status_code == 200

    @patch("app.routes.get_weather_for_cities")
    def test_response_structure(self, mock_gw, client):
        mock_gw.return_value = []
        data = client.get("/api/weather").get_json()
        assert "cities" in data
        assert "total" in data

    @patch("app.routes.get_weather_for_cities")
    def test_total_matches_cities(self, mock_gw, client):
        mock_city = {**parse_city_weather(MOCK_OWM_RESPONSE), "name": "Chennai", "country": "India",
                     "region": "india", "gradient": "linear-gradient(135deg,red,blue)"}
        mock_gw.return_value = [mock_city]
        data = client.get("/api/weather").get_json()
        assert data["total"] == len(data["cities"])

    @patch("app.routes.get_weather_for_cities")
    def test_celsius_display(self, mock_gw, client):
        mock_city = {**parse_city_weather(MOCK_OWM_RESPONSE), "name": "Chennai", "country": "India",
                     "region": "india", "gradient": "x"}
        mock_gw.return_value = [mock_city]
        data = client.get("/api/weather?unit=C").get_json()
        assert "°C" in data["cities"][0]["display_temp"]

    @patch("app.routes.get_weather_for_cities")
    def test_fahrenheit_display(self, mock_gw, client):
        mock_city = {**parse_city_weather(MOCK_OWM_RESPONSE), "name": "Chennai", "country": "India",
                     "region": "india", "gradient": "x"}
        mock_gw.return_value = [mock_city]
        data = client.get("/api/weather?unit=F").get_json()
        assert "°F" in data["cities"][0]["display_temp"]


class TestCityEndpoint:

    @patch("app.routes.fetch_city_weather")
    def test_known_city_200(self, mock_fetch, client):
        mock_fetch.return_value = parse_city_weather(MOCK_OWM_RESPONSE)
        assert client.get("/api/weather/Chennai").status_code == 200

    @patch("app.routes.fetch_city_weather")
    def test_city_data_has_name(self, mock_fetch, client):
        mock_fetch.return_value = parse_city_weather(MOCK_OWM_RESPONSE)
        data = client.get("/api/weather/Chennai").get_json()
        assert data["name"] == "Chennai"

    @patch("app.routes.fetch_city_weather")
    def test_api_error_returns_503(self, mock_fetch, client):
        mock_fetch.side_effect = WeatherAPIError("API down")
        assert client.get("/api/weather/BadCity").status_code == 503
