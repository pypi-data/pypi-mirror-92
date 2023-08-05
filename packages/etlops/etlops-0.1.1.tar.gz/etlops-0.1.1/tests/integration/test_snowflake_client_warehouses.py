import os
import unittest
from unittest import skipIf

from etlops.clients.mpp import SnowflakeClient
from tests.integration.test_snowflake_client import CREDENTIALS_USER_PASSWORD_AUTH
from tests.integration.test_assets import constants

ENABLE_INTEGRATION_TESTS: bool = bool(
    os.environ.get(constants.ENABLE_INTEGRATION_TESTS_KEY, False)
)


class SnowflakeClientWarehouses(unittest.TestCase):
    @skipIf(ENABLE_INTEGRATION_TESTS, "Skipping integration tests")
    def test_client_is_able_to_resume_warehouse(self):
        with SnowflakeClient(CREDENTIALS_USER_PASSWORD_AUTH) as connected_client:
            try:
                connected_client.alter_warehouse(
                    "XSMALL_ETL", connected_client.RESUME_COMMAND
                )
            except Exception as exception:
                self.fail(exception)
