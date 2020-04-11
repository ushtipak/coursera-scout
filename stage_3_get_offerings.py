import logging
from time import sleep

from selenium import webdriver

driver = webdriver.Firefox("/usr/local/bin/")

email = "lhbpujoqyhwzwxtaxp@ttirv.com"
password = "https://www.selenium.dev/downloads/"


def login(_email, _password):
    """Sign in with provided credentials."""
    logging.info("calling login with email \"{}\"".format(_email))
    url = "https://www.coursera.org"
    logging.info("url: {}".format(url))
    driver.get(url)
    sleep(8.3)

    driver.find_elements_by_link_text("Log In")[0].click()
    driver.find_elements_by_name("email")[0].send_keys(_email)
    driver.find_elements_by_name("password")[0].send_keys(_password)
    # class "_1hx9z6hg" covers three, we're using last:
    # - continue with facebook
    # - continue with apple
    # - log in
    driver.find_elements_by_class_name("_1hx9z6hg")[2].click()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    login(email, password)
