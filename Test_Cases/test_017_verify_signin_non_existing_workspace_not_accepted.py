from utils.verif_utils import *
from utils.random_email_and_workspace_generator import *


def test_signin_using_non_existing_workspace(driver, config):
    url = config["app"]["url"]
    workspace = generate_unique_workspace_name(config["app"]["workspace"])
    delay = config["app"]["delay"]
    xpath = f"//div[@role='alert']//div[normalize-space()='Org Id not found for subdomain: {workspace}']"

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    initial_url = driver.current_url
    logger.info(f"[INFO] Initial URL before action: {initial_url}")

    logger.info(f"[STEP] Entering (non existing) workspace name")

    # Locating workspace element
    workspace_input = locate_element(driver, (By.XPATH, "//input[contains(@placeholder,'Workspace')]"),
                                     click_element=True)
    assert workspace_input is not None, "Workspace element not found!"

    time.sleep(delay)

    workspace_input.send_keys(workspace)
    logger.info(f"[INFO] Workspace entered: {workspace}")
    time.sleep(delay)
    # locating and clicking Next button
    result = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Next']"),
                            click_element=True)
    assert result is not None, "Next button failed to click"
    logger.info(f"[SUCCESS] Next button clicked...")
    time.sleep(delay)
    # locating and Org Id Not Found Error

    org_id_error = locate_element(driver, (By.XPATH, xpath),
                                  )
    assert org_id_error is not None, f"'Org Id not found for subdomain: {workspace}' error NOT populated as expected!"
    logger.info(f"[SUCCESS] 'Org Id not found for subdomain: {workspace}' error populated as expected! Test Passed")

    current_url = driver.current_url
    logger.info(f"[INFO] Current URL after action: {current_url}")

    # verify current url does not change
    logger.info("[STEP] Verify current url does not change..")
    url_navigated = verify_url_change(driver, initial_url)
    assert not url_navigated, f"URL changed! (Not expected): {current_url}"

    logger.info(f"[SUCCESS] Verified: User stayed on the same page {current_url} as expected. ✅")
