from utils.db_utils import get_otp_from_db
import logging

logger = logging.getLogger(__name__)


def test_fetch_otp(config):
    logger.info("[STEP] Fetching OTP from DB")

    db_config = config["db"]
    ssh_config = config["ssh"]
    email = config["app"]["email"]

    otp = get_otp_from_db(db_config, ssh_config, email)

    assert otp is not None, "OTP not found ❌"

    logger.info(f"[SUCCESS] OTP fetched: {otp} ✅")