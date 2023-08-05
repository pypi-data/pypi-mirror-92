import json
import os

import pytest
from etlops.clients.rdbms import MySQLClient
from etlops.databaseops.mysql import MySQLTransaction
from etlops.utils import SQLQuerySet
from tests.integration.test_assets import constants

pytestmark = pytest.mark.integration


@pytest.fixture
def mysql_credentials():
    return {
        "host": os.environ.get("MYSQL_HOST"),
        "port": os.environ.get("MYSQL_PORT"),
        "user": os.environ.get("MYSQL_USER"),
        "password": os.environ.get("MYSQL_PASSWORD"),
        "charset": os.environ.get("MYSQL_CHARSET"),
    }


@pytest.fixture(scope="module")
def client(mysql_credentials):
    client = MySQLClient(mysql_credentials)
    return client


@pytest.fixture
def query_metadata():
    metadata_path = os.path.join(
        constants.DB_OPS_TESTS_OPS_PATH, "mysql_transaction.json"
    )
    with open(metadata_path) as metadata_file:
        metadata = json.load(metadata_file)

    return metadata


@pytest.fixture
def queryset(metadata):

    query_set = SQLQuerySet(metadata)
    query_set.fetch_queries()
    query_set.build_query_set()
    queries = query_set.get_query_set()
    return queries


def test_executes(client: MySQLClient, queryset: dict, metadata: dict):

    transaction = MySQLTransaction(queries=queryset, client=client, metadata=metadata)
    transaction.execute()
