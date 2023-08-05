import time

import log
import pomace


URL = "https://defendyourballot.formstack.com/forms/voter_fraud"


def main():
    submits = 0
    errors = 0

    while errors < 10:
        page = pomace.visit(URL)

        person = pomace.fake.person

        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)

        page.fill_phone(person.phone)

        while "<strong>Your Phone" in page:
            person = pomace.fake.person
            page.fill_first_name(person.first_name)
            page.fill_last_name(person.last_name)
            page.fill_phone(person.phone)
            page.type_tab()

        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)

        page.fill_address(person.address)
        page.fill_city(person.city)
        page.select_state(person.state)
        page.fill_zip_code(person.zip_code)

        page.fill_email(person.email)
        page.fill_email_confirmation(person.email)

        page.select_state_of_the_incident(pomace.fake.state)
        page.fill_county_of_the_incident(person.county)

        page.fill_name_of_the_polling_place("")
        page.fill_description_of_the_incident("More people voted for Biden than Trump.")

        result = page.click_submit_form()

        if pomace.shared.browser.url == URL:
            log.warn("Complete CAPTCHA manually...")
        while pomace.shared.browser.url == URL:
            log.debug("CAPTCHA visible")
            time.sleep(1)

        if "The form was submitted successfully." in result:
            submits += 1
            errors = 0
            log.info(f"Submission count: {submits}")
        else:
            errors += 1
            log.info(f"Error count: {errors}")
