import json


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

    event_data = {"title": event_title['data'],
                  "description": event_description['data'],
                  "link": event_link,
                  "image_link": event_image_link,
                  "date": event_date_time[0],
                  "time": event_date_time[1],
                  "ticket Info": event_ticket_info,
                  "ticket_price": event_ticket_price,
                  "performers": event_performers,
                  "works": {"program":event_program['works_author'][0],
                            "work": event_program['works'],
                            "work_author":event_program['works_author'][1:]
                            },
                  "event_venue": event_venue
    }

    data = event_data

    # print(data['date'], data['time'])

    return data
