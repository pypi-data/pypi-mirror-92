import os
import unittest
from unittest.case import skipIf

from etlops.clients.mpp import SnowflakeClient
from pandas import DataFrame
from tests.integration.test_assets import constants

CREDENTIALS_KEY_PAIR_AUTH = {
    SnowflakeClient.ACCOUNT_IDENTIFIER: os.environ.get("SNOWFLAKE_ACCOUNT"),
    SnowflakeClient.USER_IDENTIFIER: os.environ.get("SNOWFLAKE_USER"),
    SnowflakeClient.PRIVATE_KEY_IDENTIFIER: SnowflakeClient.get_private_key_at_path(
        path=os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH"),
        encoded_password=os.environ.get("SNOWFLAKE_PRIVATE_KEY_PASSWORD").encode(),
    ),
    SnowflakeClient.INSECURE_MODE: False,
}

CREDENTIALS_USER_PASSWORD_AUTH = {
    SnowflakeClient.ACCOUNT_IDENTIFIER: os.environ.get("SNOWFLAKE_ACCOUNT"),
    SnowflakeClient.USER_IDENTIFIER: os.environ.get("SNOWFLAKE_USER"),
    SnowflakeClient.PASSWORD_IDENTIFIER: os.environ.get("SNOWFLAKE_PASSWORD"),
    SnowflakeClient.INSECURE_MODE: False,
}
ENABLE_INTEGRATION_TESTS: bool = bool(
    os.environ.get(constants.ENABLE_INTEGRATION_TESTS_KEY, False)
)


class SnowflakeClientAuthentication(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.key_pair_instance = SnowflakeClient(CREDENTIALS_KEY_PAIR_AUTH)
        cls.user_pass_instance = SnowflakeClient(CREDENTIALS_USER_PASSWORD_AUTH)

    def is_data_frame_non_empty(self, data_frame: DataFrame):
        self.assertTrue(isinstance(data_frame, DataFrame) and len(data_frame) > 0)

    @skipIf(ENABLE_INTEGRATION_TESTS, "Skipping integration tests")
    def test_key_pair_auth_connection_is_able_to_run_query(self):
        with self.key_pair_instance as connected_client:
            self.is_data_frame_non_empty(
                connected_client.select_query("select current_date;")
            )

    @skipIf(ENABLE_INTEGRATION_TESTS, "Skipping integration tests")
    def test_user_pass_auth_connection_is_able_to_run_query(self):
        with self.user_pass_instance as connected_client:
            self.is_data_frame_non_empty(
                connected_client.select_query("select current_date;")
            )
