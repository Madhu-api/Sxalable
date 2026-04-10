from utils.verif_utils import *


def test_subscriptions_add_new_card(driver, config):
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
    # card_details
    name_on_card = config["user"]["card_details"]["name_on_card"]
    valid_card_number = config["user"]["card_details"]["alternative_card_number"]
    valid_expiry = config["user"]["card_details"]["valid_expiry"]
    cvc = config["user"]["card_details"]["cvc"]
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
    time.sleep(delay)
    # Sign In
    logger.info(f"[STEP] Signing in...")
    sign_in_status = verify_successful_signin(driver, workspace, email, pwd, db_config, ssh_config)
    assert sign_in_status, "Sign in NOT successful ❌"
    logger.info(f"[SUCCESS] Sign in is successful ✅")
    time.sleep(delay)

    # Navigating to Administration page

    navigate_to_tab(driver, 'Administration')
    time.sleep(delay)

    # Navigating to Subscription page
    navigate_to_tab(driver, 'Subscriptions')
    time.sleep(delay)

    three_dots_button_xpath = "//p[text()='Payment Method']/following-sibling::button"

    # Verify 3 dots button clickable
    click_status = is_button_clickable(driver, three_dots_button_xpath)
    assert click_status, "Payment method 3 dots not clickable"
    logger.info("[SUCCESS] Payment method 3 dots clickable")
    time.sleep(delay)

    # Click 3 dots button
    three_dots_button = locate_element(driver, (By.XPATH, three_dots_button_xpath), click_element=True)
    assert three_dots_button, "Payment method 3 dots not clicked"
    logger.info("[SUCCESS] Payment method 3 dots clicked")
    time.sleep(delay)

    # Clicking Add card
    add_card_xpath = "//li[contains(., 'Add Card')]"
    add_card = locate_element(driver, (By.XPATH, add_card_xpath), click_element=True)
    assert add_card, "Add card button not clicked"
    logger.info("[SUCCESS] Add card button clicked")
    time.sleep(delay)

    # Locating Add payment method Text
    logger.info("[STEP] Locating Add payment method Text")
    text_found = verify_text_on_page(driver, 'Add Payment Method', timeout=15)
    assert text_found, "'Add Payment Method' was NOT displayed in the page as expected"
    logger.info("[SUCCESS] 'Add Payment Method' was displayed in the page as expected")

    # Entering card Details into the form
    logger.info(f"[STEP] Entering card Details into the form...")

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

    time.sleep(15)
    # Verify new card on the page
    logger.info(f"[STEP] Verify new card on the page...")

    logger.info("[STEP] Verify Card details is correct")
    card_xpath = "(//p[contains(@class, 'MuiTypography-root') and contains(., '****')])[2]"
    actual_card_number = get_text_from_xpath(driver, card_xpath)
    assert actual_card_number.startswith("**** **** ****"), f"Card is not masked correctly! Found: {actual_card_number}"
    logger.info(f"[SUCCESS] card number masked as expected: {actual_card_number[:-5]}")
    expected_suffix = valid_card_number[-4:]
    actual_suffix = actual_card_number[-4:]
    assert actual_suffix == expected_suffix, f"expected: {expected_suffix}, but received: {actual_suffix}"
    logger.info(f"[SUCCESS] expected card suffix: {expected_suffix}, received card suffix: {actual_suffix}")
    time.sleep(delay)
