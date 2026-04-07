from utils.verif_utils import *


def test_invalid_passwords(driver, config):
    url = config["app"]["url"]

    expected_password_invalid_text = config["app"]["expected_password_invalid_text"]
    invalid_list = config["app"]["invalid_password_list"]
    delay = config["app"]["delay"]

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Locating/clicking Sign up button
    result = locate_element(driver, (By.PARTIAL_LINK_TEXT, 'Sign up'), click_element=True)
    assert result is not None, "Sign up button failed to click"

    logger.info(f"[STEP] validating each invalid pwd input from {invalid_list}")
    time.sleep(delay)
    for password in invalid_list:
        try:
            logger.info(f"[STEP] Validating password error message for input: {password}")
            password_input = locate_element(driver, (By.XPATH, "//input[contains(@placeholder,'password')]"))
            assert password_input is not None, "Password button failed to click"

            password_input.click()
            password_input.send_keys(Keys.CONTROL + "a")
            password_input.send_keys(Keys.DELETE)
            password_input.send_keys(password)

            next_button = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Next']"),
                                         click_element=True)
            assert next_button is not None, "Next button failed to click"

            time.sleep(delay)
            text_found = verify_text_on_page(driver, expected_password_invalid_text, timeout=15)
            assert text_found, f"{expected_password_invalid_text} was NOT displayed in the sign up page as expected"
            time.sleep(delay)
            password_input.clear()

        except Exception as e:
            logger.error("[ERROR] Expected error message for invalid Pwd input not found on the page ❌")
            logger.error(str(e))
            assert False, f"Password invalid validation failed: {str(e)}"
