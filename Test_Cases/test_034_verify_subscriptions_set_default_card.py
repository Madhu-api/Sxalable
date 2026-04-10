from utils.verif_utils import *


def test_subscriptions_set_default_card(driver, config):
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

    valid_card_number = config["user"]["card_details"]["valid_card_number"]
    alternative_card_number = config["user"]["card_details"]["alternative_card_number"]

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
    logger.info("[STEP] Verify Payment method 3 dots clickable...")
    click_status = is_button_clickable(driver, three_dots_button_xpath)
    assert click_status, "Payment method 3 dots not clickable"
    logger.info("[SUCCESS] Payment method 3 dots clickable")
    time.sleep(delay)

    # Click 3 dots button
    logger.info("[STEP] Clicking Payment method 3 dots button...")
    three_dots_button = locate_element(driver, (By.XPATH, three_dots_button_xpath), click_element=True)
    assert three_dots_button, "Payment method 3 dots not clicked"
    logger.info("[SUCCESS] Payment method 3 dots clicked")
    time.sleep(delay)

    # Click 'Manage Cards' button
    logger.info("[STEP] Clicking Manage cards button...")
    manage_card_xpath = "//li[contains(., 'Manage Cards')]"
    manage_card = locate_element(driver, (By.XPATH, manage_card_xpath), click_element=True)
    assert manage_card, "Manage cards button not clicked"
    logger.info("[SUCCESS] Manage cards button clicked")
    time.sleep(delay)

    # Locating 'Manage Payment Methods' Text
    logger.info("[STEP] Locating 'Manage Payment Methods' Text")
    text_found = verify_text_on_page(driver, 'Manage Payment Methods', timeout=15)
    assert text_found, "'Manage Payment Methods' was NOT displayed in the page as expected"
    logger.info("[SUCCESS] 'Manage Payment Methods' was displayed in the page as expected")

    logger.info(f"[STEP] Verify card is correctly displayed as 'default'...")
    default_card_suffix = valid_card_number[-4:]
    default_card_xpath = f"//div[p[contains(., '{default_card_suffix}')]]/following-sibling::div//p[text()='Default']"
    default_card = locate_element(driver, (By.XPATH, default_card_xpath), click_element=False)
    assert default_card, f"{valid_card_number} is NOT marked default"
    logger.info(f"[SUCCESS] {valid_card_number} is marked default")
    time.sleep(delay)

    # Verify '...' button is disabled for default card
    logger.info("[STEP] Verify '...' button is disabled for default card")
    edit_button_xpath = f"//div[p[contains(., '{default_card_suffix}')]]/following-sibling::div[p[text(" \
                        f")='Default']]/following-sibling::button"
    edit_button = locate_element(driver, (By.XPATH, edit_button_xpath), click_element=False)
    assert edit_button, f"for {valid_card_number} '...' button not located"
    logger.info(f"for {valid_card_number} '...' button located")
    time.sleep(delay)

    assert not verify_button_enabled_by_xpath(driver, edit_button_xpath), "'...' Button should be disabled, but not " \
                                                                          "disabled"
    logger.info(f"[SUCCESS] '...' Button is disabled for the default card: {valid_card_number} ✅")

    # Verify 3 dots button not clickable for default card
    logger.info("[STEP] Verify '...' button is not clickable for default card")
    click_status = is_button_clickable(driver, edit_button_xpath)
    assert not click_status, "'...' button clickable"
    logger.info("[SUCCESS] '...' button not clickable as expected")
    time.sleep(delay)

    # Locate and click '...' button for alternative card
    alternative_card_suffix = alternative_card_number[-4:]
    logger.info("[STEP] Locate and click '...' button for alternative card")
    edit_button_xpath = f"//div[p[contains(., '{alternative_card_suffix}')]]/following-sibling::button"
    edit_button = locate_element(driver, (By.XPATH, edit_button_xpath), click_element=True)
    assert edit_button, f"for {alternative_card_number} '...' button not located and clicked"
    logger.info(f"[SUCCESS] for {alternative_card_number} '...' button located and clicked")
    time.sleep(delay)

    # Verify Make as Default is present, enabled and clickable
    logger.info("[STEP] Verify Make as Default is present, clickable")

    make_as_default_xpath = "//li[text()='Make as default']"
    make_as_default_button = locate_element(driver, (By.XPATH, make_as_default_xpath), click_element=True)
    assert make_as_default_button, f"for {alternative_card_number} Make as default button not located and clicked"
    logger.info(f"[SUCCESS] for {alternative_card_number} Make as default button located and clicked")
    time.sleep(6)

    # Verify Alternative card now becomes default
    logger.info("[STEP] Verify Alternative card now becomes default")

    default_card_xpath = f"//div[p[contains(., '{alternative_card_suffix}')]]/following-sibling::div//p[text(" \
                         f")='Default']"
    default_card = locate_element(driver, (By.XPATH, default_card_xpath), click_element=False)
    assert default_card, f"{alternative_card_number} is NOT marked default"
    logger.info(f"[SUCCESS] {alternative_card_number} is Now marked default")
    time.sleep(delay)

    # Verify original card not marked default
    logger.info("[STEP] Verify original card not marked default")
    default_card_xpath = f"//div[p[contains(., '{default_card_suffix}')]]/following-sibling::div//p[text(" \
                         f")='Default']"
    is_absent = verify_element_absent(driver, (By.XPATH, default_card_xpath))
    assert is_absent, "Original card still marked default"
    logger.info("[SUCCESS] Original card not marked default as expected")
    time.sleep(delay)

    # Make original card default again, (for cleanup purposes)
    logger.info("[STEP] Clean up --restoring to original card configuration")
    # Locate and click '...' button for original card

    logger.info("[STEP] Locate and click '...' button for original card")
    edit_button_xpath = f"//div[p[contains(., '{default_card_suffix}')]]/following-sibling::button"
    edit_button = locate_element(driver, (By.XPATH, edit_button_xpath), click_element=True)
    assert edit_button, f"for {valid_card_number} '...' button not located and clicked"
    logger.info(f"[SUCCESS] for {valid_card_number} '...' button located and clicked")
    time.sleep(delay)

    # Verify Make as Default is present, enabled and clickable
    logger.info("[STEP] Verify Make as Default is present, clickable")

    make_as_default_button = locate_element(driver, (By.XPATH, make_as_default_xpath), click_element=True)
    assert make_as_default_button, f"for {valid_card_number} Make as default button not located and clicked"
    logger.info(f"[SUCCESS] for {valid_card_number} Make as default button located and clicked")
    time.sleep(6)

    # Verify original card now becomes default
    logger.info("[STEP] Verify Original card now becomes default")

    default_card_xpath = f"//div[p[contains(., '{default_card_suffix}')]]/following-sibling::div//p[text(" \
                         f")='Default']"
    default_card = locate_element(driver, (By.XPATH, default_card_xpath), click_element=False)
    assert default_card, f"{valid_card_number} is NOT marked default"
    logger.info(f"[SUCCESS] {valid_card_number} is Now marked default")
    time.sleep(delay)
