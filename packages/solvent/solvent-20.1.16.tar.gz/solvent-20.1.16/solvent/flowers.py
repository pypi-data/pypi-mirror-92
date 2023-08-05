import log
import pomace
import random

URL = "https://www.beckysflowersmidland.com/contacts.html"


def main():
    submits = 0
    errors = 0

    pomace.freeze()

    while errors < 10:
        page = pomace.visit(URL)

        person = pomace.fake.person
        page.fill_date("1/5/21")
        page.fill_full_name(person.first_name + " " + person.last_name)
        page.fill_email(person.email)
        page.fill_message(
            random.choice(
                [
                    "https://twitter.com/Cleavon_MD/status/1347334743323394048",
                    "https://www.instagram.com/p/CJw0GrLHazm/",
                ]
            )
        )
        result = page.click_submit_request()

        if result.url != URL:
            submits += 1
            errors = 0
            log.info(f"Submission count: {submits}")
        else:
            errors += 1
            log.info(f"Error count: {errors}")
