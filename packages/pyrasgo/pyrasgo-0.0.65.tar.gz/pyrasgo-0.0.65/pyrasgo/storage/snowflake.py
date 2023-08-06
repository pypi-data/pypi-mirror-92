import logging
import os
from typing import Optional

import pandas as pd
from snowflake import connector as snowflake
from snowflake.connector import SnowflakeConnection

from pyrasgo.monitoring import track_usage
from pyrasgo.storage.base import DataWarehouse, DataWarehouseSession
from pyrasgo.session import Session
from pyrasgo.utils import dataframe


class SnowflakeDataWarehouse(DataWarehouse, Session, metaclass=DataWarehouseSession):
    def __init__(self):
        username = os.environ.get('SNOWFLAKE_USERNAME', self.profile.get("snowUsername", None))
        if username is None:
            raise EnvironmentError("Your user is missing credentials, please contact Rasgo support.")
        self.username = username

        organization = self.profile.get("organization")
        self.organization_code = organization.get("code", None)
        if self.organization_code is None:
            raise EnvironmentError("Your organization is missing credentials, please contact Rasgo support.")

        self.password = os.environ.get("SNOWFLAKE_PASSWORD", self.profile.get("snowPassword"))
        self.account = os.environ.get("SNOWFLAKE_ACCOUNT", organization.get("account"))
        self.database = os.environ.get("SNOWFLAKE_DATABASE", organization.get("database"))
        self.schema = os.environ.get("SNOWFLAKE_SCHEMA", organization.get("schema"))
        self.warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", organization.get("warehouse"))
        self.user_role = os.environ.get("SNOWFLAKE_ROLE",
                                        self.profile.get("role", f"{self.organization_code}_{self.username}"))

    @property
    def publisher_role(self):
        return f"{self.organization_code}PUBLISHER"

    @property
    def reader_role(self):
        return f"{self.organization_code}READER"

    @property
    def public_role(self):
        return "PUBLIC"

    @property
    @track_usage
    def user_connection(self) -> SnowflakeConnection:
        return snowflake.connect(**self.user_credentials)

    @property
    @track_usage
    def user_credentials(self) -> dict:
        return {
            "user": self.username,
            "password": self.password,
            "account": self.account,
            "database": self.database,
            "schema": self.schema,
            "warehouse": self.warehouse,
            "role": self.user_role
        }

    @property
    @track_usage
    def publisher_connection(self) -> SnowflakeConnection:
        return snowflake.connect(**self.publisher_credentials)

    @property
    @track_usage
    def publisher_credentials(self) -> dict:
        return {
            "user": self.username,
            "password": self.password,
            "account": self.account,
            "database": self.database,
            "schema": self.schema,
            "warehouse": self.warehouse,
            "role": self.user_role
        }

    @track_usage
    def execute_query(self, query: str, params: Optional[dict] = None, as_publisher: bool = False):
        """
        Execute a query on the [cloud] data platform.

        :param query: String to be executed on the data platform
        :param params: Optional parameters
        :param as_publisher: Flag on whether to run the query as the publisher role.
        :return:
        """
        if as_publisher:
            return self.publisher_connection.cursor().execute(query, params)
        return self.user_connection.cursor().execute(query, params)

    @track_usage
    def get_source_table(self, table_name: str, database: Optional[str] = None, schema: Optional[str] = None,
                         record_limit: Optional[int] = None) -> pd.DataFrame:
        if record_limit is None:
            logging.info(f"Loading all rows from {table_name}...")
        database = database or self.database
        schema = schema or self.schema
        result_set = self.execute_query(f"SELECT * FROM {database}.{schema}.{table_name} {f'LIMIT {record_limit}' if record_limit else ''}")
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_source_tables(self, database: Optional[str] = None, schema: Optional[str] = None):
        database = database or self.database
        schema = schema or self.schema
        filters = f"WHERE TABLE_SCHEMA='{schema}'"
        result_set = self.execute_query(f"SELECT TABLE_NAME, TABLE_CATALOG||'.'||TABLE_SCHEMA||'.'||TABLE_NAME AS FQTN, ROW_COUNT, TABLE_OWNER, CREATED, LAST_ALTERED FROM {database}.INFORMATION_SCHEMA.TABLES {filters}")
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])

    @track_usage
    def get_source_columns(self, table: Optional[str] = None, database: Optional[str] = None, schema: Optional[str] = None, data_type: Optional[str] = None):
        database = database or self.database
        schema = schema or self.schema
        filters = f"WHERE TABLE_SCHEMA='{schema}'"
        filters += f" AND TABLE_NAME='{table}'" if table else ""
        filters += f" AND DATA_TYPE='{data_type}'" if data_type else ""
        result_set = self.execute_query(f"SELECT COLUMN_NAME, DATA_TYPE, TABLE_NAME, TABLE_CATALOG||'.'||TABLE_SCHEMA||'.'||TABLE_NAME AS FQTN FROM {database}.INFORMATION_SCHEMA.COLUMNS {filters}")
        return pd.DataFrame.from_records(iter(result_set), columns=[x[0] for x in result_set.description])
    
    @track_usage
    def grant_publisher(self):
        self.execute_query(f"GRANT ROLE {self.publisher_role} TO ROLE {self.user_role};", as_publisher=True)

    @track_usage
    def grant_table_ownership(self, table: str, role: str, database: Optional[str] = None, schema: Optional[str] = None):
        database = database or self.database
        schema = schema or self.schema
        self.execute_query(f"GRANT OWNERSHIP ON {database}.{schema}.{table} TO ROLE {role} REVOKE CURRENT GRANTS;")

    @track_usage
    def clone_table(self, existing_table: str, new_table: str, overwrite: bool = False, existing_database: Optional[str] = None, existing_schema: Optional[str] = None):
        """
        Note: we will allow users to select from other database, but only to write into org default database
        """
        database = existing_database or self.database
        schema = existing_schema or self.schema
        if overwrite:
            self.execute_query(f"CREATE OR REPLACE TABLE {new_table} CLONE {database}.{schema}.{existing_table};")
        self.execute_query(f"CREATE TABLE {new_table} CLONE {database}.{schema}.{existing_table};")

    @track_usage
    def append_to_table(self, from_table: str, into_table: str, from_database: Optional[str] = None, from_schema: Optional[str] = None):
        """
        Note: we will allow users to select from other database, but only to write into org default database
        """
        database = from_database or self.database
        schema = from_schema or self.schema
        self.execute_query(f"INSERT INTO {into_table} SELECT * FROM {database}.{schema}.{from_table};")

    def _make_table_metadata(self, table: str):
        if table.count(".") > 0:
            table = table.split(".")[-1]
        metadata = {
            "database": self.database,
            "schema": self.schema,
            "table": table,
        }
        return metadata

    def _write_dataframe_to_table(self, df: pd.DataFrame, table_name: str, append: Optional[bool] = False):
        """
        Note: we will allow users to select from other database, but only to write into org default database
        """
        from snowflake.connector.pandas_tools import write_pandas

        self._snowflakify_dataframe(df)
        write_pandas(conn=self.user_connection, df=df, table_name=self._snowflakify_name(table_name), quote_identifiers=False)

    @classmethod
    def _snowflakify_data_type(cls, dtype: str):
        if dtype.lower() in ["object", "text"]:
            return "string"
        else:
            return dtype.lower()

    @classmethod
    def _snowflakify_dataframe(cls, df: pd.DataFrame):
        """
        Renames all columns in a pandas dataframe to Snowflake compliant names in place
        """
        df.rename(columns={r: cls._snowflakify_name(r) for r in dataframe.build_schema(df)},
                  inplace=True)

    @classmethod
    def _snowflakify_list(cls, list_in):
        """
        param list_in: list
        return list_out: list
        Changes a list of columns to Snowflake compliant names
        """
        return [cls._snowflakify_name(n) for n in list_in]

    @staticmethod
    def _snowflakify_name(name):
        """
        param name: string
        return: string
        Converts a string to a snowflake compliant value
        Removes double quotes, replaces dashes/dots/spaces with underscores, casts to upper case
        """
        return name.replace(" ", "_").replace("-", "_").replace('"', '').replace(".","_").upper()
