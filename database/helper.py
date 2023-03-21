from geopy.geocoders import Nominatim
import re


def get_country(url):
    # Extract the location string from the URL
    location = re.search(r"/place/(.*)/", url).group(1)

    # Use Nominatim to get the country from the location string
    geolocator = Nominatim(user_agent="my-application")
    location = geolocator.geocode(location)
    if location is not None:
        country = location.raw['address']['country']
        print(country)
        return country
    else:
        return None


if __name__ == "__main__":
    get_country(
        "https://www.google.ch/maps/place/Kultur-+und+Kongresszentrum+Luzern/@47.050429,8.312062,"
        "17z/data=!3m1!4b1!4m2!3m1!1s0x478ffb986b79cc93:0x3db2a608282feeb8?hl=de")
