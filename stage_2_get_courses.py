"""
Create CSVs with title, university, type and tier for all courses from all retrieved categories
"""

import csv
import logging
import os
from time import sleep

from selenium import webdriver

CLASS_PAGES = "Box_120drhm-o_O-centerJustify_1nezfbd-o_O-centerAlign_19zvu2s-o_O-displayflex_poyjc"
CLASS_TITLE = "card-title"
CLASS_UNIVERSITY = "partner-name"
CLASS_DETAILS = "browse-result-card"

driver = webdriver.Firefox("/usr/local/bin/")


def get_number_of_pages(_category):
    """Return total number of pages for given category."""
    logging.info("calling get_number_of_pages for \"{}\"".format(_category))
    url = "https://www.coursera.org/browse/{}?page=2".format(_category)
    logging.info("url: {}".format(url))
    driver.get(url)
    sleep(7.8)

    nums = []
    for element in driver.find_elements_by_class_name(CLASS_PAGES):
        num = element.text
        if num.isdigit():
            nums.append(int(num))
    max_num = 0
    if len(nums) > 0:
        max_num = max(nums)

    logging.info("return from get_number_of_pages: {}".format(max_num))
    return max_num


def get_details_from_page(_category, _page):
    """Return all info on courses from given page."""
    logging.info("calling get_details_from_page for \"{}\", page: {}".format(_category, _page))
    url = "https://www.coursera.org/browse/{}?page={}".format(_category, _page)
    logging.info("url: {}".format(url))
    driver.get(url)
    sleep(6.1)

    titles = []
    for element in driver.find_elements_by_class_name(CLASS_TITLE):
        titles.append(element.text)

    universities = []
    for element in driver.find_elements_by_class_name(CLASS_UNIVERSITY):
        universities.append(element.text)
    universities = universities[2:]

    links = []
    form = []
    for element in driver.find_elements_by_class_name(CLASS_DETAILS):
        links.append(element.get_attribute("href"))
        details = element.text
        if "COURSE" in details:
            form.append("course")
        elif "SPECIALIZATION" in details:
            form.append("specialization")
        else:
            form.append("not specified")

    _courses = []
    for i in range(len(titles)):
        _courses.append(
            {
                "title": titles[i],
                "university": universities[i],
                "form": form[i],
                "link": links[i],
                "category": _category
            }
        )

    logging.info("return from get_details_from_page: {}".format(_courses))
    return _courses


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # load category list if exits
    category_list = "results/all-categories"
    if not os.path.isfile(category_list):
        logging.error("category_list \"{}\" not found!".format(category_list))
        exit(1)
    with open(category_list, "r") as f:
        categories = f.read().splitlines()

    # prepare output dir and header for csv files
    field_names = ["title", "university", "form", "link", "category"]
    if not os.path.exists("results/courses"):
        os.makedirs("results/courses")

    # process each category in list:
    # - get total number of pages
    # - get details on courses for each page up to the last one
    # - save retrieved list of course dicts under category file name in outputs dir
    for category in categories:
        pages = get_number_of_pages(category)
        courses = []
        for page in range(2, pages + 1):
            for course in get_details_from_page(category, page):
                courses.append(course)

        try:
            with open("results/courses/{}.csv".format(category.replace("/", "---")), 'w') as f:
                writer = csv.DictWriter(f, fieldnames=field_names)
                writer.writeheader()
                for course in courses:
                    writer.writerow(course)
        except IOError as e:
            logging.error("IOError [{}]".format(e))
            exit(2)

    driver.close()
