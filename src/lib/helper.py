import logging

logger = logging.getLogger(__name__)

def parse_city_region_country(place: str) -> tuple[str, str, str] | None:
    try:
        city, region, country = place.split("/")
        return city, region, country
    except ValueError as e:
        logger.error(
            "cannot parse (%s) 'city', 'region, 'country' with error '%s', please check format, use city/region/country",
            e,
            place,
        )
        return None
    except Exception as e:
        logger.error("unexpected error while parsing place: %s", e)
        return None