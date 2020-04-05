from selenium import webdriver
from pprint import pprint
import json


if __name__ == "__main__":
    driver = webdriver.Firefox("/usr/local/bin/")
    driver.get("https://www.coursera.org")
    html = driver.page_source

    state = ""
    lines = html.split("\n")
    for line in lines:
        if "__APOLLO_STATE__" in line:
            state = line.split(" = ")[1]

    # cut unrelated category state content and close of to form proper json
    domains = state.split("$ROOT_QUERY.DomainsV1Resource.getAll")[0]
    categories = domains[:-2] + "}"

    pprint(json.loads(categories))

    driver.close()
