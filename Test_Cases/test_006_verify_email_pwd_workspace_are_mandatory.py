from utils.verif_utils import *


def test_signup_mandatory_inputs(driver, config):
    url = config["app"]["url"]
    expected_signup_text = config["app"]["expected_signup_text"]
    expected_email_missing_text = config["app"]["expected_email_missing_text"]
    expected_pwd_missing_text = config["app"]["expected_pwd_missing_text"]
    expected_workspace_missing_text = config["app"]["expected_workspace_missing_text"]

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Locating/clicking Sign up button
    result = locate_element(driver, (By.PARTIAL_LINK_TEXT, 'Sign up'), click_element=True)
    assert result is not None, "Sign up button failed to click"

    # Locating Sign up Text
    text_found = verify_text_on_page(driver, expected_signup_text, timeout=15)
    assert text_found, f"{expected_signup_text} was NOT displayed in the sign up page as expected"

    # Locating/clicking Next button
    result = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Next']"),
                            click_element=True)
    assert result is not None, "Next button failed to click"

    # Locating email mandatory error
    text_found = verify_text_on_page(driver, expected_email_missing_text, timeout=15)
    assert text_found, f"{expected_email_missing_text} was NOT displayed in the sign up page as expected"

    # Locating Pwd mandatory error
    text_found = verify_text_on_page(driver, expected_pwd_missing_text, timeout=15)
    assert text_found, f"{expected_pwd_missing_text} was NOT displayed in the sign up page as expected"

    # Locating workspace mandatory error
    text_found = verify_text_on_page(driver, expected_workspace_missing_text, timeout=15)
    assert text_found, f"{expected_workspace_missing_text} was NOT displayed in the sign up page as expected"
