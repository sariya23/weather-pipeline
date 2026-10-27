import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='WeatherPipeline',
                        description='Pipeline for downloading weather data')
    args = parser.parse_args()
    print('Hello')