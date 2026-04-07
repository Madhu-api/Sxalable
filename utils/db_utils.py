import psycopg2
import paramiko
import logging
# MONKEY PATCH: Fix for 'paramiko' has no attribute 'DSSKey'
# This allows newer paramiko (3.x) to work with older sshtunnel (0.4.0)
if not hasattr(paramiko, 'DSSKey'):
    paramiko.DSSKey = paramiko.PKey

from sshtunnel import SSHTunnelForwarder
logger = logging.getLogger(__name__)


def get_otp_from_db(db_config, ssh_config, email):
    try:
        logger.info("[STEP] Starting SSH tunnel (using default SSH config)")

        with SSHTunnelForwarder(
            (ssh_config["host"], ssh_config["port"]),
            ssh_username=ssh_config["username"],
            #  No ssh_pkey → uses default ssh config
            remote_bind_address=(db_config["host"], db_config["port"])
        ) as tunnel:

            logger.info("[SUCCESS] SSH tunnel established")

            conn = psycopg2.connect(
                host="127.0.0.1",
                port=tunnel.local_bind_port,
                database=db_config["database"],
                user=db_config["user"],
                password=db_config["password"]
            )

            cursor = conn.cursor()

            query = """
                SELECT otp
                FROM otp_requests
                WHERE email = %s
                ORDER BY expires_at DESC
                LIMIT 1;
            """

            cursor.execute(query, (email,))
            result = cursor.fetchone()

            cursor.close()
            conn.close()

            if result:
                otp = result[0]
                logger.info(f"[DB SUCCESS] OTP fetched: {otp}")
                return otp
            else:
                logger.error("[DB ERROR] No OTP found")
                return None

    except Exception as e:
        logger.error("[ERROR] DB fetch failed ❌")
        logger.error(str(e))
        return None
