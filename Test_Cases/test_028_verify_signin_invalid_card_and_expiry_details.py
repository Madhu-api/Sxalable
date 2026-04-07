from utils.verif_utils import *
from utils.random_user_details_generator import *


# Fresh sign up required for this test-case
# Run test_011_verify_signup_functionality.py before this TC

def test_signin_invalid_card_expiry_details(driver, config):
    url = config["app"]["url"]
    base_dir = os.getcwd()  # project root
    file_path = os.path.join(base_dir, "input_variables", "test_signin_credentials.json")
    with open(file_path) as f:
        data = json.load(f)
    email = data["email"]
    workspace = data["workspace"]
    pwd = config["app"]["pwd"]
    delay = config["app"]["delay"]
    expected_available_plans_text = config["app"]["expected_available_plans_text"]
    expected_checkout_page_text = config["app"]["expected_checkout_page_text"]
    db_config = config["db"]
    ssh_config = config["ssh"]
    # generating unique name with username 'Automationuser' with only a-z characters
    first_name = generate_unique_first_name(config["user"]["first_name"])
    # generating unique name with username 'Automationcompany' with only a-z characters
    company_name = generate_unique_first_name(config["user"]["company_name"])
    # generating unique company address with only a-z characters
    company_address = generate_unique_first_name(config["user"]["company_address"])
    user_credentials = {"Enter your first name": first_name, "Enter your company name": company_name,
                        "Enter your company address": company_address}

    # card_details
    name_on_card = config["user"]["card_details"]["name_on_card"]
    invalid_card_number = config["user"]["card_details"]["invalid_card_number"]
    invalid_expiry = config["user"]["card_details"]["invalid_expiry"]
    cvc = config["user"]["card_details"]["cvc"]

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Sign In
    logger.info(f"[STEP] Signing in...")
    sign_in_status = verify_successful_signin(driver, workspace, email, pwd, db_config, ssh_config)
    assert sign_in_status, "Sign in NOT successful ❌"
    logger.info(f"[SUCCESS] Sign in is successful ✅")

    # Entering user details
    logger.info("[STEP] Entering user details..")
    time.sleep(delay)
    form_success = enter_form_data(driver, user_credentials, delay=2)

    assert form_success, "Form entry failed. Check the logs to see which field was missing."
    logger.info(f"[STEP] Entered User details successfully")

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

    logger.info("[STEP] Skipping user details and concentrating on card details for the test-case...")
    card_fields = [
        {"name": "name_on_card", "xpath": "//input[@name='nameOnCard']", "value": name_on_card,
         "check_invalid": False},
        {"name": "invalid_card_number", "xpath": "//input[@id='cardnumber']", "value": invalid_card_number,
         "iframe_xpath": "//iframe[contains(@id, 'card-number')]", "check_invalid": True},
        {"name": "invalid_expiry", "xpath": "//input[@id='exp-date']", "value": invalid_expiry,
         "iframe_xpath": "//iframe[contains(@id, 'card-expiry')]", "check_invalid": True},
        {"name": "CVC", "xpath": "//input[@id='cvc']", "value": cvc,
         "iframe_xpath": "//iframe[contains(@id, 'card-cvv')]", "check_invalid": False}
    ]

    logger.info(f"[STEP] Entering Card Details and verifying field states...")

    try:
        for i, step in enumerate(card_fields):
            logger.info(f"[STEP] Step {i + 1}: Processing {step['name']}: {step['value']}...")

            # 1. SWITCH TO IFRAME (if applicable)
            if "iframe_xpath" in step:
                iframe = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, step['iframe_xpath']))
                )
                driver.switch_to.frame(iframe)

            # 2. FIND AND FILL FIELD
            field_element = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, step['xpath']))
            )

            # Scroll and Clear
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field_element)
            field_element.clear()

            # Input value
            field_element.send_keys(step['value'])

            # Trigger validation: Most Chargebee/MUI fields validate on 'Blur' (losing focus)
            field_element.send_keys(Keys.TAB)
            time.sleep(1)  # Short wait for React to update the class to 'is-invalid'

            # 3. VERIFY 'IS-INVALID' (Only for specific fields)
            if step.get("check_invalid"):
                classes = field_element.get_attribute("class")
                if "is-invalid" in classes:
                    logger.info(f"[SUCCESS] Field '{step['name']}' turned RED (is-invalid class detected).")
                else:
                    logger.error(f"[FAIL] Field '{step['name']}' did NOT turn red. Classes found: {classes}")
                    # Optional: assert "is-invalid" in classes
            else:
                logger.info(f"   - Input entered for {step['name']} (Validation check skipped).")

            # 4. RETURN TO MAIN CONTEXT
            driver.switch_to.default_content()
            time.sleep(delay)

        logger.info("[COMPLETE] All card fields processed.")

    except Exception as e:
        driver.switch_to.default_content()  # Always switch back on error
        logger.error(f"[CRITICAL] Error at Step {i + 1} ({step['name']}): {str(e)}")
        assert False
