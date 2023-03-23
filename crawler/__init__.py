from crawler.data_extraction import get_event_data
from crawler.crawler import Crawler

crawler = Crawler()

"""
This module initializes the Crawler class, which is used for extracting the data from whe website. 

By initializing Crawler in the __init__.py file, we make it easier to import and use the class 
from other modules within this package. 

Usage:
    from crawler import crawler

    links = crawler.get_links()
"""
