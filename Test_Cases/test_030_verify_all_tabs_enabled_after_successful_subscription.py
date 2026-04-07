from utils.verif_utils import *


def test_signin_successful_subscription(driver, config):
    url = config["app"]["url"]
    base_dir = os.getcwd()  # project root
    file_path = os.path.join(base_dir, "input_variables", "test_signin_credentials.json")
    with open(file_path) as f:
        data = json.load(f)
    email = data["email"]
    workspace = data["workspace"]
    pwd = config["app"]["pwd"]
    db_config = config["db"]
    ssh_config = config["ssh"]
    delay = config["app"]["delay"]
    subscribe_enable_tab_list = config["app"]["subscribe_enable_tab_list"]

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Sign In
    logger.info(f"[STEP] Signing in...")
    sign_in_status = verify_successful_signin(driver, workspace, email, pwd, db_config, ssh_config)
    assert sign_in_status, "Sign in NOT successful ❌"
    logger.info(f"[SUCCESS] Sign in is successful ✅")

    logger.info(f"[STEP] Verifying Enabled tabs...")

    for tab in subscribe_enable_tab_list:
        try:

            logger.info(f"[STEP] Verifying '{tab}' tab is enabled...")
            xpath1 = f"//span[text()='{tab}']/ancestor::li"
            tab_element = driver.find_element(By.XPATH, xpath1)
            classes = tab_element.get_attribute("class")
            time.sleep(delay)
            assert "disabled" not in classes.lower(), f"Expected no 'disabled' in class list, but got: {classes}"
            logger.info(f"[SUCCESS] {tab} tab enabled for subscribed user...")
            time.sleep(delay)
            current_url = driver.current_url
            # Clicking tab element and verifying url navigation
            if tab != 'Dashboard':  # assuming current url is on dashboard, url change is not required

                logger.info("[STEP] Verifying Page navigated...")
                tab_element.click()
                time.sleep(delay)
                url_navigated = verify_url_change(driver, current_url)
                assert url_navigated, f"Navigation timed out! Still stuck on {current_url}"
                logger.info(f"[SUCCESS] Page successfully navigated for tab: {tab}..")

            if tab == 'Administration':
                xpath2 = f"//span[text()='IAM']/ancestor::li"
                xpath3 = f"//span[text()='Subscriptions']/ancestor::li"
                tab_element2 = driver.find_element(By.XPATH, xpath2)
                tab_element3 = driver.find_element(By.XPATH, xpath3)
                tab_element_list = [tab_element2, tab_element3]
                for tab_element in tab_element_list:
                    classes = tab_element.get_attribute("class")
                    time.sleep(delay)
                    assert "disabled" not in classes.lower(), f"Expected no 'disabled' in class list, but got: {classes}"
                    logger.info(f"[SUCCESS] {tab} tab enabled for subscribed user...")
                    if tab_element != tab_element2:
                        logger.info("[STEP] Verifying Page navigated...")
                        tab_element.click()
                        time.sleep(delay)
                        url_navigated = verify_url_change(driver, current_url)
                        assert url_navigated, f"Navigation timed out! Still stuck on {current_url}"
                        logger.info("[SUCCESS] Page successfully navigated for Subscription..")

                time.sleep(delay)

            time.sleep(delay)

        except Exception as e:
            logger.error(f"[ERROR] Failure in Verifying tab status ❌")
            logger.error(str(e))
            assert False, f"Failure in Verifying tab status: {str(e)}"
