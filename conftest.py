import yaml

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import os
from datetime import datetime
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only handle test execution failures
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)

        if driver:
            # Create screenshots folder
            screenshots_dir = os.path.join("logs", "failed_ screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            # Create file name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name

            file_name = os.path.join(
                screenshots_dir,
                f"{test_name}_{timestamp}.png"
            )

            # Take screenshot
            driver.save_screenshot(file_name)

            full_path = os.path.abspath(file_name)

            # Print in console
            print(f"\n[SCREENSHOT] Saved at: {full_path}")

            # Add path to pytest report (visible in HTML as text)
            report.sections.append(
                ("Screenshot", f"Saved at: {full_path}")
            )


def pytest_configure(config):
    os.makedirs("logs", exist_ok=True)
    base_dir = "logs"
    log_dir = os.path.join(base_dir, "testcase_logs")
    html_dir = os.path.join(base_dir, "html_reports")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"test_{timestamp}.log")
    html_file = os.path.join(html_dir, f"report_{timestamp}.html")

    config.option.log_file = log_file
    config.option.log_file_level = "INFO"
    config.option.log_file_format = "%(asctime)s [%(levelname)s] %(message)s"
    config.option.log_file_date_format = "%Y-%m-%d %H:%M:%S"
    config.option.log_format = "%(asctime)s [%(levelname)s] %(message)s"
    config.option.log_date_format = "%Y-%m-%d %H:%M:%S"
    config.option.htmlpath = html_file

    print(f"\n[INFO] Log file: {log_file}")
    print(f"[INFO] HTML report: {html_file}")


@pytest.fixture(scope="session")
def config():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "input_variables", "config.yaml")

    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def driver():
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver
    driver.quit()
