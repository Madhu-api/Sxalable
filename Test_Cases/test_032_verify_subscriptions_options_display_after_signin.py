from utils.verif_utils import *


def test_subscriptions_options_display_after_signin(driver, config):
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
    valid_card_number = config["user"]["card_details"]["valid_card_number"]

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

    # Validating current plan, trial period!
    logger.info("[STEP] Validating current plan, trial period!")
    text_to_verify = ['Current Plan', 'Trial Period', 'Business Plan']
    for text in text_to_verify:
        text_xpath = f"//p[contains(@class, 'MuiTypography-root') and text()='{text}']"
        text_located = locate_element(driver, (By.XPATH, text_xpath),
                                      click_element=False)
        assert text_located is not None, f"Text {text} failed to verify"
        logger.info(f"[SUCCESS] {text} is verified in the page correctly")
        time.sleep(delay)
    logger.info("[SUCCESS] Validated current plan, trial period!")

    # Verify Manage Subscription is enabled/clickable
    logger.info("[STEP] Verify Manage Subscription is enabled/clickable")
    manage_sub_xpath = "//button[@type='button' and text()='Manage Subscription']"
    click_status = is_button_clickable(driver, manage_sub_xpath)
    assert click_status, "Manage Subscription button not found/disabled/not clickable"
    logger.info("[SUCCESS] Verified Manage Subscription is enabled/clickable")
    time.sleep(delay)

    # Verify SxR and xWAN count is zero initially
    logger.info("[STEP] Verify SxR and xWAN count is zero initially")
    SxR_count_xpath = "//p[text()='SxR Routers']/preceding-sibling::p"
    xWAN_count_xpath = "//p[text()='xWANs']/preceding-sibling::p"
    SxR_count = get_text_from_xpath(driver, SxR_count_xpath)
    xWAN_count = get_text_from_xpath(driver, xWAN_count_xpath)
    assert SxR_count == '0', f"SxR  count is NOT zero initially, received: {SxR_count}"
    logger.info(f"[SUCCESS] Verified SxR count is zero initially, received: {SxR_count}")
    assert xWAN_count == '0', f"xWAN  count is NOT zero initially, received: {xWAN_count}"
    logger.info(f"[SUCCESS] Verified xWAN count is zero initially, received: {xWAN_count}")
    time.sleep(delay)

    # Verify Card details is correct
    logger.info("[STEP] Verify Card details is correct")
    card_xpath = "//p[contains(@class, 'MuiTypography-root') and contains(., '****')]"
    actual_card_number = get_text_from_xpath(driver, card_xpath)
    assert actual_card_number.startswith("**** **** ****"), f"Card is not masked correctly! Found: {actual_card_number}"
    logger.info(f"[SUCCESS] card number masked as expected: {actual_card_number[:-5]}")
    expected_suffix = valid_card_number[-4:]
    actual_suffix = actual_card_number[-4:]
    assert actual_suffix == expected_suffix, f"expected: {expected_suffix}, but received: {actual_suffix}"
    logger.info(f"[SUCCESS] expected card suffix: {expected_suffix}, received card suffix: {actual_suffix}")
    time.sleep(delay)

    # Verify No Billing History initially
    logger.info("[STEP] Verify No Billing History initially, (trial period + no SxRs)")
    no_rows_xpath = "//p[text()='Billing History']/following-sibling::div//span[text()='No Rows To Show']"
    no_rows_located = locate_element(driver, (By.XPATH, no_rows_xpath),
                                     click_element=False)
    assert no_rows_located is not None, "failed to verify, expected no rows in billing history"
    logger.info(f"[SUCCESS] verified as expected, no rows in billing history")
    time.sleep(delay)
