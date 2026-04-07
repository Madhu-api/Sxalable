from datetime import datetime


def generate_unique_router_name(router_name):
    timestamp = datetime.now().strftime("%d%m%H%M%S")
    return f"{router_name}{timestamp}"
