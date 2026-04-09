from utils.imports import *


def open_url(driver, url, delay=2):
    """
       Opens the given URL.

       :param driver: Selenium WebDriver instance
       :param url: URL of the page
       :param delay: Seconds to wait (default 2)
       :return: Boolean; True if url opens, False if fails to open
       """
    try:
        logger.info(f"[STEP] Opening URL: {url}")
        driver.get(url)
        time.sleep(delay)
        logger.info(f"[SUCCESS] Opened URL: {url}")
        return True  # <--- Relays SUCCESS
    except Exception as e:
        logger.error(f"[ERROR] URL Navigation failed: {str(e)}")
        return False  # <--- Relays FAILURE


def locate_element(driver, locator, timeout=10, click_element=False):
    """
    Locates an element and optionally clicks it.

    :param driver: Selenium WebDriver instance
    :param locator: Tuple (By.ID, "value") or (By.XPATH, "value")
    :param timeout: Seconds to wait (default 10)
    :param click_element: Boolean; if True, clicks the element after finding it
    :return: The WebElement if found, else None
    """
    try:
        logger.info(f"[STEP] Locating element: {locator}")

        # We wait for 'visibility' first to ensure it's on the screen
        element = WebDriverWait(driver, timeout).until(
            ec.visibility_of_element_located(locator)
        )

        logger.info(f"[SUCCESS] Found element: {locator}")

        if click_element:
            # If clicking, we ensure it's actually 'clickable'
            WebDriverWait(driver, 5).until(ec.element_to_be_clickable(locator))
            element.click()
            logger.info(f"[ACTION] Clicked element: {locator}")

        return element

    except TimeoutException:
        # This identifies exactly which locator failed and captures the UI state
        logger.error(f"[TIMEOUT] Element {locator} not found/clickable within {timeout}s")
        logger.debug(f"[DEBUG] URL at failure: {driver.current_url}")
        logger.debug(f"[DEBUG] Page Snippet: {driver.page_source[:500]}")
        return None

    except Exception as e:
        logger.error(f"[ERROR] Unexpected failure for {locator}: {str(e)}")
        return None


def enter_otp(driver, otp, delay=1, aria_label_base="Please enter OTP character"):
    """
    Iterates through OTP digits and enters them into individual input fields
    based on their aria-label index.

    Args:
        driver: The Selenium WebDriver instance.
        otp (str): The OTP string (e.g., "123456").
        delay (int): Seconds to wait before and after entering the full OTP.
        aria_label_base (str): The prefix of the aria-label used to identify
                               each input box. Defaults to "Please enter OTP character".

    Returns:
        bool: True if all digits were entered successfully, False otherwise.
    """
    try:
        logger.info("[STEP] Entering OTP...")
        time.sleep(delay)

        # Iterate through the OTP string, starting the index at 1
        for i, digit in enumerate(otp, start=1):
            xpath = f"//input[@aria-label='{aria_label_base} {i}']"

            # Find the specific input for this digit
            otp_field = driver.find_element(By.XPATH, xpath)
            otp_field.send_keys(digit)

        time.sleep(delay)
        logger.info(f"[SUCCESS] OTP '{otp}' entered successfully! ✅")
        return True

    except WebDriverException as e:
        logger.error(f"[ERROR] OTP entry failed at digit index {i} ❌")
        logger.error(f"Reason: {str(e)}")
        return False
    except Exception as e:
        logger.error("[CRITICAL] Unexpected error during OTP entry")
        logger.error(str(e))
        return False


def enter_form_data(driver, data_dict, delay=1):
    """
    Generalized utility to fill multiple input fields based on partial placeholder text.

    Args:
        driver: Selenium WebDriver instance.
        data_dict (dict): Keys are partial placeholder strings, values are text to enter.
        delay (int): Seconds to wait between inputs for stability.

    Returns:
        bool: True if all fields were entered, False if any field failed.
    """
    try:
        for key, value in data_dict.items():
            # Construct dynamic XPath using the dictionary key
            xpath = f"//input[contains(@placeholder,'{key}')]"
            logger.info(f"[STEP] Attempting to enter {key}...")

            # Reusing your existing locate_element utility
            # (Ensure locate_element is imported or in the same file)
            element = locate_element(driver, (By.XPATH, xpath), click_element=True)

            if element is None:
                logger.error(f"[ERROR] Failed to locate or click field for: {key} ❌")
                return False

            # Clear and enter data
            element.clear()
            element.click()
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            time.sleep(delay)
            element.send_keys(value)
            logger.info(f"[SUCCESS] {key} entered ✅")
            time.sleep(delay)

        return True

    except WebDriverException as e:
        logger.error(f"[CRITICAL] WebDriver error during form entry: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"[CRITICAL] Unexpected error: {str(e)}")
        return False


def get_text_from_xpath(driver, xpath, timeout=10):
    """
    Waits for an element to be present in the DOM,
    retrieves its text, and strips whitespace.
    """
    try:
        # Correct method: presence_of_element_located
        element = WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )
        return element.text.strip()
    except Exception as e:
        print(f"Error finding element with XPath: {xpath} - {e}")
        return None


def navigate_to_tab(driver, tab_name, timeout=10):
    """
    Navigates to a specific sidebar or menu tab based on its visible text.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        tab_name (str): The exact text of the tab (e.g., 'Subscriptions').
        timeout (int): Seconds to wait for the tab to become clickable.

    Returns:
        bool: True if navigation was successful, False otherwise.

    Raises:
        AssertionError: If the tab fails to be found or clicked within the timeout.
    """
    # Xpath finds the span with text, then moves to the clickable list item/anchor
    tab_xpath = f"//span[text()='{tab_name}']/ancestor::li"

    logger.info(f"[STEP] Navigating to '{tab_name}' page")

    try:
        # Wait until the element is present and clickable
        element = WebDriverWait(driver, timeout).until(
            ec.element_to_be_clickable((By.XPATH, tab_xpath))
        )

        # Perform the click
        element.click()
        logger.info(f"[SUCCESS] Navigated to '{tab_name}' page")
        return True

    except TimeoutException:
        error_msg = f"FAILED: Tab '{tab_name}' was not clickable within {timeout}s"
    except NoSuchElementException:
        error_msg = f"FAILED: Tab '{tab_name}' does not exist in the DOM"
    except ElementClickInterceptedException:
        error_msg = f"FAILED: Tab '{tab_name}' is obscured by another element (e.g., a modal/spinner)"
    except WebDriverException as e:
        error_msg = f"FAILED: WebDriver error during navigation to '{tab_name}': {str(e)}"

    logger.error(error_msg)
    raise AssertionError(error_msg)
