from utils.verif_utils import *
from utils.unique_router_name_generator import *


def test_signin_cannot_deploy_SxR_no_subscription(driver, config):
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
    expected_subscription_incomplete_text = config["app"]["expected_subscription_incomplete_text"]
    expected_available_plans_text = config["app"]["expected_available_plans_text"]
    router_name = generate_unique_router_name(config["SxR"]["name"])
    router_credentials = {"Enter router name": router_name}
    db_config = config["db"]
    ssh_config = config["ssh"]
    xpath_str = "//button[contains(., 'Continue to plans')]"

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Sign In
    logger.info(f"[STEP] Signing in...")
    sign_in_status = verify_successful_signin(driver, workspace, email, pwd, db_config, ssh_config)
    assert sign_in_status, "Sign in NOT successful ❌"
    logger.info(f"[SUCCESS] Sign in is successful ✅")

    #  Verify 'continue to plans' button enabled, assuming user details have already
    #  been entered by previous test-case
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

    # Verifying available plans page opens
    logger.info("[STEP] Verifying available plans page opens ...")

    text_found = verify_text_on_page(driver, expected_available_plans_text, timeout=15)
    assert text_found, f"{expected_available_plans_text} was NOT displayed in the page as expected"
    logger.info(f"[SUCCESS] '{expected_available_plans_text}' found on page ✅")

    # Click Setup later, Add SxR verify for Add SxR heading

    xpath_list = [{"setup_later_button": "//span[contains(text(), 'Setup Later')]"},
                  {"Add_SxR_button": "//span[normalize-space()='Add SxR']/ancestor::button"},
                  {"Add_SxR_text": "//h6[text()='Add SxR']"}]

    for xpath in xpath_list:

        for key, value in xpath.items():
            time.sleep(delay)
            logger.info(f"[STEP] Clicking '{key}' button...")
            button = locate_element(driver, (By.XPATH, value),
                                    click_element=True)
            assert button is not None, "Failure in clicking '{key}' button"
            logger.info(f"[SUCCESS] Clicked '{key}' button......")
            time.sleep(delay)

    # Entering Router name
    logger.info(f"[STEP] Entering Router name...")
    time.sleep(delay)
    form_success = enter_form_data(driver, router_credentials, delay=2)
    assert form_success, "Form entry failed. Check the logs to see which field was missing."
    logger.info(f"[STEP] Entered Router details successfully")

    # Click Manual mode, Save button, deploy button

    xpath_list = [{"manual_radio_button": "//label[.//input[@value='manual']]"},
                  {"save_button": "//button[normalize-space()='Save']"},
                  {"deploy_button": "//*[@data-testid='PlayCircleOutlineRoundedIcon']/ancestor::button"}]

    for xpath in xpath_list:

        for key, value in xpath.items():
            time.sleep(delay)
            logger.info(f"[STEP] Clicking '{key}' button...")
            button = locate_element(driver, (By.XPATH, value),
                                    click_element=True)
            assert button is not None, f"Failure in clicking '{key}' button"
            logger.info(f"[SUCCESS] Clicked '{key}' button......")
            time.sleep(delay)

    # Verify 'Your subscription is incomplete' msg.

    logger.info(f"[STEP] Verify 'Your subscription is incomplete' msg...")
    text_found = verify_text_on_page(driver, expected_subscription_incomplete_text, timeout=15)
    assert text_found, f"{expected_subscription_incomplete_text} was NOT displayed in the page as expected"
    logger.info(f"[SUCCESS] '{expected_subscription_incomplete_text}' found on page ✅")

    # click may be later, delete button, remove router, confirmation
    xpath_list = [{"maybe_later_btn": "//button[text()='May be later']"},
                  {"vert_dots_button": "//*[local-name()='svg' and @data-testid='MoreVertIcon']"},
                  {"remove_router": "//li[@role='menuitem' and normalize-space()='Remove Router']"},
                  {"confirmation": "//button[normalize-space()='Yes, Delete it']"}]

    for xpath in xpath_list:

        for key, value in xpath.items():
            time.sleep(delay)
            logger.info(f"[STEP] Clicking '{key}' button...")
            button = locate_element(driver, (By.XPATH, value),
                                    click_element=True)
            assert button is not None, f"Failure in clicking '{key}' button"
            logger.info(f"[SUCCESS] Clicked '{key}' button......")
            time.sleep(delay)

    # Verify Router is not found on SxR page after deletion.
    logger.info(f"[STEP] Verify Router '{router_name}' is not found on SxR page after deletion...")

    deleted_item_xpath = f"//p[@title='{router_name}']"

    is_absent = verify_element_absent(driver, (By.XPATH, deleted_item_xpath))
    assert is_absent, f"Router '{router_name}' validation failure in SxR page after deletion"
    logger.info(f" Router '{router_name}' not found on SxR page after deletion as expected ✅")
    time.sleep(delay)