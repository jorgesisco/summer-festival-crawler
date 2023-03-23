"""
get_event_data calls find_elements based on the required parameter to allow bs4 to extract the data we need, it then
returns a ditc() with the data in a way we can access it to populate the tables.
"""
def get_event_data(link, crawler):
    event_title = crawler.find_elements(url=link,
                                        tag="header",
                                        inner_tag_1="h1",
                                        multiple_elements=False)

    event_date_time = crawler.find_elements(url=link,
                                            tag="div",
                                            attrs={"class": "cell large-6 subtitle", "id": ""},
                                            date=True,
                                            multiple_elements=False)

    event_ticket_info = crawler.find_elements(url=link,
                                              tag="div",
                                              inner_tag_1="span",
                                              attrs={"class": "cell medium-5 large-4 ticket-status", "id": ""},
                                              ticket=True,
                                              multiple_elements=False)

    event_ticket_price = crawler.find_elements(url=link,
                                               tag="div",
                                               inner_tag_1="div",
                                               attrs={"class": "cell medium-5 large-4 ticket-status", "id": ""},
                                               ticket=True,
                                               multiple_elements=False)

    event_performers = crawler.find_elements(url=link,
                                             tag="div",
                                             inner_tag_1="li",
                                             attrs={"class": "readmore-container text-left", "id": ""},
                                             performers=True,
                                             multiple_elements=False)

    event_program = crawler.find_elements(url=link,
                                          tag="section",
                                          inner_tag_1="strong",
                                          inner_tag_2="em",
                                          attrs={"class": "grid-container program-description", "id": "program"},
                                          multiple_elements=True,
                                          works=True)

    event_description = crawler.find_elements(url=link,
                                              tag="section",
                                              inner_tag_1="p",
                                              attrs={"class": "grid-container", "id": "description"},
                                              multiple_elements=False)

    event_link = link

    event_image_link = crawler.find_elements(url=link,
                                             tag="img",
                                             multiple_elements=False,
                                             image=True)

    event_venue = crawler.find_elements(url=link,
                                        tag="section",
                                        inner_tag_1="p",
                                        inner_tag_2='a',
                                        attrs={"class": "grid-container venue", "id": "venue"},
                                        multiple_elements=True,
                                        venue=True)

    if event_description is None:
        description = "Not Found"
    else:
        description = event_description['data']

    if event_performers is None:
        performers = ["Not Found"]

    else:
        performers = event_performers

    if event_program is None:
        event_ = {"works_author": ["Not Found"],
                  "works": ['Not Found']}

    else:
        event_ = event_program

    event_data = {"title": event_title['data'],
                  "description": description,
                  "link": event_link,
                  "image_link": event_image_link,
                  "date": event_date_time[0],
                  "time": event_date_time[1],
                  "ticket Info": event_ticket_info,
                  "ticket_price": event_ticket_price,
                  "performers": performers,
                  "works": {"program": event_['works_author'][0],
                            "work": event_['works'],
                            "work_author": event_['works_author']
                            },
                  "event_venue": event_venue
                  }

    data = event_data

    return data
