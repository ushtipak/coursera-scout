"""

READ `coursera-categories.txt`

"""

import os
from time import sleep

from selenium import webdriver

CLASS_PAGES = "Box_120drhm-o_O-centerJustify_1nezfbd-o_O-centerAlign_19zvu2s-o_O-displayflex_poyjc"
list_of_categories = "coursera-categories.txt"

if __name__ == "__main__":
    if not os.path.isfile(list_of_categories):
        print("missing input ({})".format(list_of_categories))
        exit(1)

    driver = webdriver.Firefox("/usr/local/bin/")

    with open(list_of_categories, "r") as f:
        categories = f.read().splitlines()

    for category in categories:
        driver.get("https://www.coursera.org/browse/{}?page=2".format(category))
        sleep(7.8)

        pages = []
        for element in driver.find_elements_by_class_name(CLASS_PAGES):
            el = element.text
            if el.isdigit():
                pages.append(int(el))

        page_count = 0
        if len(pages) > 0:
            page_count = max(pages)

        print("{}: {} pages".format(category, page_count))

    driver.close()
