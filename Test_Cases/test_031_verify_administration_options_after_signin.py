from utils.verif_utils import *


def test_administration_options_after_signin(driver, config):
    url = config["app"]["url"]
    base_dir = os.getcwd()  # project root
    file_path = os.path.join(base_dir, "input_variables", "test_signin_credentials.json")
    with open(file_path) as f:
        data = json.load(f)
    email = data["email"]
    workspace = data["workspace"]
    pwd = config["app"]["pwd"]
    admin_username = data["admin_username"]
    org_name = data["organization"]
    db_config = config["db"]
    ssh_config = config["ssh"]
    delay = config["app"]["delay"]

    # opening Sxalable URL
    url_status = open_url(driver, url)
    assert url_status, f"{url} failed to load. Check Network/VPN."
    time.sleep(delay)
    # Sign In
    logger.info(f"[STEP] Signing in...")
    sign_in_status = verify_successful_signin(driver, workspace, email, pwd, db_config, ssh_config)
    assert sign_in_status, "Sign in NOT successful ❌"
    logger.info(f"[SUCCESS] Sign in is successful ✅")
    time.sleep(delay)
    # Footer validations
    # Finding Admin username is correct
    logger.info("---Footer Validations---")
    logger.info("[STEP] Validating Admin username is correct")
    admin_user_name_xpath = "//p[contains(@class, '_userName_')]"

    actual_admin_user_name = get_text_from_xpath(driver, admin_user_name_xpath)

    assert actual_admin_user_name == admin_username, f"Sxabale portal does not display the admin user name as " \
                                                     f"expected; received: {actual_admin_user_name}, expected: " \
                                                     f"{admin_username}"

    logger.info("[SUCCESS] Sxabale portal correctly displays the admin user name as "
                f"expected; received: {actual_admin_user_name}, expected: {admin_username}")
    time.sleep(delay)
    logger.info("[STEP] Validating user role is correct")
    user_role_xpath = "//span[contains(@class, '_userRole_')]"
    actual_user_role = get_text_from_xpath(driver, user_role_xpath)
    assert actual_user_role == 'ADMIN', f"Sxabale portal does not display the user role as " \
                                        f"expected; received: {actual_user_role}, expected: " \
                                        f"ADMIN"

    logger.info("[SUCCESS] Sxabale portal correctly displays the user role as "
                f"expected; received: {actual_user_role}, expected: ADMIN")
    time.sleep(delay)
    # Header validations
    logger.info("---Header Validations---")
    logger.info("[STEP] Validating workspace display is correct")

    workspace_xpath = "//span[contains(@class, 'uppercase') and contains(@class, 'text-[22px]')]"
    actual_workspace = get_text_from_xpath(driver, workspace_xpath)
    assert actual_workspace == workspace.upper(), f"Sxabale portal does not display the workspace as " \
                                                  f"expected; received: {actual_workspace}, expected: " \
                                                  f"{workspace.upper()}"
    logger.info("[SUCCESS] Sxabale portal correctly displays the workspace as "
                f"expected; received: {actual_workspace}, expected: {workspace.upper()}")
    time.sleep(delay)
    logger.info("---Tab Validations---")
    logger.info("[STEP] Validating Organization name in Organization page")

    org_name_xpath = "//span[contains(@id, 'OrgName')]"

    navigate_to_tab(driver, 'Organizations')

    time.sleep(delay)

    actual_org = get_text_from_xpath(driver, org_name_xpath)
    assert actual_org == org_name, f"Org tab does not display the org name correctly, expected: {org_name}, " \
                                   f"received: {actual_org}"
    logger.info(f"[SUCCESS] Org tab displays the org name correctly, expected: {org_name}, received: {actual_org}")
    time.sleep(delay)

    logger.info("[STEP] Validating Admin user details in Administration page")

    navigate_to_tab(driver, 'Administration')

    time.sleep(delay)

    email_xpath = "//*[local-name()='svg' and @data-testid='EmailOutlinedIcon']/following-sibling::p"
    actual_email = get_text_from_xpath(driver, email_xpath)
    assert actual_email == email, f"Admin tab does not display the email correctly, expected: {email}, " \
                                  f"received: {actual_email}"
    logger.info(f"[SUCCESS]Admin tab displays the email correctly, expected: {email}, "
                f"received: {actual_email}")

    logger.info("[STEP] Validating role is: Administrator")
    admin_role_xpath = "//span[contains(@id, 'cell-roles-')]//div[contains(@class, 'MuiChip-root')]//span"
    actual_admin_role = get_text_from_xpath(driver, admin_role_xpath)
    assert actual_admin_role == "Administrator", f"Admin tab does not display the admin role correctly, expected: " \
                                                 f"Administrator, " \
                                                 f"received: {actual_admin_role}"

    logger.info("[SUCCESS] Admin tab displays the admin role correctly, expected: "
                f"Administrator, "
                f"received: {actual_admin_role}")

    logger.info("[STEP] Validating status is: Active")
    admin_status_xpath = "//span[contains(@id, 'cell-status-')]//div[contains(@class, 'MuiChip-root')]//span"
    actual_admin_status = get_text_from_xpath(driver, admin_status_xpath)
    assert actual_admin_status == "Active", f"Admin tab does not display the admin status correctly, expected: " \
                                            f"Active, " \
                                            f"received: {actual_admin_status}"

    logger.info("[SUCCESS] Admin tab displays the admin role correctly, expected: "
                f"Active, "
                f"received: {actual_admin_status}")
