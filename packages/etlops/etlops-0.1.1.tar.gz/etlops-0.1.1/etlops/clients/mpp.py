import logging
from typing import Any, Dict, Optional, Union

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from etlops.clients.exceptions import AuthenticationError
from etlops.clients.sql import SQLClient
from pandas import DataFrame, read_sql
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine


class SnowflakeClient(SQLClient):
    SUSPENDED_WAREHOUSE_STATUS = ("SUSPENDED", "SUSPENDING")
    USER_IDENTIFIER = "user"
    PASSWORD_IDENTIFIER = "password"
    ACCOUNT_IDENTIFIER = "account"
    INSECURE_MODE = "insecure_mode"
    PRIVATE_KEY_IDENTIFIER = "private_key"
    WAREHOUSE = "WAREHOUSE"
    SUSPEND_COMMAND = "suspend"
    RESUME_COMMAND = "resume"
    RESUME_IF_SUSPENDED = "resume if suspended"

    def __init__(
        self,
        config: Optional[Union[Dict[str, Any], str]] = None,
        *,
        user: Optional[str] = None,
        password: Optional[str] = None,
        account: Optional[str] = None,
        insecure_mode: bool = False,
        private_key: Optional[bytes] = None,
    ):
        if isinstance(config, str):
            self.configuration_dict = self._load_configuration_file(config)
        elif isinstance(config, dict):
            self.configuration_dict = config
        elif config is None:
            self.configuration_dict = {
                self.USER_IDENTIFIER: user,
                self.PASSWORD_IDENTIFIER: password,
                self.ACCOUNT_IDENTIFIER: account,
                self.INSECURE_MODE: insecure_mode,
                self.PRIVATE_KEY_IDENTIFIER: private_key,
            }

        self.user = self.configuration_dict.get(self.USER_IDENTIFIER, user)
        self.password = self.configuration_dict.get(self.PASSWORD_IDENTIFIER, password)
        self.account = self.configuration_dict.get(self.ACCOUNT_IDENTIFIER, account)
        self.insecure_mode = self.configuration_dict.get(
            self.INSECURE_MODE, insecure_mode
        )
        self.private_key = self.configuration_dict.get(
            self.PRIVATE_KEY_IDENTIFIER, private_key
        )
        self.key_pair_auth = self.private_key is not None
        self._validate_connection_params(self.private_key, self.password)

        self.sql_alchemy_connection = None
        self.__set_sql_aqlchemy_engine()
        self.logger = logging.getLogger("SnowflakeClient")

    @staticmethod
    def _validate_connection_params(
        private_key: Optional[bytes], password: Optional[str]
    ) -> None:
        """
        Validates that exactly one of the private key or
        password options were provided.

        Raises:
            - AuthenticationError: If there wasn't exactly one authentication
                option provided
        """
        if not private_key and not password:
            raise AuthenticationError(
                (
                    "Neither the password nor the private key"
                    " have been provided. Exactly one was expected."
                )
            )

        if private_key and password:
            raise AuthenticationError(
                "Both password and private key were provided. Exactly one was expected"
            )

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "SnowflakeClient":
        """
        Alternate constructor to create a `SnowflakeClient` from a
        dictionary.

        Args:
            - config (Dict[str, Any]): Mapping of arguments required
                to connect to Snowflake.

        Raises:
            - ValueError: If one of the required keys is not present.
        """
        required_keys = [
            cls.USER_IDENTIFIER,
            cls.PASSWORD_IDENTIFIER,
            cls.ACCOUNT_IDENTIFIER,
            cls.INSECURE_MODE,
        ]
        for required_key in required_keys:
            if required_key not in config.keys():
                raise ValueError(
                    "Required key {key} not found in configuration".format(
                        key=required_key
                    )
                )
        return cls(**config)

    @classmethod
    def from_private_key_file(
        cls, path: str, encoded_password: bytes, *args: Any, **kwargs: Any
    ) -> "SnowflakeClient":

        private_key = cls.get_private_key_at_path(
            path=path, encoded_password=encoded_password
        )
        return cls(*args, **kwargs, private_key=private_key)

    def __set_sql_aqlchemy_engine(self):
        url = URL(
            account=self.account, user=self.user, insecure_mode=self.insecure_mode
        )

        if self.key_pair_auth:
            conn_args = {"private_key": self.private_key}
        else:
            conn_args = {"password": self.password}

        self.sql_alchemy_engine = create_engine(
            url,
            connect_args=conn_args,
        )

    def connect(self) -> None:
        self.sql_alchemy_connection = self.sql_alchemy_engine.connect()
        self.logger.info("Snowflake Connection Open")

    def disconnect(self):
        if not self.sql_alchemy_connection:
            self.logger.info("Not connected to Snowflake. Skipping disconnect.")
            return
        self.sql_alchemy_connection.close()
        self.logger.info("Snowflake Connection Closed")

    def switch_to(self, db_object: str, db_object_name: str) -> None:
        if db_object.upper() == SnowflakeClient.WAREHOUSE:
            self.alter_warehouse(warehouse=db_object_name, action="resume")
        switching_query = "USE {OBJECT} {OBJECT_NAME};".format(
            OBJECT=db_object, OBJECT_NAME=db_object_name
        )
        self.sql_alchemy_connection.execute(switching_query)
        self.logger.info(
            "Switched to {OBJECT} = {OBJECT_NAME} successfully".format(
                OBJECT=db_object, OBJECT_NAME=db_object_name
            )
        )

    def __check_warehouse_state(self, warehouse: str) -> str:
        warehouse = warehouse.upper()
        warehouse_state_dataframe = self.select_query(
            "SHOW WAREHOUSES LIKE '{WAREHOUSE}';".format(WAREHOUSE=warehouse)
        )
        warehouse_state = warehouse_state_dataframe.loc[
            warehouse_state_dataframe["name"] == warehouse, "state"
        ].values[0]
        return warehouse_state

    def dml_query(self, query_string: str) -> None:
        self.sql_alchemy_connection.execute(query_string)

    def select_query(self, query_string: str) -> DataFrame:
        return read_sql(query_string, con=self.sql_alchemy_connection)

    def alter_warehouse(self, warehouse: str, action: str) -> None:
        status = self.__check_warehouse_state(warehouse)
        if (
            action == SnowflakeClient.SUSPEND_COMMAND
            and status not in SnowflakeClient.SUSPENDED_WAREHOUSE_STATUS
        ):
            self.__alter_warehouse_query(warehouse, SnowflakeClient.SUSPEND_COMMAND)
        elif (
            action == SnowflakeClient.RESUME_COMMAND
            and status in SnowflakeClient.SUSPENDED_WAREHOUSE_STATUS
        ):
            self.__alter_warehouse_query(warehouse, SnowflakeClient.RESUME_IF_SUSPENDED)

    def __alter_warehouse_query(self, warehouse: str, command: str):
        self.dml_query(
            "Alter warehouse {WAREHOUSE} {COMMAND};".format(
                WAREHOUSE=warehouse, COMMAND=command
            )
        )

    @staticmethod
    def get_private_key_at_path(path: str, encoded_password: bytes) -> bytes:
        with open(path, "rb") as key:
            p_key = serialization.load_pem_private_key(
                key.read(), password=encoded_password, backend=default_backend()
            )

        return p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
