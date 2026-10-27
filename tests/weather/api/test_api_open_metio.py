from datetime import date

from src.config import Config
from src.weather.api.open_meteo import ApiOpenMetio
from src.weather.models.dto.get_weather_request import GetWeatherRequestDTO


class TestApiOpenMetio:
    def test_get_weather_success(self):
        cfg = Config(_env_file='.env.local')
        api = ApiOpenMetio(base_url=cfg.base_url)
        params = GetWeatherRequestDTO(latitude=55.75, longitude=37.62, hourly=['temperature_2m', 'wind_speed_10m', 'relative_humidity_2m', 'rain'],
                                     start_date=date(2025, 5, 9), end_date=date(2025, 5, 9))
        response = api.get_weather(params)

        assert response.status_code == 200
        assert response.json() != {}

        response_data = response.json()
        assert 'utc_offset_seconds' in response_data
        assert 'timezone' in response_data

        assert 'hourly_units' in response_data
        assert 'time' in response_data['hourly_units']
        assert 'temperature_2m' in response_data['hourly_units']
        assert 'wind_speed_10m' in response_data['hourly_units']
        assert 'relative_humidity_2m' in response_data['hourly_units']

        assert 'hourly' in response_data
        assert 'rain' in response_data['hourly']
        assert 'temperature_2m' in response_data['hourly']
        assert 'relative_humidity_2m' in response_data['hourly']
        assert 'wind_speed_10m' in response_data['hourly']