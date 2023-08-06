from hdv.validator import Validator

s = Validator()

s.validate(jdbc_table='validator', snowflake_table='validator_test')