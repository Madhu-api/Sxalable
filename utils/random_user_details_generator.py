from datetime import datetime
import random
import string


def generate_unique_first_name(first_name):
    # Generates 8 random lowercase letters
    timestamp = datetime.now().strftime("%d%m%H%M%S")
    mapping = str.maketrans("0123456789", "abcdefghij")
    unique_suffix = timestamp.translate(mapping)
    return f"{first_name}{unique_suffix}"


def generate_unique_company_name(company_name):
    timestamp = datetime.now().strftime("%d%m%H%M%S")
    mapping = str.maketrans("0123456789", "abcdefghij")
    unique_suffix = timestamp.translate(mapping)    # e.g., 153245
    return f"{company_name}{unique_suffix}"


def generate_unique_company_address(company_address):
    timestamp = datetime.now().strftime("%d%m%H%M%S")
    mapping = str.maketrans("0123456789", "abcdefghij")
    unique_suffix = timestamp.translate(mapping)
    # e.g., 153245
    return f"{company_address}{unique_suffix}"
