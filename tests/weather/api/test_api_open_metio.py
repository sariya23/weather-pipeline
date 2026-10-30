from datetime import date, datetime

import httpx

from src.config import Config
from src.weather.api.open_meteo import ApiOpenMetio
from src.weather.models.domain.weather import Weather, WeatherList
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

    def test_response_to_domain(self):
        api = ApiOpenMetio(base_url='https://example.com')
        response = httpx.Response(200, json={
            'latitude': 55.75,
            'longitude': 37.62,
            'hourly': {
                'time': ['2025-05-09T00:00', '2025-05-09T01:00', '2025-05-09T02:00'],
                'temperature_2m': [-2.5, 0.0, 3.7],
                'wind_speed_10m': [4.1, 5.2, 6.3],
                'relative_humidity_2m': [80.0, 75.0, 70.0],
            },
        })

        result = api.response_to_domain(response)

        assert isinstance(result, WeatherList)
        assert len(result) == 3
        expected = [
            (datetime(2025, 5, 9, 0), -2.5, 4.1, 80.0),
            (datetime(2025, 5, 9, 1), 0.0, 5.2, 75.0),
            (datetime(2025, 5, 9, 2), 3.7, 6.3, 70.0),
        ]
        for weather, (timestamp, temperature, wind_speed, humidity) in zip(result, expected, strict=True):
            assert isinstance(weather, Weather)
            assert weather.timestamp == timestamp
            assert weather.temperature_cel_2m == temperature
            assert weather.wind_speed_10m == wind_speed
            assert weather.relative_humidity_2m == humidity
            assert weather.location.latitude == 55.75
            assert weather.location.longitude == 37.62
