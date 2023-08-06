import argparse
from hdv.validator import Validator
import getopt
import sys


def cli_validate(argv):
    if argv is None:
        argv = sys.argv[1:]
    sf_table = ''
    jdbc_table = ''
    try:
        opts, args = getopt.getopt(argv, "sf:jdbc:", ["snowflake_table=", "jdbc_table="])
    except getopt.GetoptError:
        print("hdv -sf <snowflake_table> -jdbc <jdbc_table>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-sf", "--snowflake_table"):
            sf_table = arg
        elif opt in ("-jdbc", "--jdbc_table"):
            jdbc_table = arg

    return print(sf_table, jdbc_table)

# def main(snowflake, jdbc):
#
#     data_validation = Validator()
#     data_validation.validate(snowflake_table=snowflake, jdbc_table=jdbc)
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(prog='hashmap_data_validator', usage='%(prog)s [options]')
#     parser.add_argument("-sf", "--snowflake_table", type=str,
#                         help="The name of the Snowflake table that you would like to validate.")
#     parser.add_argument("-jdbc", "--jdbc_table", type=str,
#                         help="The name of the JDBC table that you would like to validate.")
#
#     args = parser.parse_args()
#
#     data_validation = Validator()
#
#     data_validation.validate(snowflake_table=args.snowflake_table, jdbc_table=args.jdbc_table)
