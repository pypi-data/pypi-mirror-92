import yaml
import os
import logging
import jaydebeapi
import pandas as pd

class JDBCObject:
    """Base class for all JDBC Object types.
    This object holds the methods needed to connect to JDBC and configure JDBC credentials."""

    # True once JDBC configured and connection established
    jdbc_initialized = False
    # credentials used to establish JDBC connection
    jdbc_credentials = None
    # JDBC connection object
    jdbc_connection = False
    # logger object
    _logger = logging.getLogger()
    # log message
    log_message = str
    # jdbc pandas dataframe
    jdbc_df = None

    def initialize_jdbc(self, table: str, database: str = None):
        """method that creates JDBC connection and configures JDBC credentials"""

        if not self.jdbc_initialized:
            # calls method to configure JDBC credentials
            self.configure_jdbc_credentials(database=database)

            # calls method to connect to JDBC using the jdbc_credentials variable
            self.get_jdbc_connection()

            self.get_jdbc_pandas_dataframe(table=table)

        self.jdbc_initialized = True

    def configure_jdbc_credentials(self, database: str = None):
        """configures JDBC credentials for session"""

        # Path to JDBC credentials file
        __profile_path: str = os.path.join(os.getenv("HDV_HOME"),
                                           '.hashmap_data_validator/hdv_profiles.yml')
        with open(__profile_path, 'r') as stream:
            self.jdbc_credentials = yaml.safe_load(stream)['source']['jdbc']

        # overwrite default credentials with passed in credentials if applicable
        if database:
            self.jdbc_credentials['database'] = database

        # checks if user has configured or passed credentials
        if self.jdbc_credentials['user'] == '<username>' or self.jdbc_credentials['password'] == \
                '<password>' or self.jdbc_credentials['host'] == '<host>' or self.jdbc_credentials['port'] == '<port>'\
                or self.jdbc_credentials['driver'] == '<driver_name>' or self.jdbc_credentials['jar_file'] == \
                '<jar_file_path>' or self.jdbc_credentials['database'] == '<database_name>':

            self.log_message = f"Please configure JDBC your credentials at {__profile_path} or pass the applicable credentials " \
                               f"as arguments when calling this method."
            self._logger.error(self.log_message)
            self.jdbc_credentials = None
            return False

        return True

    def get_jdbc_connection(self):
        """establishes a connection with jdbc server"""
        url = self.jdbc_credentials['host'] + ':' + str(self.jdbc_credentials['port'])

        if self.jdbc_credentials['jar_file']:
            self.jdbc_connection = jaydebeapi.connect(self.jdbc_credentials['driver'],
                                                      url=url,
                                                      driver_args=[
                                                          self.jdbc_credentials['user'],
                                                          str(self.jdbc_credentials['password'])
                                                                   ],
                                                      jars=self.jdbc_credentials['jar_file']
                                                      )
        else:
            self.jdbc_connection = jaydebeapi.connect(self.jdbc_credentials['driver'],
                                                      url=url,
                                                      driver_args=[
                                                          self.jdbc_credentials['user'],
                                                          str(self.jdbc_credentials['password'])
                                                                   ]
                                                      )
        return True

    def get_jdbc_pandas_dataframe(self, table: str):
        """Reads data from a JDBC table as a pandas dataframe."""

        self.jdbc_df = pd.read_sql_query(sql=f"select * from {self.jdbc_credentials['database']}.{table}",
                                         con=self.jdbc_connection
                                         )
