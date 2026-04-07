from datetime import datetime


def generate_unique_email(base_email):
    prefix, domain = base_email.split("@")

    timestamp = datetime.now().strftime("%d%m%H%M%S")

    return f"{prefix}+{timestamp}@{domain}"


def generate_unique_workspace_name(base_name):
    timestamp = datetime.now().strftime("%d%m%H%M%S")  # e.g., 153245
    return f"{base_name}{timestamp}"
