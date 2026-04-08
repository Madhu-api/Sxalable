from utils.verif_utils import *
from utils.random_user_details_generator import *


def test_signin_enter_user_details(driver, config):
    url = config["app"]["url"]
    base_dir = os.getcwd()  # project root
    file_path = os.path.join(base_dir, "input_variables", "test_signin_credentials.json")
    with open(file_path) as f:
        data = json.load(f)
    email = data["email"]
    workspace = data["workspace"]
    # pwd = config["app"]["change_pwd"]  # user change_pwd for batch run
    pwd = config["app"]["pwd"]
    delay = config["app"]["delay"]
    # generating unique name with username 'Automationuser' with only a-z characters
    first_name = generate_unique_first_name(config["user"]["first_name"])
    # generating unique name with username 'Automationcompany' with only a-z characters
    company_name = generate_unique_first_name(config["user"]["company_name"])
    # generating unique company address with only a-z characters
    company_address = generate_unique_first_name(config["user"]["company_address"])
    expected_available_plans_text = config["app"]["expected_available_plans_text"]

    user_credentials = {"Enter your first name": first_name, "Enter your company name": company_name,
                        "Enter your company address": company_address}
    db_config = config["db"]
    ssh_config = config["ssh"]

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Sign In
    logger.info(f"[STEP] Signing in...")
    sign_in_status = verify_successful_signin(driver, workspace, email, pwd, db_config, ssh_config)
    assert sign_in_status, "Sign in NOT successful ❌"
    logger.info(f"[SUCCESS] Sign in is successful ✅")

    # Verifying Continue to plans button initially disabled

    logger.info("[STEP] Verifying Continue to plans button initially disabled..")

    #  Verify initial state (Disabled)
    xpath_str = "//button[contains(., 'Continue to plans')]"
    assert not verify_button_enabled_by_xpath(driver, xpath_str), "Continue Button should be disabled, but not disabled"
    logger.info(f"[SUCCESS] Continue Button is disabled initially ✅")

    # Entering user details
    logger.info("[STEP] Entering user details..")
    time.sleep(delay)
    form_success = enter_form_data(driver, user_credentials, delay=2)

    assert form_success, "Form entry failed. Check the logs to see which field was missing."
    logger.info(f"[STEP] Entered User details successfully")

    #  Verify 'continue to plans' button enabled
    logger.info("[STEP] Verifying Continue Button is enabled after entering user details...")

    assert verify_button_enabled_by_xpath(driver, xpath_str), "Continue Button should be enabled, but not enabled"
    logger.info(f"[SUCCESS] Continue Button is enabled after entering user details ✅")

    # Clicking 'Continue to Plans' button
    logger.info(f"[STEP] Clicking 'Continue to Plans' button...")
    time.sleep(delay)
    continue_button = locate_element(driver, (By.XPATH, xpath_str),
                                     click_element=True)
    assert continue_button is not None, "Continue button failed to click"
    logger.info(f"[SUCCESS] Clicked 'Continue to Plans' button...")
    time.sleep(delay)

    logger.info("[STEP] Verifying available plans page opens ...")

    text_found = verify_text_on_page(driver, expected_available_plans_text, timeout=15)
    assert text_found, f"{expected_available_plans_text} was NOT displayed in the page as expected"
    logger.info(f"[SUCCESS] '{expected_available_plans_text}' found on page ✅")

    logger.info(f"[STEP] Clicking 'Setup Later' button...")

    setup_later = locate_element(driver, (By.XPATH, "//span[contains(text(), 'Setup Later')]"),
                                 click_element=True)
    assert setup_later is not None, "Failure in clicking 'Setup Later' button"
    logger.info(f"[SUCCESS] 'Setup Later' button clicked...")

    # Save Admin username and org in input_variables/test_signin_credentials.json for further use
    data["admin_username"] = first_name
    data["organization"] = company_name

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"[SUCCESS] credential stored in  input_variables/test_signin_credentials.json")
