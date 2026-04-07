from utils.verif_utils import *

# Note: Failed due to https://sxalable.atlassian.net/browse/VLS-2809


def test_forgot_pwd_functionality(driver, config):
    url = config["app"]["url"]
    base_dir = os.getcwd()  # project root
    delay = config["app"]["delay"]
    file_path = os.path.join(base_dir, "input_variables", "test_signin_credentials.json")
    with open(file_path) as f:
        data = json.load(f)
    workspace = data["workspace"]
    email = data["email"]
    expected_otp_page_text = config["app"]["expected_otp_page_text"]
    changed_pwd = config["app"]["change_pwd"]
    expected_fp_page_url = "https://stage.sxalable.io/forgotpassword"
    expected_home_page_url = "https://stage.sxalable.io/"
    expected_signin_page_url = "https://stage.sxalable.io/login"
    db_config = config["db"]
    ssh_config = config["ssh"]

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."

    # Locating workspace element
    workspace_input = locate_element(driver, (By.XPATH, "//input[contains(@placeholder,'Workspace')]"),
                                     click_element=True)
    assert workspace_input is not None, "Workspace element not found!"
    time.sleep(delay)

    # Entering workspace name
    workspace_input.send_keys(workspace)
    logger.info(f"[INFO] Workspace entered: {workspace}")
    time.sleep(delay)

    # locating and clicking Next button
    result = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Next']"),
                            click_element=True)
    assert result is not None, "Next button failed to click"
    logger.info(f"[SUCCESS] Next button clicked...")

    time.sleep(delay)

    # Checking Sign in page URL
    logger.info(f"[STEP] Checking Sign in page URL...")
    url_contains = verify_url_contains(driver, expected_signin_page_url)
    assert url_contains, f"Failed to redirect to Sign in Page. Current URL: {driver.current_url}"
    logger.info(f"[STEP] Checked Sign in page URL...")

    # Locating 'Forgot Password' option
    logger.info(f"[STEP] Locating 'Forgot Password' option...")
    forgot_password = locate_element(driver, (By.XPATH, "//h5[contains(normalize-space(),'Forgot Password?')]"))
    assert forgot_password is not None, "Forgot Password Failed to locate"
    logger.info(f"[SUCCESS] Forgot Password button located...")

    # Clicking Forgot Password 'Click Here' button
    logger.info(f"[STEP] Clicking Forgot Password 'Click Here' button...")

    click_here = locate_element(driver, (By.XPATH, "//a[@href='/forgotpassword' and normalize-space()='Click Here']"),
                                click_element=True)
    assert click_here is not None, "Click Here button Failed to Click"
    logger.info(f"[SUCCESS] Click Here button located...")
    time.sleep(delay)

    # Checking Forgot Password page URL
    logger.info(f"[STEP] Checking Forgot password page URL...")
    url_contains = verify_url_contains(driver, expected_fp_page_url)
    assert url_contains, f"Failed to redirect to Forgot Password Page. Current URL: {driver.current_url}"
    logger.info(f"[STEP] Checked Forgot password page URL...")

    # Locating Enter Your email option
    logger.info(f"[STEP] Locating Enter Your email option...")
    time.sleep(delay)
    enter_email_button = locate_element(driver, (By.XPATH, "//input[@placeholder='Enter your email']"),
                                        click_element=True)
    assert enter_email_button is not None, "Failure in locating/clicking Enter Your email option"
    logger.info(f"[SUCCESS] Enter Your Email has been located/Clicked...")

    # Entering existing email
    logger.info(f"[STEP] Entering email...")
    enter_email_button.send_keys(email)
    logger.info(f"[SUCCESS] Email entered")
    time.sleep(delay)

    # Clicking Generate Login code button
    logger.info(f"[STEP] Clicking Generate Login code button...")
    generate_login_code_button = locate_element(driver, (
        By.XPATH, "//button[@type='submit' and normalize-space()='Generate Login code']"),
                                                click_element=True)
    assert generate_login_code_button is not None, "Failure in clicking Generate Login code button"
    time.sleep(delay)

    # Waiting for OTP page text
    logger.info(f"[STEP] Waiting for OTP page text...")
    text_found = verify_text_on_page(driver, expected_otp_page_text, timeout=15)
    assert text_found, f"{expected_otp_page_text} was NOT displayed in the page as expected"

    # Fetching OTP from DB
    logger.info("[STEP] Fetching OTP from DB...")

    otp = get_otp_from_db(db_config, ssh_config, email)
    assert otp, f"OTP fetch failed for {email}. Check logs for DB/SSH tunnel issues."
    logger.info(f"[SUCCESS] OTP fetched: {otp} ✅")
    time.sleep(delay)

    # Entering OTP
    logger.info("[STEP] Entering OTP...")
    otp_status = enter_otp(driver, otp)
    assert otp_status, "Failed to enter OTP into the input fields."
    logger.info("[STEP] Entered OTP")
    time.sleep(delay)

    # Clicking Verify button
    logger.info("[STEP] Clicking Verify button...")
    verify_btn = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Verify']"),
                                click_element=True)
    assert verify_btn is not None, "Failure in clicking Verify button"
    logger.info(f"[SUCCESS] Verify button clicked ✅")
    time.sleep(delay)

    # Locating Change Password option
    logger.info(f"[STEP] Locating Change Password option...")
    text_found = verify_text_on_page(driver, 'Change Password?', timeout=15)
    assert text_found, f"'Change Password?' was NOT displayed in the page as expected"
    logger.info(f"[SUCCESS] Change Password element located in page")
    time.sleep(delay)

    # Entering New password, Confirm password
    logger.info(f"[STEP] Entering New password, Confirm password")
    time.sleep(delay)
    logger.info(f"[STEP] Entering New Password: {changed_pwd}...")
    new_pwd_input = locate_element(driver, (By.XPATH, "(//input[contains(@placeholder,'Enter your password')])[1]"),
                                   click_element=True)
    assert new_pwd_input is not None, "Failure in entering input fields in Change Password"
    time.sleep(delay)
    new_pwd_input.send_keys(changed_pwd)

    time.sleep(delay)
    logger.info(f"[STEP] Entering Confirm Password: {changed_pwd}...")
    confirm_pwd_input = locate_element(driver, (By.XPATH, "(//input[contains(@placeholder,'Enter your password')])[2]"),
                                       click_element=True)
    assert confirm_pwd_input is not None, "Failure in entering input fields in Change Password"
    time.sleep(delay)
    confirm_pwd_input.send_keys(changed_pwd)
    time.sleep(delay)

    logger.info(f"[INFO] New pwd and Confirm pwd entered...")

    # Clicking Change Password button
    logger.info(f"[STEP] Clicking Change Password button...")
    cp_button = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Change Password']"),
                               click_element=True)
    assert cp_button is not None, "Failure in clicking Change Password button"
    logger.info(f"[SUCCESS] Change Password button clicked...")
    time.sleep(delay)

    # Locating 'Password Changed!' Text
    logger.info(f"[STEP] Locating 'Password Changed!' Text...")
    time.sleep(1)
    password_changed_input = locate_element(driver, (By.XPATH, "//h5[contains(normalize-space(),'Password Changed!')]"))
    assert password_changed_input is not None, "Failure in locating 'Password Changed!'Text in page"
    logger.info(f"[SUCCESS] 'Password Changed!' Text located in page")
    time.sleep(1)

    # Checking URL is redirected to home page after change pwd
    logger.info(f"[STEP] Checking URL is redirected to home page after change pwd...")
    logger.info(f"[STEP] Waiting for ~12 sec...")
    time.sleep(12)

    url_contains = verify_url_contains(driver, expected_home_page_url)
    assert url_contains, f"Failed to redirect to home Page. Current URL: {driver.current_url}"

    logger.info(f"[SUCCESS] Checked URL is correct after change pwd operation: {driver.current_url}")
