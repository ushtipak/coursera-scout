from selenium import webdriver
from time import sleep
import logging
import mappings

driver = webdriver.Firefox("/usr/local/bin/")

categories = [
    "arts-and-humanities/history",
    "arts-and-humanities/music-and-art",
    "arts-and-humanities/philosophy"
]


def get_number_of_pages(category):
    """Return number of pages with course results from given category."""
    url = "https://www.coursera.org/browse/{}?page=2".format(category)
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)

    for category in categories:
        print("{}: {} pages".format(category, get_number_of_pages(category)))

    driver.close()
