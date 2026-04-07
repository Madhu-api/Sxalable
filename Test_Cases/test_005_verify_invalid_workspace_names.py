from utils.verif_utils import *


def test_invalid_workspace_names(driver, config):
    url = config["app"]["url"]
    expected_workspace_invalid_text = config["app"]["expected_workspace_invalid_text"]
    delay = config["app"]["delay"]
    invalid_list = config["app"]["invalid_workspace_list"]

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Locating workspace element
    workspace_input = locate_element(driver, (By.XPATH, "//input[contains(@placeholder,'Workspace')]"))
    assert workspace_input is not None, "Workspace element not found!"

    logger.info(f"[STEP] validating each invalid input from {invalid_list}")
    time.sleep(delay)
    for workspace in invalid_list:
        try:
            logger.info(f"[STEP] Validating workspace error message for input: {workspace}")

            workspace_input.click()
            workspace_input.send_keys(Keys.CONTROL + "a")
            workspace_input.send_keys(Keys.DELETE)
            workspace_input.send_keys(workspace)

            next_button = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Next']"),
                                         click_element=True)
            assert next_button is not None, "Issue in finding/clicking Next button!"
            time.sleep(delay)
            text_found = verify_text_on_page(driver, expected_workspace_invalid_text, timeout=15)
            assert text_found, f"{expected_workspace_invalid_text} was NOT displayed in the page as expected"
            workspace_input.clear()

        except Exception as e:
            logger.error("[ERROR] Expected error message for invalid workspace input not found on the page ❌")
            logger.error(str(e))
            assert False, f"Workspace invalid validation failed: {str(e)}"
