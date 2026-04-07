from utils.verif_utils import *


def test_homepage_welcome_text(driver, config):
    url = config["app"]["url"]
    expected_welcome_text = config["app"]["expected_welcome_text"]
    # Open URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Call the verification utility
    text_found = verify_text_on_page(driver, expected_welcome_text, timeout=15)
    assert text_found, f"{expected_welcome_text} was NOT displayed in the home as expected"
