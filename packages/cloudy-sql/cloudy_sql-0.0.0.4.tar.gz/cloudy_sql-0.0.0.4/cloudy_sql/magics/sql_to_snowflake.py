from cloudy_sql.snowflake_objects.snowflake_object import SnowflakeObject
from IPython.core import magic_arguments
from cloudy_sql.parse.arg_parser import Parser
from jinjasql import JinjaSql
import IPython
import json
import pandas as pd

# initiate objects
context = SnowflakeObject()
parser = Parser()


# optional args to pass in
@magic_arguments.magic_arguments()
# variable name for the resulting pandas DataFrame
# users can run pandas commands on this variable
@magic_arguments.argument(
    "destination_var",
    nargs="?",
    help=("If provided, save the output to this variable instead of displaying it.")
)
# Snowflake username (will be used instead of default value)
@magic_arguments.argument(
    "--params",
    nargs="+",
    default=None,
    help=(
    "Parameters to include in the Snowflake query. If provided, the --params flag should be followed by a Python dictionary."
    "Example: --params {'param_key': 'param_value'}")
)
# Snowflake username (will be used instead of default value)
@magic_arguments.argument(
    "--username",
    default=None,
    type=str,
    help=(
    "If provided, the called method will connect to Snowflake with this username instead of the default in the configuration file.")
)
# Snowflake password (will be used instead of default value)
@magic_arguments.argument(
    "--password",
    default=None,
    type=str,
    help=(
    "If provided, the called method will connect to Snowflake with this password instead of the default in the configuration file.")
)
# Snowflake account (will be used instead of default value)
@magic_arguments.argument(
    "--account",
    default=None,
    type=str,
    help=(
    "If provided, the called method will connect to Snowflake with this account instead of the default in the configuration file.")
)
# Snowflake role (will be used instead of default value)
@magic_arguments.argument(
    "--role",
    default=None,
    type=str,
    help=(
    "If provided, the called method will connect to Snowflake with this role instead of the default in the configuration file.")
)
# Snowflake warehouse (will be used instead of default value)
@magic_arguments.argument(
    "--warehouse",
    default=None,
    type=str,
    help=("If provided, the called method will use this warehouse instead of the default in the configuration file.")
)
# magic function that can be called in IPython
def sql_to_snowflake(line, query):

    # initialize variables
    df = None
    params_str = ""
    args_str = ""

    try:
        if line:
            # parse the passed in args
            params_str, args_str = parser.parse_line(params_str=params_str, args_str=args_str, line=line)

        # if '--params' inline arg, covert str to dict
        if params_str:
            params = json.loads(params_str)
        else:
            params = None

        # parse other args
        args = magic_arguments.parse_argstring(sql_to_snowflake, args_str)

        # if params dict, configure query to use the params variables
        if params:
            j = JinjaSql(param_style='pyformat')
            configured_query, bind_params = j.prepare_query(query, params)
        else:
            configured_query = query
            bind_params = None

        # initialize Snowflake credentials
        context.initialize_snowflake(username=args.username,
                                     password=args.password,
                                     account=args.account,
                                     role=args.role,
                                     warehouse=args.warehouse
                                     )

        # execute passed in Snowflake SQL query
        context.cursor.execute(configured_query, bind_params)

        # check if query will return data from a table
        if 'select' in configured_query or 'SELECT' in configured_query:
            df = context.cursor.fetch_pandas_all()

        # if query does not yield a pandas dataframe, return print statement
        else:
            return print("Successfully ran SQL Query in Snowflake")

        # if a destination variable was specified, pandas DataFrame is returned
        # user can run pandas commands on the DataFrame
        if args.destination_var:
            # save the SQL query results as a pandas DataFrame
            IPython.get_ipython().push({args.destination_var: df})
            return print(f"Query successfully ran and results were stored to the '{args.destination_var}' destination variable.")

        # if destination variable not specified, pandas DataFrame is printed out in IPython terminal
        elif isinstance(df, pd.DataFrame):
            return df.head(10)

    # catch error
    except Exception as e:
        context.log_message = e
        context._logger.error(context.log_message)
        return e


def close_connection(line):
    """Function can be called to close Snowflake connection and cursor objects"""
    # close connection
    if context.connection:
        context.connection.close()
    # close cursor
    if context.cursor:
        context.cursor.close()
    return print('connection successfully closed')
