from utils.verif_utils import *


def test_signin_disabled_options(driver, config):
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
    xpath_str = "//button[contains(., 'Continue to plans')]"

    expected_available_plans_text = config["app"]["expected_available_plans_text"]
    unsubscribe_disable_tab_list = config["app"]["unsubscribe_disable_tab_list"]
    unsubscribe_enable_tab_list = config["app"]["unsubscribe_enable_tab_list"]
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

    logger.info("[STEP] Verifying available plans page opens ...")

    text_found = verify_text_on_page(driver, expected_available_plans_text, timeout=15)
    assert text_found, f"{expected_available_plans_text} was NOT displayed in the page as expected"
    logger.info(f"[SUCCESS] '{expected_available_plans_text}' found on page ✅")

    logger.info(f"[STEP] Clicking 'Setup Later' button...")

    setup_later = locate_element(driver, (By.XPATH, "//span[contains(text(), 'Setup Later')]"),
                                 click_element=True)
    assert setup_later is not None, "Failure in clicking 'Setup Later' button"
    logger.info(f"[SUCCESS] 'Setup Later' button clicked...")

    logger.info(f"[STEP] Verifying Disabled tabs...")
    time.sleep(delay)

    for tab in unsubscribe_disable_tab_list:

        try:

            logger.info(f"[STEP] Verifying '{tab}' tab is disabled...")
            xpath1 = f"//span[text()='{tab}']/ancestor::li"
            xpath2 = f"//span[contains(., '{tab}')]"
            if tab == "IAM":
                driver.find_element(By.XPATH, "//span[contains(., 'Administration')]").click()

            tab_element = driver.find_element(By.XPATH, xpath1)
            classes = tab_element.get_attribute("class")
            time.sleep(delay)
            assert "disabled" in classes.lower(), f"Expected 'disabled' in class list, but got: {classes}"
            logger.info(f"[SUCCESS] {tab} tab disabled for unsubscribed user...")
            time.sleep(delay)
            logger.info(f"[STEP] Verifying URL does not change after clicking: '{tab}'tab")
            current_url = driver.current_url
            try:
                driver.find_element(By.XPATH, xpath2).click()
                time.sleep(delay)
            except:
                pass

            assert driver.current_url == current_url, "URL changed! The tab was clickable."
            logger.info(f"[SUCCESS] Verified URL does not change after clicking disabled tab: '{tab}'")
            time.sleep(delay)

        except Exception as e:
            logger.error(f"[ERROR] Failure in Verifying tab status ❌")
            logger.error(str(e))
            assert False, f"Failure in Verifying tab status: {str(e)}"

    time.sleep(delay)

    logger.info(f"[STEP] Verifying Enabled tabs...")

    for tab in unsubscribe_enable_tab_list:
        try:

            logger.info(f"[STEP] Verifying '{tab}' tab is enabled...")
            xpath1 = f"//span[text()='{tab}']/ancestor::li"
            xpath2 = f"//span[contains(., '{tab}')]"
            if tab == "IAM":
                driver.find_element(By.XPATH, "//span[contains(., 'Administration')]").click()

            tab_element = driver.find_element(By.XPATH, xpath1)
            classes = tab_element.get_attribute("class")
            time.sleep(delay)
            assert "disabled" not in classes.lower(), f"Expected no 'disabled' in class list, but got: {classes}"
            logger.info(f"[SUCCESS] {tab} tab enabled for unsubscribed user...")
            time.sleep(delay)

            if tab == "SxR":
                driver.find_element(By.XPATH, "//span[text()='SxR']").click()
                current_url = driver.current_url
                assert current_url == "https://stage.sxalable.io/devices/sxr", \
                    f"Expected SxR URL, but got: {current_url}"
                logger.info(f"[SUCCESS] {tab} is clickable...")

            if tab == "Administration":
                driver.find_element(By.XPATH, xpath2).click()
                current_url = driver.current_url
                assert current_url == "https://stage.sxalable.io/admin/subscriptions", \
                    f"Expected subscription URL, but got: {current_url}"
                logger.info(f"[SUCCESS] {tab} is clickable...")
                time.sleep(delay)

        except Exception as e:
            logger.error(f"[ERROR] Failure in Verifying tab status ❌")
            logger.error(str(e))
            assert False, f"Failure in Verifying tab status: {str(e)}"
