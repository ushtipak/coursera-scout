import csv
import logging
import os
import sqlite3
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import *

driver = webdriver.Firefox("/usr/local/bin/")

email = "lhbpujoqyhwzwxtaxp@ttirv.com"
password = "https://www.selenium.dev/downloads/"


def init_db():
    _conn = sqlite3.connect('results/offerings.db')
    _conn.execute('''CREATE TABLE IF NOT EXISTS offerings
                     (link TEXT PRIMARY KEY, title TEXT, university TEXT, category TEXT, fare INTEGER)''')
    _conn.commit()
    return _conn


def login(_email, _password):
    """Sign in with provided credentials."""
    logging.info("calling login with email \"{}\"".format(_email))
    driver.get("https://www.coursera.org")
    sleep(6.3)

    driver.find_elements_by_link_text("Log In")[0].click()
    sleep(3.2)

    driver.find_elements_by_name("email")[0].send_keys(_email)
    sleep(4.1)

    driver.find_elements_by_name("password")[0].send_keys(_password)
    # class "_1hx9z6hg" covers three, we're using last:
    # - continue with facebook
    # - continue with apple
    # - log in
    sleep(7.2)

    driver.find_elements_by_class_name("_1hx9z6hg")[2].click()
    sleep(6.4)


def get_course_offering(_course):
    """...."""
    link = _course['link']
    logging.info("calling get_course_offering with url \"{}\"".format(link))

    scanned = conn.execute('SELECT * FROM offerings WHERE link=?', (link,)).fetchone()
    if scanned is None:
        # course wasn't checked before, load it up
        driver.get(link)
        sleep(4.7)

        logging.info("click on enroll ...")
        try:
            driver.find_elements_by_class_name("EnrollButton")[0].click()
            sleep(2.2)

            logging.info("check if course is part of multiple specializations ...")
            is_unique = True
            try:
                choose_specialization = driver.find_element_by_id("course_enroll_s12n_selection_button_button")
                is_unique = False
                choose_specialization.click()
            except NoSuchElementException:
                logging.info("course is unique!")
            if not is_unique:
                logging.info("course IS part of multiple specializations, one selected to proceed ...")
            sleep(1.1)

            logging.info("check if course is completely free ...")
            is_free = False
            try:
                h4s = driver.find_elements_by_tag_name("h4")
                for h4 in h4s:
                    if "Full Course, No Certificate" in h4.text:
                        is_free = True
            except NoSuchElementException:
                pass
            sleep(1.3)

            if is_free:
                logging.info("course is free \\o/ :)")
                fare = 0

            # proceed only if course is not free
            else:
                logging.info("check if one can audit the course ...")
                is_auditable = False

                # most courses have a sublime link "audit only" link
                try:
                    driver.find_element_by_id("enroll_subscribe_audit_button")
                    is_auditable = True
                except NoSuchElementException:
                    pass

                if is_auditable:
                    logging.info("course is auditable :)")
                    fare = 1

                # if course is not auditable with the link, check if there is same enroll option
                else:
                    # some courses have audit option in primary-description
                    is_alternatively_auditable = False
                    try:
                        h4s = driver.find_elements_by_tag_name("h4")
                        for h4 in h4s:
                            if "Audit only" in h4.text:
                                is_alternatively_auditable = True
                    except NoSuchElementException:
                        pass
                    finally:
                        if is_alternatively_auditable:
                            logging.info("course is auditable :)")
                            fare = 1
                        else:
                            logging.info("course is pay only :(")
                            fare = 2
                sleep(1.2)

            conn.execute("""INSERT INTO offerings (link, title, university, category, fare) VALUES (?, ?, ?, ?, ?)""",
                         (link, _course['title'], _course['university'], _course['category'], fare))
            conn.commit()

        except ElementNotInteractableException:
            logging.info("there are no upcoming sessions available ...")

    else:
        logging.info("course already scanned ...")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    login(email, password)

    # ...
    records = "results/courses"
    if not os.path.isdir(records):
        logging.error("directory \"{}\" not found!".format(records))
        exit(1)

    conn = init_db()

    # ...
    for category in os.listdir(records):
        if category.endswith(".csv"):
            # if category.endswith("life-sciences---animal-health.csv"):
            logging.info("processing category \"{}\"".format(category))
            with open(os.path.join(records, category), newline='') as courses:
                reader = csv.DictReader(courses)
                for course in reader:
                    if course['form'] == "course":
                        get_course_offering(course)
                        # if course['link'] == "https://www.coursera.org/learn/global-disease-non-communicable":
                        #     get_course_offering(course)

    conn.close()
    driver.close()
