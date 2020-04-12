import logging
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import *

driver = webdriver.Firefox("/usr/local/bin/")

email = "lhbpujoqyhwzwxtaxp@ttirv.com"
password = "https://www.selenium.dev/downloads/"


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


def get_course_offering(_url):
    """...."""
    logging.info("calling get_course_offering with url \"{}\"".format(_url))
    driver.get(_url)
    sleep(4.7)

    logging.info("click on enroll ...")
    driver.find_elements_by_class_name("EnrollButton")[0].click()
    sleep(2.2)

    logging.info("check if course is part of multiple specializations ...")
    is_unique = True
    try:
        choose_specialization = driver.find_element_by_id("course_enroll_s12n_selection_button_button")
        is_unique = False
        choose_specialization.click()
    except NoSuchElementException:
        pass
    if not is_unique:
        logging.info("MULTIPLE SPECIALIZATIONS")
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
        logging.info("COURSE IS FREE !!!")
    else:
        logging.info("check if one can audit the course ...")
        is_auditable = False
        try:
            driver.find_element_by_id("enroll_subscribe_audit_button")
            is_auditable = True
        except NoSuchElementException:
            pass
        if is_auditable:
            logging.info("COURSE IS AT LEAST AUDITABLE !!!")
        else:
            logging.info("closed af :(")
        sleep(1.2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    login(email, password)

    # examples of completely free courses
    # get_course_offering("https://www.coursera.org/learn/science-of-meditation")
    # get_course_offering("https://www.coursera.org/learn/egypt")

    # examples of courses that aren't free, but can be audited
    # get_course_offering("https://www.coursera.org/learn/introcss")
    # get_course_offering("https://www.coursera.org/learn/javascript")

    # example of course that is part of multiple specializations
    # get_course_offering("https://www.coursera.org/learn/bootstrap-4")

    get_course_offering("https://www.coursera.org/learn/praktiki-raboty-dannymi-sredstvami-power-query-pivot")
    get_course_offering("https://www.coursera.org/learn/detecting-cyber-attacks")
    get_course_offering("https://www.coursera.org/learn/financing-infrastructure-in-african-cities")
    get_course_offering("https://www.coursera.org/learn/nonprofit-gov-capstone")
    get_course_offering("https://www.coursera.org/learn/intro-redes-sociales")
    get_course_offering("https://www.coursera.org/learn/image-processing")
    get_course_offering("https://www.coursera.org/learn/cennye-bumagi-pravovoe-regulirovanie")
    get_course_offering("https://www.coursera.org/learn/basic-sentiment-analysis-tensorflow")
    get_course_offering("https://www.coursera.org/learn/game-theory-1")
    get_course_offering("https://www.coursera.org/learn/web-design-strategy")

    driver.close()
