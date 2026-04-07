from utils.verif_utils import *
from utils.random_email_and_workspace_generator import *


def test_forgot_pwd_validations(driver, config):
    # validating that an invalid email for the workspace is not accepted
    # validating pwd format for change pwd
    url = config["app"]["url"]
    base_dir = os.getcwd()  # project root
    delay = config["app"]["delay"]
    file_path = os.path.join(base_dir, "input_variables", "test_signin_credentials.json")
    with open(file_path) as f:
        data = json.load(f)
    workspace = data["workspace"]
    email = generate_unique_email(config["app"]["email"])  # invalid email for the given workspace
    expected_signin_page_url = "https://stage.sxalable.io/login"
    expected_fp_page_url = "https://stage.sxalable.io/forgotpassword"
    expected_otp_page_text = config["app"]["expected_otp_page_text"]
    invalid_list = config["app"]["invalid_password_list"]
    expected_password_invalid_text = config["app"]["expected_password_invalid_text"]
    xpath = "//div[@role='alert']//div[normalize-space()='User not found. Please check your email.']"
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

    # Entering an invalid Email
    logger.info(f"[STEP] Entering an invalid Email for the given workspace: {email}...")
    enter_email_button.send_keys(email)
    logger.info(f"[SUCCESS] (Invalid) Email entered")
    time.sleep(delay)

    # Clicking Generate Login code button
    logger.info(f"[STEP] Clicking Generate Login code button...")
    generate_login_code_button = locate_element(driver, (
        By.XPATH, "//button[@type='submit' and normalize-space()='Generate Login code']"),
                                                click_element=True)
    assert generate_login_code_button is not None, "Failure in clicking Generate Login code button"
    time.sleep(delay)

    # Verifying 'User not found' error msg
    logger.info(f"[STEP] Verifying 'User not found' error msg...")

    user_not_found_error = locate_element(driver, (By.XPATH, xpath), click_element=True)
    assert user_not_found_error is not None, "Failure in locating User not found error"
    logger.info(f"[SUCCESS] User Not Found error populated as expected")

    # Entering valid email

    logger.info(f"[STEP]Entering valid email...")
    email = data["email"]  # valid email
    credentials = {"email": email}
    form_success = enter_form_data(driver, credentials, delay=2)
    assert form_success, "Form entry failed. Check the logs to see which field was missing."
    logger.info(f"[SUCCESS] Entered email")

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

    # Entering & validating invalid New password, invalid Confirm password

    logger.info(f"[STEP] Entering invalid New password, invalid Confirm password")
    time.sleep(delay)

    for password in invalid_list:

        try:
            logger.info(f"[STEP] Validating password error message for input: {password}")
            logger.info(f"[STEP] Entering new password: {password}")
            new_password = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located(
                    (By.XPATH, "(//input[contains(@placeholder,'Enter your password')])[1]")
                )
            )
            new_password.click()
            new_password.send_keys(Keys.CONTROL + "a")
            new_password.send_keys(Keys.DELETE)
            new_password.send_keys(password)
            logger.info(f"[STEP] Entered new password: {password}")

            logger.info(f"[STEP] Entering confirm password: {password}")
            confirm_password = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located(
                    (By.XPATH, "(//input[contains(@placeholder,'Enter your password')])[2]")
                )
            )
            confirm_password.click()
            confirm_password.send_keys(Keys.CONTROL + "a")
            confirm_password.send_keys(Keys.DELETE)
            confirm_password.send_keys(password)
            logger.info(f"[STEP] Entered confirm password: {password}")

            logger.info(f"[STEP] Clicking Change Password button...")

            cp_btn = locate_element(driver,
                                    (By.XPATH, "//button[@type='submit' and normalize-space()='Change Password']"),
                                    click_element=True)
            assert cp_btn is not None, "Failure in clicking Change Password button"
            time.sleep(delay)
            logger.info(f"[SUCCESS] Change Password button clicked...")
            time.sleep(1)

            logger.info(f"[STEP] Waiting for password validation error...")

            xpath1 = "(//span[contains(@class, '_error_message') and contains(., 'Invalid password')])[1]"
            xpath2 = "(//span[contains(@class, '_error_message') and contains(., 'Invalid password')])[2]"

            xpath_list = [xpath1, xpath2]

            for xpath in xpath_list:
                invalid_pwd = locate_element(driver, (By.XPATH, xpath))
                assert invalid_pwd is not None, "] Expected error message for invalid Pwd input not found on the page"
                logger.info(f"[SUCCESS] '{expected_password_invalid_text}' found on page for both pwds✅")
            new_password.clear()
            confirm_password.clear()

        except Exception as e:
            logger.error("[ERROR] Failure in entering pwd or locating invalid pwd input error ❌")
            logger.error(str(e))
            assert False, f"Password invalid validation failed: {str(e)}"
