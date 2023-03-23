import json
import re
import urllib
import urllib.parse
from bs4 import BeautifulSoup
import requests

"""
Two helper function to extract urls based by a domain name, When I get the urls by tag, the results is an array, in order to
find each url dynamically this functions are usefully.
"""


def url_by_domain(url_list, domain):
    filtered_urls = []
    for url in url_list:
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.netloc.endswith(domain):
            filtered_urls.append(url)
            return filtered_urls[0]
        else:
            None


def extract_urls(text_list):
    url_pattern = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(],]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    urls = [url for text in text_list for url in url_pattern.findall(text)]
    return urls


class Crawler:
    @staticmethod
    def get_soup(url=str()):
        """
        Takes in a URL and returns the parsed soup object.
        """

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            return soup

        except requests.ConnectionError as e:
            print(e)

    """
    Getting event links        
    """

    @staticmethod
    def get_links(soup, tag_=str(), class_=str()):
        event_links = []

        event_div = soup.find_all(tag_, class_)
        for link in event_div:
            event_links.append("https://www.lucernefestival.ch" + link.a['href'])

        return event_links

    """
    Method to find the info inside each event, each parameter is to allow me to make conditions to run the right find method
    to gather exact what we need.
    """

    def find_elements(self, url, tag,
                      inner_tag_1=None,
                      inner_tag_2=None,
                      attrs=None,
                      multiple_elements=None,
                      works=None,
                      venue=None,
                      performers=None,
                      date=None,
                      ticket=None,
                      image=None):

        unicode_pattern = re.compile(r"[\u00fc\u00e9\u00f1\u00f3\u00e1\u201d\u201c]")

        found_elements = dict()
        # Fetch the content from the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the elements matching the tag and attributes
            elements = soup.find_all(tag, attrs)

            if multiple_elements is not True and image is True:
                image_link = [img for img in elements]

                image_link_complete = f"https://www.lucernefestival.ch{image_link[0]['src']}"
                return image_link_complete

            for element in elements and elements:

                if multiple_elements is True and works is True:
                    found_elements['works_author'] = [unicode_pattern.sub("", t.text) for t in
                                                      element.find_all(inner_tag_1)]
                    found_elements['works'] = [t.text for t in element.find_all(inner_tag_2)]
                    # print(found_elements)

                    if len(found_elements['works']) == 0:
                        found_elements['works'] = ['Not Found']

                    if len(found_elements['works_author']) == 0:
                        found_elements['works_author'] = ['Not Found']

                    return found_elements

                elif multiple_elements is True and venue is True:
                    elements_ = [t.text.strip()
                                 .replace('\xa0', " ")
                                 .replace('\r\n', " ")
                                 for t in element.find_all(inner_tag_1)]

                    urls = [t['href']
                            for t in element.find_all(inner_tag_2)]

                    urls = extract_urls(urls)

                    found_elements['venue'] = elements_[0]
                    found_elements['address'] = elements_[1]
                    found_elements['address_url'] = url_by_domain(urls, 'google.ch')
                    found_elements['more_info'] = elements_[5:]
                    found_elements['arriving_bus_train_url'] = url_by_domain(urls, 'sbb.ch')
                    found_elements['arriving_auto_url'] = url_by_domain(urls, 'www.parking-luzern.ch')
                    found_elements['flights_info_url'] = url_by_domain(urls, 'swiss.com')
                    found_elements['concierge_info_url'] = url_by_domain(urls, '.buchertravel.ch')

                    return found_elements

                elif multiple_elements is not True and performers is True:

                    performer = [re.sub("[\n\t]+", "", t.text) for t in
                                 element.find_all(inner_tag_1)]

                    return performer

                elif multiple_elements is not True and date is True:
                    inner_element = element.text
                    if inner_element:
                        data = re.sub(r"[\n\t]+", "", inner_element)

                        found_elements['data'] = re.findall("\d{2}\.\d{2}", data)

                        return found_elements['data']

                elif multiple_elements is not True and ticket is True:
                    if element.find(inner_tag_1):
                        inner_element = re.sub(r"[\n\t]+", "", element.find(inner_tag_1).text).strip()
                    else:
                        inner_element = None

                    if inner_element:
                        return inner_element

                elif multiple_elements is not True:
                    inner_element = element.find(inner_tag_1)

                    if inner_element:
                        found_elements['data'] = inner_element.text
                        return found_elements


        else:
            return f"Error: Unable to fetch the URL. Status code: {response.status_code}"


"""
The function above returns a dict()
"""
