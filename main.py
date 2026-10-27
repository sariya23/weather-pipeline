import argparse
from datetime import date

import httpx
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
                        prog='WeatherPipeline',
                        description='Pipeline for downloading weather data')
    args = parser.parse_args()

    base_url = 'https://archive-api.open-meteo.com/v1/archive'
    params = {
        "latitude": 55.75,
        "longitude": 37.62,
        "hourly": ",".join([
            "temperature_2m",
            "wind_speed_10m",
            "relative_humidity_2m",
            "rain",
        ]),
        'start_date': date(2026, 5, 9).strftime('%Y-%m-%d'),
        'end_date': date(2026, 5, 9).strftime('%Y-%m-%d'),
    }
    response = httpx.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    print(main())