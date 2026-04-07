from utils.verif_utils import *
from utils.random_email_and_workspace_generator import *


def test_email_exists_functionality(driver, config):
    url = config["app"]["url"]
    expected_signup_text = config["app"]["expected_signup_text"]
    # fetching existing email from input_variables/test_signin_credentials.json
    base_dir = os.getcwd()  # project root
    file_path = os.path.join(base_dir, "input_variables", "test_signin_credentials.json")
    with open(file_path) as f:
        data = json.load(f)
    email = data["email"]
    pwd = config["app"]["pwd"]
    # generate unique workspace name
    workspace = generate_unique_workspace_name(config["app"]["workspace"])
    delay = config["app"]["delay"]
    credentials = {"email": email, "password": pwd, "workspace name": workspace}

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Locating/clicking Sign up button
    sign_up_element = locate_element(driver, (By.PARTIAL_LINK_TEXT, 'Sign up'), click_element=True)
    assert sign_up_element is not None, "Sign up button failed to click"

    # Locating Sign up Text
    text_found = verify_text_on_page(driver, expected_signup_text, timeout=15)
    assert text_found, f"{expected_signup_text} was NOT displayed in the sign up page as expected"

    # Enter credentials
    logger.info(f"[STEP] Entering email, password and workspace name")
    form_success = enter_form_data(driver, credentials, delay=2)

    assert form_success, "Form entry failed. Check the logs to see which field was missing."
    logger.info(f"[STEP] Entered email, password and workspace name")

    current_url = driver.current_url
    logger.info(f"[STEP] Clicking Next button...")

    next_button = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Next']"),
                                 click_element=True)
    assert next_button is not None, "Next button failed to click"
    logger.info(f"[STEP] Clicked Next button...")

    logger.info(f"[STEP] Locating 'email already exists Error'...")

    email_error = locate_element(driver,
                                 (By.XPATH, "//div[@role='alert']//div[normalize-space()='email already exists']"),
                                 )
    assert email_error is not None, "Email error not located"

    logger.info(f"[STEP] Located 'email already exists Error'...'")

    logger.info("[STEP] Verify current url does not change..")
    url_navigated = verify_url_change(driver, current_url)
    assert not url_navigated, f"URL changed! (Not expected): {current_url}"

    logger.info(f"[SUCCESS] Verified: User stayed on the same page {current_url} as expected. ✅")
