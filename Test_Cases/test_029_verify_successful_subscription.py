from utils.verif_utils import *


def test_signin_successful_subscription(driver, config):
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
    expected_welcome_msg_text = config["app"]["expected_welcome_msg_text"]
    db_config = config["db"]
    ssh_config = config["ssh"]

    # user_details
    full_name = config["user"]["user_details"]["full_name"]
    address_line1 = config["user"]["user_details"]["address_line1"]
    country = config["user"]["user_details"]["country"]
    state = config["user"]["user_details"]["state"]
    city = config["user"]["user_details"]["city"]
    pincode = config["user"]["user_details"]["pincode"]
    # card_details
    name_on_card = config["user"]["card_details"]["name_on_card"]
    valid_card_number = config["user"]["card_details"]["valid_card_number"]
    valid_expiry = config["user"]["card_details"]["valid_expiry"]
    cvc = config["user"]["card_details"]["cvc"]

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

    card_fields = [
        {"name": "name_on_card", "xpath": "//input[@name='nameOnCard']", "value": name_on_card,
         },
        {"name": "valid_card_number", "xpath": "//input[@id='cardnumber']", "value": valid_card_number,
         "iframe_xpath": "//iframe[contains(@id, 'card-number')]"},
        {"name": "valid_expiry", "xpath": "//input[@id='exp-date']", "value": valid_expiry,
         "iframe_xpath": "//iframe[contains(@id, 'card-expiry')]"},
        {"name": "CVC", "xpath": "//input[@id='cvc']", "value": cvc,
         "iframe_xpath": "//iframe[contains(@id, 'card-cvv')]"}
    ]

    add_button_xpath = "//button[normalize-space()='Add']"

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Sign In
    logger.info(f"[STEP] Signing in...")
    sign_in_status = verify_successful_signin(driver, workspace, email, pwd, db_config, ssh_config)
    assert sign_in_status, "Sign in NOT successful ❌"
    logger.info(f"[SUCCESS] Sign in is successful ✅")

    #  Verify 'continue to plans' button enabled
    logger.info("[STEP] Verifying Continue Button is enabled (assuming user details previously entered)...")
    xpath = "//button[contains(., 'Continue to plans')]"
    continue_button = driver.find_element(By.XPATH, xpath)
    assert continue_button.is_enabled(), "Continue Button should be enabled, but not enabled"
    logger.info(f"[SUCCESS] Continue Button is enabled after entering user details ✅")
    logger.info(f"[STEP] Clicking 'Continue to Plans' button...")
    time.sleep(delay)
    continue_button.click()
    logger.info(f"[SUCCESS] Clicked 'Continue to Plans' button...")

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
    time.sleep(delay)

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

                except Exception as e:
                    logger.error(f"- Option '{step['value']}' did not appear in the list!: {str(e)}")
                    assert False
            else:
                # Standard input (Full Name, Address, etc.)
                field_element.clear()
                field_element.send_keys(step['value'])

            time.sleep(delay)
        logger.info("[SUCCESS] User Details Entered!")

    except Exception as e:
        logger.error(f"[CRITICAL] Error in entering user details: {str(e)}")
        assert False

    logger.info("[STEP] Entering Card Details into the form...")
    try:
        for i, step in enumerate(card_fields):
            try:
                logger.info(f"[STEP] Step {i + 1}: Entering {step['name']} ({step['value']})...")
                # 1. SWITCH TO IFRAME
                if "iframe_xpath" in step:
                    iframe = WebDriverWait(driver, 10).until(
                        ec.presence_of_element_located((By.XPATH, step['iframe_xpath']))
                    )
                    driver.switch_to.frame(iframe)
                    logger.info(f"   - Switched to iframe for {step['name']}")
                # 2. FIND AND FILL FIELD
                field_element = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, step['xpath']))
                )

                # Force the element to the center of the modal view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field_element)
                time.sleep(0.5)  # Wait for the scroll animation to finish

                field_element.clear()
                field_element.send_keys(step['value'])

                # 3. SWITCH BACK TO MAIN PAGE (Only if we were in an iframe)
                if "iframe_xpath" in step:
                    driver.switch_to.default_content()
                time.sleep(delay)

            except Exception as e:
                logger.error(f"[CRITICAL] Error at Step {i + 1} ({step['name']}): {str(e)}")
                assert False

            # 2. CLICK ADD
        logger.info(f"[SUCCESS] Card details entered, clicking Add button...")
        add_btn = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, add_button_xpath)))
        # JS click is safer if the 'Add' button is near the bottom of the screen
        driver.execute_script("arguments[0].click();", add_btn)
        time.sleep(delay)

    except Exception as e:
        logger.error(f"[ERROR]:Failure in entering card details: {str(e)}")
        assert False

    logger.info(f"[STEP] Verifying msg {expected_welcome_msg_text}...")
    text_found = verify_text_on_page(driver, expected_welcome_msg_text, timeout=15)
    assert text_found, f"{expected_welcome_msg_text} was NOT displayed in the page as expected"
    logger.info(f"[SUCCESS] '{expected_welcome_msg_text}' found on page ✅")
    time.sleep(delay)

