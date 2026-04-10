from utils.config_utils import *


def verify_text_on_page(driver, expected_text, timeout=10):
    """
    Waits for specific text to appear anywhere in the body of the page.
    Returns True if found, False otherwise.
    """
    try:
        logger.info(f"[STEP] Waiting for text: '{expected_text}'")

        WebDriverWait(driver, timeout).until(
            ec.text_to_be_present_in_element(
                (By.TAG_NAME, "body"),
                expected_text
            )
        )

        logger.info(f"[SUCCESS] Text '{expected_text}' found on page ✅")
        return True

    except Exception as e:
        logger.error(f"[ERROR] Failed to find text '{expected_text}' ❌")
        # Log a snippet of page source to help debug UI issues in CI/CD
        logger.debug(f"[DEBUG] Page Source Snippet: {driver.page_source[:500]}")
        logger.error(f"[EXCEPTION] {str(e)}")
        return False


def verify_url_change(driver, original_url, timeout=10):
    """
    Waits for the browser URL to change from the provided original_url.

    Args:
        driver: Selenium WebDriver instance.
        original_url (str): The URL you are moving away from.
        timeout (int): Seconds to wait for the change.

    Returns:
        bool: True if the URL changed within the timeout, False otherwise.
    """
    try:
        logger.info(f"[STEP] Waiting for URL to change from: {original_url}")

        # Lambda checks if current URL is different from the one we started with
        WebDriverWait(driver, timeout).until(
            lambda d: d.current_url != original_url
        )

        new_url = driver.current_url
        logger.info(f"[SUCCESS] URL changed to: {new_url} ✅")
        return True

    except TimeoutException:
        logger.error(f"[TIMEOUT] URL did not change from {original_url} within {timeout}s ❌")
        # Useful for debugging if a button click didn't trigger navigation
        logger.debug(f"[DEBUG] Final URL state: {driver.current_url}")
        return False
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error during URL verification: {str(e)}")
        return False


def verify_url_contains(driver, expected_partial_url, timeout=15):
    """
    Waits for the browser URL to contain a specific string.

    Args:
        driver: Selenium WebDriver instance.
        expected_partial_url (str): The string expected in the new URL (e.g., '/dashboard').
        timeout (int): Seconds to wait for the navigation to complete.

    Returns:
        bool: True if the URL contains the expected string, False otherwise.
    """
    try:
        logger.info(f"[STEP] Waiting for URL to contain: '{expected_partial_url}'")

        # This built-in EC is highly optimized for navigation
        WebDriverWait(driver, timeout).until(
            ec.url_contains(expected_partial_url)
        )

        current_url = driver.current_url
        logger.info(f"[SUCCESS] Reached target URL: {current_url} ✅")
        return True

    except TimeoutException:
        logger.error(f"[TIMEOUT] Did not reach URL containing '{expected_partial_url}' within {timeout}s ❌")
        logger.debug(f"[DEBUG] Actual URL at timeout: {driver.current_url}")
        return False
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error during URL verification: {str(e)}")
        return False


def verify_element_absent(driver, locator, timeout=5):
    """
    Verifies that an element is NOT present on the page.
    Returns True if absent, False if it exists.
    """
    try:
        # We wait for the element to disappear or stay absent
        WebDriverWait(driver, timeout).until_not(
            ec.presence_of_element_located(locator)
        )
        logger.info(f"[SUCCESS] element {locator} is absent")
        return True
    except TimeoutException:
        # If it's still there after the timeout, return False
        logger.error(f"[FAILURE] Element {locator} is still present after {timeout}s wait.")
        return False


def verify_button_enabled_by_xpath(driver, xpath, timeout=10):
    """
    Locates a button using an XPath string and checks if it is enabled.

    Args:
        driver: Selenium WebDriver instance.
        xpath (str): The raw XPath string.
        timeout (int): Seconds to wait for the button to be visible.

    Returns:
        bool: True if the button is found and enabled, False otherwise.
    """
    try:
        logger.info(f"[STEP] Checking if enabled: {xpath}")

        # Wait for visibility to ensure the button is interactable
        button = WebDriverWait(driver, timeout).until(
            ec.visibility_of_element_located((By.XPATH, xpath))
        )

        if button.is_enabled():
            logger.info("[SUCCESS] Button is enabled ✅")
            return True
        else:
            logger.warning("[WARNING] Button is present but DISABLED ⚠️")
            return False

    except Exception as e:
        logger.error(f"[ERROR] Element not found or check failed: {str(e)} ❌")
        return False


def verify_successful_signin(driver, workspace, email, pwd, db_config, ssh_config, delay=2):
    """
        Verifies successful signin using the given signin credentials.

    Args:
            driver: Selenium WebDriver instance.
            workspace (str): workspace name for sign in
            email (str) : email for sign in
            pwd (str) : password for sign in
            db_config (dict) : db credentials
            ssh_config (dict) : ssh credentials
            delay (int) : delay in seconds (default: 2)

    Returns:
            bool: True if the sign-in flow is successful, False otherwise.

        """
    credentials = {"email": email, "password": pwd}
    expected_otp_page_text = "Enter Code"
    try:

        # Locating/clicking workspace button
        logger.info(f"[STEP] Finding workspace button")
        workspace_element = locate_element(driver, (By.XPATH, "//input[contains(@placeholder,'Workspace')]"),
                                           click_element=True)
        assert workspace_element is not None, "Workspace button failed to click"
        logger.info(f"[SUCCESS] Located workspace button")

        # Entering workspace name
        logger.info(f"[STEP] Entering workspace name")
        workspace_element.send_keys(workspace)
        logger.info(f"[SUCCESS] Workspace entered: {workspace}")
        time.sleep(delay)

        # locating and clicking Next button
        logger.info(f"[STEP] Clicking Next button")
        result = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Next']"),
                                click_element=True)
        assert result is not None, "Next button failed to click"
        logger.info(f"[SUCCESS] Clicked Next button")

        # Checking Sign in page URL
        logger.info(f"[STEP] Checking Sign in page URL...")
        url_contains = verify_url_contains(driver, "https://stage.sxalable.io/login")
        assert url_contains, f"Failed to redirect to Sing in page, Current URL: {driver.current_url}"
        logger.info(f"[SUCCESS] Checked Sign in page URL: {driver.current_url}")
        time.sleep(delay)

        # Entering email, password
        logger.info(f"[STEP] Entering email, password")
        form_success = enter_form_data(driver, credentials, delay=2)
        assert form_success, "Form entry failed. Check the logs to see which field was missing."
        logger.info(f"[SUCCESS] Entered email, password")

        time.sleep(delay)
        current_url = driver.current_url

        # locating and clicking Login button
        logger.info(f"[STEP] locating and clicking Login button")
        result = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Login']"),
                                click_element=True)
        assert result is not None, "Login button failed to click"
        logger.info(f"[SUCCESS] Clicked Login button...")
        time.sleep(delay)

        # Verifying Page navigated to OTP
        logger.info("[STEP] Verifying Page navigated to OTP...")
        url_navigated = verify_url_change(driver, current_url)
        assert url_navigated, f"Navigation timed out! Still stuck on {current_url}"

        # Verify OTP page text
        logger.info(f"[STEP] finding '{expected_otp_page_text}' on OTP page ✅")
        text_found = verify_text_on_page(driver, expected_otp_page_text, timeout=15)
        assert text_found, f"{expected_otp_page_text} was NOT displayed in the OTP page as expected"
        logger.info(f"[SUCCESS] '{expected_otp_page_text}' found on OTP page ✅")
        time.sleep(delay)

        # Fetching OTP from DB
        logger.info("[STEP] Fetching OTP from DB...")
        otp = get_otp_from_db(db_config, ssh_config, email)
        assert otp, f"OTP fetch failed for {email}. Check logs for DB/SSH tunnel issues."
        logger.info(f"[SUCCESS] OTP fetched: {otp} ✅")

        # Entering OTP
        logger.info("[STEP] Entering OTP...")
        otp_status = enter_otp(driver, otp)
        assert otp_status, "Failed to enter OTP into the input fields."
        logger.info("[STEP] Entered OTP")
        time.sleep(delay)

        current_url = driver.current_url

        # Clicking Verify button
        logger.info("[STEP] Clicking Verify button...")
        verify_button = locate_element(driver, (By.XPATH, "//button[@type='submit' and normalize-space()='Verify']"),
                                       click_element=True)
        assert verify_button is not None, "Verify button failed to click"
        logger.info("[STEP] Clicked Verify button...")
        time.sleep(delay)

        # verify page is navigated away from OTP page
        logger.info("[STEP] Verifying Page navigated away from OTP...")
        url_navigated = verify_url_change(driver, current_url)
        assert url_navigated, f"Navigation timed out! Still stuck on {current_url}"
        logger.info("[SUCCESS] Page successfully navigated..")
        time.sleep(delay)

        # Verifying Landing URL after sign-in
        logger.info("[STEP] Verifying Landing URL after sign-in..")

        # landing on dashboard or SxR page depending on signing after/before subscription
        valid_urls = [
            "https://stage.sxalable.io/dashboard",
            "https://stage.sxalable.io/devices/sxr"
        ]

        WebDriverWait(driver, 10).until(
            lambda d: any(d.current_url.startswith(signin_url) for signin_url in valid_urls)
        )

        logger.info(f"[SUCCESS] Valid URL landed: {driver.current_url} ✅")
        return True

    except AssertionError as e:
        logger.error(f"[FAIL] Sign-in Workflow Interrupted: {str(e)} ❌")
        return False
    except Exception as e:
        logger.error(f"[CRITICAL] Unexpected System Error during sign-in: {str(e)} ❌")
        return False


def is_button_clickable(driver, xpath, timeout=10):
    """
    Extensive check to verify if a button is ready for interaction.
    Logs specific failure reasons to help with debugging.
    """
    try:
        WebDriverWait(driver, timeout).until(
            ec.element_to_be_clickable((By.XPATH, xpath))
        )
        logger.info(f"Element is clickable: {xpath}")
        return True

    except TimeoutException:
        logger.error(f"FAILED: Element not clickable within {timeout}s: {xpath}")

    except NoSuchElementException:
        logger.error(f"FAILED: Element does not exist in DOM: {xpath}")

    except ElementClickInterceptedException:
        # This happens if a spinner or modal is covering the button
        logger.error(f"FAILED: Element is obscured by another layer: {xpath}")

    except StaleElementReferenceException:
        # This happens if the page refreshes/updates while checking
        logger.warning(f"RETRYING: Element went stale: {xpath}")
        # A simple recursive call or a second attempt often fixes staleness
        return is_button_clickable(driver, xpath, timeout)

    except WebDriverException as e:
        logger.error(f"FAILED: Internal WebDriver error occurred: {str(e)}")

    except Exception as e:
        logger.error(f"FAILED: An unexpected error occurred: {str(e)}")

    return False
