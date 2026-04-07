from utils.verif_utils import *


def test_signin_mandatory_billing_address_input_fields(driver, config):
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

    expected_available_plans_text = config["app"]["expected_available_plans_text"]
    expected_checkout_page_text = config["app"]["expected_checkout_page_text"]
    full_name = config["user"]["user_details"]["full_name"]
    address_line1 = config["user"]["user_details"]["address_line1"]
    country = config["user"]["user_details"]["country"]
    state = config["user"]["user_details"]["state"]
    city = config["user"]["user_details"]["city"]
    pincode = config["user"]["user_details"]["pincode"]
    xpath_str = "//button[contains(., 'Continue to plans')]"
    db_config = config["db"]
    ssh_config = config["ssh"]

    billing_fields = [
        {"name": "full_name", "xpath": "//input[@name='fullName']", "value": full_name},
        {"name": "address_line1", "xpath": "//input[@name='addressline1']", "value": address_line1},
        {"name": "country",
         "xpath": "//div[contains(@class, 'MuiAutocomplete-root') and .//label[text()='Country']]",
         "is_select": True, "value": country},
        {"name": "state", "xpath": "//div[contains(@class, 'MuiAutocomplete-root') and .//label[text()='State']]",
         "is_select": True, "value": state},
        {"name": "city", "xpath": "//div[contains(@class, 'MuiAutocomplete-root') and .//label[text()='City']]",
         "is_select": True, "value": city},
        {"name": "pincode", "xpath": "//input[@name='zipCode']", "value": pincode}
    ]

    add_button_xpath = "//button[normalize-space()='Add']"

    error_msg_xpath = "//div[@role='alert']//div[normalize-space()='Please enter valid billing address']"

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
    time.sleep(delay)
    logger.info(f"[STEP] Clicking 'Select Plan' button...")
    select_plan_button = locate_element(driver, (By.XPATH, "//button[normalize-space()='Select Plan']"),
                                        click_element=True)
    assert select_plan_button is not None, "Select Plan button failed to click"
    logger.info(f"[SUCCESS] Clicked 'Select Plan' button...")
    time.sleep(delay)

    logger.info(f"[STEP] Waiting for Check out page text...")
    text_found = verify_text_on_page(driver, expected_checkout_page_text, timeout=15)
    assert text_found, f"{expected_checkout_page_text} was NOT displayed in the page as expected"
    logger.info(f"[SUCCESS] '{expected_checkout_page_text}' found on page ✅")

    logger.info(f"[STEP] Entering User Details into the form...")
    # user details list of dictionary

    try:
        for i, step in enumerate(billing_fields):
            logger.info(f"[STEP] Step {i + 1}: Entering {step['name']} ({step['value']})...")

            # 1. FIND AND FILL FIELD
            field_element = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, step['xpath']))
            )

            if step.get("is_select"):
                # For Country/State/City: Find the input, type the value, and press ENTER
                input_field = field_element.find_element(By.TAG_NAME, "input")

                # Clear existing data first to ensure a clean type
                input_field.send_keys(Keys.CONTROL + "a")
                input_field.send_keys(Keys.BACKSPACE)

                # Type and hit Enter
                input_field.send_keys(step['value'])
                time.sleep(delay)  # Give the UI a moment to register the text
                option_xpath = f"//li[@role='option' and normalize-space()='{step['value']}']"

                try:
                    option_element = WebDriverWait(driver, 10).until(
                        ec.element_to_be_clickable((By.XPATH, option_xpath))
                    )
                    option_element.click()
                    logger.info(f"   - Selected '{step['value']}' from dropdown.")

                except Exception:
                    logger.error(f"   - Option '{step['value']}' did not appear in the list!")
                    raise
            else:
                # Standard input (Full Name, Address, etc.)
                field_element.clear()
                field_element.send_keys(step['value'])

            time.sleep(delay)

            # 2. CLICK ADD
            add_btn = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, add_button_xpath)))
            # JS click is safer if the 'Add' button is near the bottom of the screen
            driver.execute_script("arguments[0].click();", add_btn)
            time.sleep(delay)
            # 3. ASSERTION
            if i < len(billing_fields) - 1:
                # Check that error is still visible
                WebDriverWait(driver, 8).until(ec.visibility_of_element_located((By.XPATH, error_msg_xpath)))
                logger.info(f"[SUCCESS] Error persists after entering: {step['name']}.")
            else:
                # Final field: Error should disappear
                WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.XPATH, error_msg_xpath)))
                logger.info("[SUCCESS] Form valid, user fields error cleared.")

    except Exception as e:
        logger.error(f"[CRITICAL] Error at Step {i + 1} ({step['name']}): {str(e)}")
        assert False
