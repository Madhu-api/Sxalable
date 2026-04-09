from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import (

    NoSuchElementException,
    ElementClickInterceptedException,

)
import logging
import time
from selenium.webdriver.common.keys import Keys
from utils.db_utils import get_otp_from_db
import os
import json
logger = logging.getLogger(__name__)