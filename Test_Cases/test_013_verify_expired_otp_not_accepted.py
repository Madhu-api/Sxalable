from utils.verif_utils import *
from utils.random_email_and_workspace_generator import *


def test_expired_otp_functionality(driver, config):
    url = config["app"]["url"]
    expected_signup_text = config["app"]["expected_signup_text"]
    email = generate_unique_email(config["app"]["email"])
    pwd = config["app"]["pwd"]
    workspace = generate_unique_workspace_name(config["app"]["workspace"])
    expected_otp_page_url = "https://stage.sxalable.io/otp"
    delay = config["app"]["delay"]
    credentials = {"email": email, "password": pwd, "workspace name": workspace}
    db_config = config["db"]
    ssh_config = config["ssh"]

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Locating/clicking Sign up button
    sign_up_element = locate_element(driver, (By.PARTIAL_LINK_TEXT, 'Sign up'), click_element=True)
    assert sign_up_element is not None, "Sign up button failed to click"

    # Locating Sign up Text
    text_found = verify_text_on_page(driver, expected_signup_text, timeout=15)
    assert text_found, f"{expected_signup_text} was NOT displayed in the sign up page as expected"

    logger.info(f"[STEP] Entering email, password and workspace name")
    form_success = enter_form_data(driver, credentials, delay=2)

    assert form_success, "Form entry failed. Check the logs to see which field was missing."
    logger.info(f"[STEP] Entered email, password and workspace name")

    current_url = driver.current_url
    logger.info(f"[STEP] Clicking Next button...")

    next_button = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Next']"),
                                 click_element=True)
    assert next_button is not None, "Next button failed to click"

    # Verify URL changed
    url_navigated = verify_url_change(driver, current_url)
    assert url_navigated, f"Navigation timed out! Still stuck on {current_url}"

    # Verify OTP page URL
    url_contains = verify_url_contains(driver, expected_otp_page_url)
    assert url_contains, f"Failed to redirect to OTP Page. Current URL: {driver.current_url}"

    # Fetching OTP from DB
    logger.info("[STEP] Fetching OTP from DB...")

    otp = get_otp_from_db(db_config, ssh_config, email)
    assert otp, f"OTP fetch failed for {email}. Check logs for DB/SSH tunnel issues."
    logger.info(f"[SUCCESS] OTP fetched: {otp} ✅")

    current_url = driver.current_url
    logger.info("[STEP] Waiting for 5 min for the OTP to expire..")
    time.sleep(305)

    logger.info("[STEP] Entering OTP...")
    otp_status = enter_otp(driver, otp)
    assert otp_status, "Failed to enter OTP into the input fields."
    logger.info("[STEP] Entered OTP")

    # Clicking Verify button
    verify_button = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Verify']"),
                                   click_element=True)

    assert verify_button is not None, "Verify button failed to click"

    # verify invalid OTP is rejected
    logger.info("[STEP] Verify Entered invalid OTP msg")
    logger.info("[STEP] Waiting for Expired OTP msg..")

    expired_otp_msg = locate_element(driver, (By.XPATH, "//div[@role='alert']//div[normalize-space()='OTP expired']")
                                     )
    assert expired_otp_msg is not None, "Invalid OTP msg not found"

    logger.info("[SUCCESS] 'OTP expired' error populated as expected! Test Passed")
    time.sleep(delay)

    # verify current url does not change after error
    logger.info("[STEP] Verify current url does not change..")
    url_navigated = verify_url_change(driver, current_url)
    assert not url_navigated, f"URL changed! (Not expected): {current_url}"

    logger.info(f"[SUCCESS] Verified: User stayed on the same page {current_url} as expected. ✅")
