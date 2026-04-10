def add_AWS_SxR_and_return_status(driver, router_name, region,
                                  AWS_credentials, VM_size, network_CIDR_block, interface_count,
                                subnet_CIDR_blocks, delay=2):
    """
        Adds an SxR type=AWS and returns status.

    Args:
            driver: Selenium WebDriver instance.
            router_name (str): unique AWS router name ex:
            region (str) : region in which AWS router to be deployed
            AWS_credentials (dict) : AWS credentials
            VM_size (str): example: VM size t2.small, t3.small
            network_CIDR_block (str): example: 10.0.0.0/16
            interface_count (int): number of interfaces ex: 2
            subnet_CIDR_blocks (list): list of subnet CIDR blocks ex: [10.0.252.0/24, 10.0.252.0/23]


    Returns:
            bool: True if the SxR add is successful, False otherwise.

        """