from . import cli_validate
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-sf", "--snowflake_table", type=str,
                        help="The name of the Snowflake table that you would like to validate.")
    parser.add_argument("-jdbc", "--jdbc_table", type=str,
                        help="The name of the JDBC table that you would like to validate.")

    args = parser.parse_args()
    cli_validate(sf_table=args.snowflake_table, jdbc_table=args.jdbc_table)
