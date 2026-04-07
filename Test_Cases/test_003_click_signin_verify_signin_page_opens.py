from utils.verif_utils import *


def test_signin_flow(driver, config):
    # Note: This test-case clicks "Are you a Sxalable member? Sign in here" button
    # without entering workspace name
    url = config["app"]["url"]
    expected_signin_text = config["app"]["expected_signin_text"]
    delay = config["app"]["delay"]
    expected_signin_url = "https://stage.sxalable.io/login"
    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."
    current_url = driver.current_url
    # locating and clicking Sign in button
    result = locate_element(driver, (By.PARTIAL_LINK_TEXT, expected_signin_text), click_element=True)
    assert result is not None, "Sign in button failed to click"

    time.sleep(delay)

    # Verifying Sign in URL

    url_navigated = verify_url_change(driver, current_url)
    assert url_navigated, f"Navigation timed out! Still stuck on {current_url}"

    url_contains = verify_url_contains(driver, expected_signin_url)
    assert url_contains, f"Failed to redirect to dashboard. Current URL: {driver.current_url}"

    # Verify Sign in text

    text_found = verify_text_on_page(driver, expected_signin_text, timeout=15)
    assert text_found, f"{expected_signin_text} was NOT displayed in the Sign in page as expected"

