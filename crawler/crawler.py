import json
import re
import urllib
import urllib.parse
from bs4 import BeautifulSoup
import requests


# base_url = "https://www.lucernefestival.ch/en/program/summer-festival-23"

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

    @staticmethod
    def get_links(soup, tag_=str(), class_=str()):
        event_links = []

        event_div = soup.find_all(tag_, class_)
        for link in event_div:
            event_links.append("https://www.lucernefestival.ch" + link.a['href'])

        return event_links

    def find_elements(self, url, tag,
                      inner_tag_1=None,
                      inner_tag_2=None,
                      attrs=None,
                      multiple_elements=None,
                      works=None,
                      venue=None,
                      performers=None,
                      date=None,
                      ticket=None):

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
            text = []
            for element in elements:
                if multiple_elements is True and works is True:
                    found_elements['performer'] = [unicode_pattern.sub("", t.text) for t in
                                                   element.find_all(inner_tag_1)]
                    found_elements['works'] = [t.text for t in element.find_all(inner_tag_2)]
                    # print(found_elements)
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
                    found_elements['Arrival'] = elements_[4]
                    found_elements['arriving_bus_train'] = elements_[5]
                    found_elements['arriving_bus_train_url'] = url_by_domain(urls, 'sbb.ch')
                    found_elements['arriving_auto'] = elements_[6]
                    found_elements['arriving_auto_url'] = url_by_domain(urls, 'www.parking-luzern.ch')
                    found_elements['p_rail'] = elements_[7]
                    found_elements['flights_info'] = elements_[8]
                    found_elements['flights_info_url'] = url_by_domain(urls, 'swiss.com')
                    found_elements['concierge_info'] = elements_[9]
                    found_elements['concierge_info_url'] = url_by_domain(urls, '.buchertravel.ch')
                    found_elements['cloakroom'] = elements_[11]
                    found_elements['wheelchair_sitting'] = [elements_[13], elements_[14]]
                    found_elements['late_admissions'] = elements_[16]
                    found_elements['restaurants_info'] = [elements_[-2], elements_[-2]]
                    found_elements['restaurants_info'] = [urls[-2], urls[-2]]

                    # print(json.dumps(found_elements, sort_keys=False, indent=2))
                    # print(urls)
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

                    inner_element = re.sub(r"[\n\t]+", "", element.find(inner_tag_1).text).strip()

                    if inner_element:
                        return inner_element

                elif multiple_elements is not True:
                    inner_element = element.find(inner_tag_1)
                    if inner_element:
                        found_elements['data'] = inner_element.text


                        return found_elements

                        # Return the list of matching elements


        else:
            return f"Error: Unable to fetch the URL. Status code: {response.status_code}"

    #
    # def get_event_data(self, links=str()):
    #
    #     for link in links:
    #         soup = self.get_soup(link)
