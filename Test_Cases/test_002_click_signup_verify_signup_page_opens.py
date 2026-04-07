from utils.verif_utils import *


def test_signup_flow(driver, config):
    url = config["app"]["url"]
    expected_signup_text = config["app"]["expected_signup_text"]
    expected_signup_url = "https://stage.sxalable.io/signup"
    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."
    current_url = driver.current_url
    # locating and clicking Sign up button
    result = locate_element(driver, (By.PARTIAL_LINK_TEXT, 'Sign up'), click_element=True)
    assert result is not None, "Sign up button failed to click"

    # Verifying Sign up URL

    url_navigated = verify_url_change(driver, current_url)
    assert url_navigated, f"Navigation timed out! Still stuck on {current_url}"

    url_contains = verify_url_contains(driver, expected_signup_url )
    assert url_contains, f"Failed to redirect to dashboard. Current URL: {driver.current_url}"

    # Verify Sign up text

    text_found = verify_text_on_page(driver, expected_signup_text, timeout=15)
    assert text_found, f"{expected_signup_text} was NOT displayed in the sign up page as expected"
