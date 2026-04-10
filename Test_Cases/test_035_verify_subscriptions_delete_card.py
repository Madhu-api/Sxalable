from utils.verif_utils import *


def test_subscriptions_delete_card(driver, config):
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

    # Verify No. of cards is 2 initially
    logger.info("[STEP] Verify No. of cards is 2 initially...")
    no_of_cards_xpath = "//p[contains(., '**** **** **** ') and string-length(substring-after(., '**** **** **** ')) = 4]"
    card_elements = driver.find_elements(By.XPATH, no_of_cards_xpath)
    count = len(card_elements)
    assert count == 2, "Number of cards is not 2 initially"
    logger.info("[SUCCESS] Verified No. of cards is 2 initially...")

    # Verify 3 dots button clickable
    logger.info("[STEP] Verify Payment method 3 dots clickable...")
    three_dots_button_xpath = "//p[text()='Payment Method']/following-sibling::button"
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

    # Locate and click '...' button for alternative card
    alternative_card_suffix = alternative_card_number[-4:]
    logger.info("[STEP] Locate and click '...' button for alternative card")
    edit_button_xpath = f"//div[p[contains(., '{alternative_card_suffix}')]]/following-sibling::button"
    edit_button = locate_element(driver, (By.XPATH, edit_button_xpath), click_element=True)
    assert edit_button, f"for {alternative_card_number} '...' button not located and clicked"
    logger.info(f"[SUCCESS] for {alternative_card_number} '...' button located and clicked")
    time.sleep(delay)

    # Verify Delete button is present, enabled and clickable
    logger.info("[STEP] Verify Delete button is present, clickable")
    delete_xpath = "//li[text()='Delete']"
    delete_button = locate_element(driver, (By.XPATH, delete_xpath), click_element=True)
    assert delete_button, f"for {alternative_card_number} Delete button not located and clicked"
    logger.info(f"[SUCCESS] for {alternative_card_number} Delete button located and clicked")
    time.sleep(delay)

    # Locate 'Delete card' title
    logger.info("[STEP] Locating 'Delete Card' Text")
    text_found = verify_text_on_page(driver, 'Delete Card', timeout=15)
    assert text_found, "'Delete Card' was NOT displayed in the dialog as expected"
    logger.info("[SUCCESS] 'Delete Card' was displayed in the dialog as expected")

    # locating and clicking Yes, Delete button
    result = locate_element(driver, (By.XPATH, "//button[@type='button' and normalize-space()='Yes, Delete']"),
                            click_element=True)
    assert result is not None, "Delete Confirmation button failed to click"
    logger.info(f"[SUCCESS] Delete confirmation  button clicked...")

    time.sleep(5)

    logger.info("[STEP] Clicking on the arrow back button")
    arrow_back_button_xpath = "//*[local-name()='svg' and @data-testid='ArrowBackIcon']"
    arrow_back_button = locate_element(driver, (By.XPATH, arrow_back_button_xpath), click_element=True)
    assert arrow_back_button, f"Arrow back button not located/clicked"
    logger.info(f"[SUCCESS] Arrow back button not located/clicked")
    time.sleep(3)

    # Verify deleted card is no longer present
    logger.info("[STEP] Verify No. of cards is now 1...")

    card_elements = driver.find_elements(By.XPATH, no_of_cards_xpath)
    count = len(card_elements)
    assert count == 1, "Verified No. of cards is 1 after deleting"
    logger.info("[SUCCESS] Verified No. of cards is 1 after deleting...")

    # Verify default card is present

    logger.info(f"[STEP] Verify card is correctly displayed as 'default'...")
    default_card_suffix = valid_card_number[-4:]
    default_card_xpath = f"//div[p[contains(., '{default_card_suffix}')]]/following-sibling::div//p[text()='Default']"
    default_card = locate_element(driver, (By.XPATH, default_card_xpath), click_element=False)
    assert default_card, f"{valid_card_number} is NOT marked default"
    logger.info(f"[SUCCESS] {valid_card_number} is marked default")
    time.sleep(delay)
