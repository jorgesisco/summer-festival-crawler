from bs4 import BeautifulSoup
import requests


# base_url = "https://www.lucernefestival.ch/en/program/summer-festival-23"

class Crawler:
    def __init__(self, url=str()):
        self.url = url

    def get_soup(self):
        """
        Takes in a URL and returns the parsed soup object.
        """

        try:
            # response = requests.get(self.url)
            # soup = BeautifulSoup(response.content, "html.parser")

            with open("crawler/events.html", "r", encoding='utf-8') as f:
                html_data = f.read()

            soup = BeautifulSoup(html_data, "html.parser")

            return soup

        except requests.ConnectionError as e:
            print(e)

    @staticmethod
    def get_links(soup, tag_, class_):
        event_links = []

        event_div = soup.find_all(tag_, class_)

        for link in event_div:
            event_links.append("https://www.lucernefestival.ch" + link.a['href'])

        return event_links

    # def get_event_data(self):