from utils.verif_utils import *


def test_workspace_name_mandatory(driver, config):
    url = config["app"]["url"]
    expected_workspace_missing_text = config["app"]["expected_workspace_missing_text"]
    delay = config["app"]["delay"]
    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # locating and clicking Next button
    result = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Next']"),
                            click_element=True)
    assert result is not None, "Next button failed to click"

    time.sleep(delay)

    # Validate error message
    text_found = verify_text_on_page(driver, expected_workspace_missing_text, timeout=15)
    assert text_found, f"{expected_workspace_missing_text} was NOT displayed in the page as expected"
