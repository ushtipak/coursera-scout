"""
Create a list of Coursera categories from Apollo state retrieved with Selenium

Categories are saved to `coursera-categories.txt`
"""

import json

from selenium import webdriver

if __name__ == "__main__":
    driver = webdriver.Firefox("/usr/local/bin/")
    driver.get("https://www.coursera.org")
    html = driver.page_source

    state = ""
    lines = html.split("\n")
    for line in lines:
        if "__APOLLO_STATE__" in line:
            state = line.split(" = ")[1]

    # cut unrelated category content and seal json correctly
    categories = state.split("$ROOT_QUERY.DomainsV1Resource.getAll")[0]
    categories = categories[:-2] + "}"
    categories = json.loads(categories)

    # save mapping of domain-ids and sub domains
    with open("coursera-categories.txt", "w") as f:
        for category in categories:
            if "SubdomainsV1:" in category:
                f.write("{}/{}\n".format(categories[category]["domainId"], category[13:]))

    driver.close()
