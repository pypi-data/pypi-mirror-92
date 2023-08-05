import log
import pomace

import random
import time


def main():
    # pomace.freeze()
    attempted = completed = failed = 0
    while failed < 10:
        attempted += 1
        person = pomace.fake.person

        page = pomace.visit("https://www.mypillow.com/")

        log.debug("Waiting for modal...")
        for _ in range(10):
            time.sleep(0.5)
            modal = pomace.shared.browser.find_by_id("ltkpopup-content")
            if modal and modal.visible:
                break
        else:
            log.warn("No modal found")

        log.info(f"Submitting phone number: {person.phone}")
        page.fill_phone(person.phone)
        page = page.click_submit()

        if "Thank you!" in page:
            completed += 1
            failed = 0
        else:
            failed += 1

        log.info(f"Iterations: {attempted=} {completed=} {failed=}")

        log.info("Clearing cookies")
        pomace.shared.browser.cookies.delete()
