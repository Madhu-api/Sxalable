from utils.verif_utils import *


def test_signin_using_invalid_pwd(driver, config):
    url = config["app"]["url"]
    base_dir = os.getcwd()  # project root

    delay = config["app"]["delay"]
    file_path = os.path.join(base_dir, "input_variables", "test_signin_credentials.json")
    with open(file_path) as f:
        data = json.load(f)
    workspace = data["workspace"]
    email = data["email"]
    pwd = "Test@12345"  # invalid pwd
    credentials = {"email": email, "password": pwd}
    expected_signin_page_url = "https://stage.sxalable.io/login"
    xpath = "//div[@role='alert']//div[normalize-space()='Invalid Password']"

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    logger.info(f"[STEP] Entering workspace name")

    # Locating workspace element
    workspace_input = locate_element(driver, (By.XPATH, "//input[contains(@placeholder,'Workspace')]"),
                                     click_element=True)
    assert workspace_input is not None, "Workspace element not found!"

    time.sleep(delay)
    # Entering workspace name
    workspace_input.send_keys(workspace)
    logger.info(f"[INFO] Workspace entered: {workspace}")
    time.sleep(delay)

    # locating and clicking Next button
    result = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Next']"),
                            click_element=True)
    assert result is not None, "Next button failed to click"
    logger.info(f"[SUCCESS] Next button clicked...")

    time.sleep(delay)

    # Checking Sign in page URL
    logger.info(f"[STEP] Checking Sign in page URL...")
    url_contains = verify_url_contains(driver, expected_signin_page_url)
    assert url_contains, f"Failed to redirect to Sign in Page. Current URL: {driver.current_url}"
    logger.info(f"[STEP] Checked Sign in page URL...")

    # Note current url
    current_url = driver.current_url
    logger.info(f"[INFO] Initial URL before Sign in action: {current_url}")

    # Entering credentials
    logger.info(f"[STEP] Entering email, (invalid) password")
    form_success = enter_form_data(driver, credentials, delay=2)
    assert form_success, "Form entry failed. Check the logs to see which field was missing."
    logger.info(f"[STEP] Entered email, password")

    # locating and clicking Login button
    logger.info(f"[STEP] locating and clicking Login button")
    result = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Login']"),
                            click_element=True)
    assert result is not None, "Login button failed to click"
    logger.info(f"[INFO] Clicked Login button...")
    time.sleep(delay)

    # Locating 'Invalid Password' error
    result = locate_element(driver, (By.XPATH, xpath))
    assert result is not None, "Unable to locate Invalid password error"
    logger.info(f"[INFO] located Invalid password error as expected...")
    time.sleep(delay)

    # verify current url does not change after the error
    logger.info("[STEP] Verify current url does not change after the error..")
    url_navigated = verify_url_change(driver, current_url)
    assert not url_navigated, f"URL changed! (Not expected): {driver.current_url}"

    logger.info(f"[SUCCESS] Verified: User stayed on the same page {current_url} after error "
                f"as expected. ✅")

