import logging
from time import sleep

from selenium import webdriver

import mappings

driver = webdriver.Firefox("/usr/local/bin/")


def get_number_of_pages(cat):
    """Return number of pages with course results from given category."""
    url = "https://www.coursera.org/browse/{}?page=2".format(cat)
    logging.debug("url: {}".format(url))
    driver.get(url)
    sleep(7.8)

    nums = []
    for element in driver.find_elements_by_class_name(mappings.CLASS_PAGES):
        num = element.text
        if num.isdigit():
            nums.append(int(num))

    max_num = 0
    if len(nums) > 0:
        max_num = max(nums)
    return max_num


def get_details_from_page(_category, page):
    driver.get("https://www.coursera.org/browse/{}?page={}".format(_category, page))
    sleep(5.1)

    titles = []
    for element in driver.find_elements_by_class_name(mappings.CLASS_TITLE):
        titles.append(element.text)

    universities = []
    for element in driver.find_elements_by_class_name(mappings.CLASS_UNIVERSITY):
        universities.append(element.text)
    universities = universities[2:]

    links = []
    print("*" * 10)
    for element in driver.find_elements_by_class_name(mappings.CLASS_LINKS):
        links.append(element.get_attribute("href"))
        print(element.text)
    print("*" * 10)

    _courses = []
    for i in range(10):
        _courses.append({"title": titles[i], "university": universities[i], "link": links[i], "category": _category})

    return _courses


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    with open("coursera-categories.txt", "r") as f:
        categories = f.read().splitlines()

    courses = []
    for category in categories:
        # print("{}: {} pages".format(category, get_number_of_pages(category)))
        courses.append(get_details_from_page("physical-science-and-engineering/electrical-engineering", 2))

    print(courses)

    driver.close()


