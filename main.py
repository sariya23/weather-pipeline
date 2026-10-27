import argparse
import httpx

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
        'start_date': None,
        'end_date': None,
    }
    response = httpx.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    print(main())