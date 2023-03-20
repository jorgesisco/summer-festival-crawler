from crawler import Crawler


if __name__ == "__main__":
    crawler = Crawler("https://www.lucernefestival.ch/en/program/summer-festival-23")

    soup = crawler.get_soup()

    links = crawler.get_links(soup, tag_="div", class_="cell shrink show-for-large")

    print(links)