import great_expectations as ge
import pandas as pd
from hdv.jdbc_objects.jdbc_object import JDBCObject
from hdv.snowflake_objects.snowflake_object import SnowflakeObject


class Validator(SnowflakeObject, JDBCObject):
    """Class that holds the validate method"""

    # row count validation
    row_count_valid = False
    # row hash validation
    row_hash_valid = False
    # great expectations snowflake dataframe
    ge_sf_df = None
    # hash df
    hash_df = None

    def validate(self, jdbc_table: str, snowflake_table: str, snowflake_database: str = None,
                 snowflake_schema: str = None, jdbc_database: str = None):
        try:
            # get jdbc pandas dataframe
            self.initialize_jdbc(database=jdbc_database,
                                 table=jdbc_table
                                 )

            # get snowflake pandas dataframe
            self.initialize_snowflake(database=snowflake_database,
                                      schema=snowflake_schema,
                                      table=snowflake_table
                                      )

            self.count_df_rows()

            self.compare_row_hashes()

            return print(self.row_hash_valid, self.row_count_valid)

        except Exception as e:
            self._logger.error(e)
            return False

        finally:
            if self.jdbc_connection:
                self.jdbc_connection.close()
            if self.sf_connection:
                self.sf_connection.close()
            if self.sf_cursor:
                self.sf_cursor.close()

    def generate_hash_list(self, df: pd.DataFrame):
        """generates a list of hash tuples over the rows in a dataframe"""
        hash_list = df.apply(lambda x: hash(tuple(x)), axis=1).tolist()

        return hash_list

    def count_df_rows(self):
        """expectation to count dataframe rows"""

        # create a great expectations dataframe from the snowflake dataframe for row count expectation
        self.ge_sf_df = ge.from_pandas(self.sf_df)

        # run row count expectation
        self.row_count_valid = self.ge_sf_df.expect_table_row_count_to_equal(len(self.jdbc_df.index))

    def compare_row_hashes(self):
        """expectation to compare row hash strings"""

        # generate hash string data and create the hash dataframe to be used in the hash expectation
        self.hash_df = pd.DataFrame.from_dict(
            {'sf_hashes': self.generate_hash_list(self.sf_df), 'jdbc_hashes': self.generate_hash_list(self.jdbc_df)})

        # convert pandas dataframe to a great expectations dataframe
        self.hash_df = ge.from_pandas(self.hash_df)

        # run hash comparison expectation
        self.row_hash_valid = self.hash_df.expect_column_pair_values_to_be_equal('sf_hashes', 'jdbc_hashes')