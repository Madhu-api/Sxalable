from utils.verif_utils import *
from utils.random_email_and_workspace_generator import *


def test_resend_enabled_after_60sec(driver, config):
    url = config["app"]["url"]
    expected_signup_text = config["app"]["expected_signup_text"]
    email = generate_unique_email(config["app"]["email"])
    pwd = config["app"]["pwd"]
    workspace = generate_unique_workspace_name(config["app"]["workspace"])

    expected_otp_page_url = "https://stage.sxalable.io/otp"
    delay = config["app"]["delay"]
    credentials = {"email": email, "password": pwd, "workspace name": workspace}
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
    assert url_contains, f"Failed to redirect to OTP Page, Current URL: {driver.current_url}"

    resend_button = locate_element(driver, (By.XPATH, "//*[contains(text(),'Resend')]"),
                                 )
    assert resend_button is not None, "Failed to locate Resend button"

    # waiting 5 sec for first OTP shared msg to disappear
    logger.info("waiting for the first OTP shared msg to disappear")
    time.sleep(5)
    try:
        logger.info("[STEP] Starting resend OTP timing validation")
        timeout = 90
        start = time.time()
        count = 0
        time.sleep(1)
        while count == 0:

            if time.time() - start > timeout:
                raise Exception("Timeout waiting for resend OTP")

            resend_btn = driver.find_element(By.XPATH, "//div[starts-with(normalize-space(),'Resend Code')]")

            try:
                resend_btn.click()
                logger.info("[DEBUG] Click attempted")

                # ✅ wait for message (short wait)
                WebDriverWait(driver, 3, poll_frequency=1).until(
                    ec.presence_of_element_located(
                        (By.XPATH, "//*[contains(text(),'OTP is shared')]")
                    )
                )

                logger.info("[SUCCESS] OTP resend success message detected")
                count = 1

            except Exception:
                logger.info("Inside exception block")
                count = 0

            time.sleep(delay)

        end = time.time()
        total_time = int(end - start)

        logger.info(f"[INFO] Time taken ~= {total_time} sec")

        # considering 5 sec delay we allowed earlier
        assert total_time >= 55, f"Resend worked too early ❌ | {total_time} sec"

        logger.info(f"[SUCCESS] Resend OTP worked after expected delay {total_time + 5} (>=60 sec) ✅")

    except Exception as e:
        logger.error("[ERROR] Resend OTP timing validation failed ❌")
        logger.error(str(e))
        assert False, f"Resend OTP test failed: {str(e)}"
