import yaml
import os
import logging
from snowflake import connector

class SnowflakeObject:
    """Base class for all Snowflake Object types.
    This object holds the methods needed to connect to Snowflake and configure Snowflake credentials."""

    # True once Snowflake configured and sf_connection established
    sf_initialized = False
    # credentials used to establish Snowflake connection
    sf_credentials = None
    # Snowflake connection object
    sf_connection = False
    # Snowflake sf_cursor object
    sf_cursor = False
    # logger object
    _logger = logging.getLogger()
    # log message
    log_message = str
    # pandas dataframe of Snowflake table
    sf_df = None

    def initialize_snowflake(self, table: str, database: str = None, schema: str = None):
        """method that creates Snowflake connection and configures Snowflake credentials"""

        if not self.sf_initialized:
            # calls method to configure Snowflake credentials
            self.configure_sf_credentials(
                schema=schema,
                database=database
            )
            # calls method to connect to Snowflake using the sf_credentials variable
            self.get_snowflake_connection(
                user=self.sf_credentials['username'],
                pswd=self.sf_credentials['password'],
                acct=self.sf_credentials['account'],
                role=self.sf_credentials['role']
            )

            # calls method to read from snowflake table and return pandas dataframe
            self.get_sf_pandas_dataframe(
                table=table
            )

        self.sf_initialized = True

    def configure_sf_credentials(self, database: str = None, schema: str = None):
        """configures Snowflake credentials for session"""

        # Path to Snowflake credentials file
        __profile_path: str = os.path.join(os.getenv("HDV_HOME"),
                                           '.hashmap_data_validator/hdv_profiles.yml')
        with open(__profile_path, 'r') as stream:
            self.sf_credentials = yaml.safe_load(stream)['sink']['snowflake']

        # overwrite default credentials with passed in credentials if applicable
        if database:
            self.sf_credentials['database'] = database
        if schema:
            self.sf_credentials['schema'] = schema

        # role is None if none is given or configured as default
        if self.sf_credentials['role'] == '<your snowflake role>':
            self.sf_credentials['role'] = None

        # warehouse is None if none is given or configured as default
        if self.sf_credentials['warehouse'] == '<your snowflake warehouse>':
            self.sf_credentials['warehouse'] = None

        # checks if user has configured or passed credentials
        if self.sf_credentials['username'] == '<snowflake_username>' or self.sf_credentials['password'] == \
                '<snowflake_password>' or self.sf_credentials['account'] == '<snowflake_account>' \
                or self.sf_credentials['database'] == '<snowflake_database>' or self.sf_credentials['schema'] == \
                '<snowflake_schema>':

            self.log_message = f"Please configure your Snowlflake credentials at {__profile_path} or pass the applicable credentials " \
                               f"as arguments when calling this method."
            self._logger.error(self.log_message)
            self.sf_credentials = None
            return False

        return True

    def get_snowflake_connection(self, user, pswd, acct, role=None):
        """establishes a connection with snowflake"""
        self.sf_connection = connector.connect(
            user=user,
            password=pswd,
            account=acct,
            role=role

        )

        return True

    def get_sf_pandas_dataframe(self, table: str):
        """Reads data from a Snowflake table as a pandas dataframe."""

        # initialize cursor object
        self.sf_cursor = self.sf_connection.cursor()
        
        # use warehouse if not None
        if self.sf_credentials['warehouse']:
            self.sf_cursor.execute(f"use warehouse {self.sf_credentials['warehouse']};")

        # select the sf table
        self.sf_cursor.execute(f"select * from {self.sf_credentials['database']}.{self.sf_credentials['schema']}.{table};")

        # fetch sf table as pandas dataframe
        self.sf_df = self.sf_cursor.fetch_pandas_all()
