import click
from hdv.validator import Validator


@click.command()
@click.option('-sf', '--snowflake_table', required=True, help='Snowflake table to be validated')
@click.option('-jdbc', '--jdbc_table', required=True, help='JDBC table to be validated')
def cli_validate(snowflake_table, jdbc_table):

    cli_validation = Validator()
    cli_validation.validate(snowflake_table=snowflake_table, jdbc_table=jdbc_table)
