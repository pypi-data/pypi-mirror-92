import unittest
from IPython.core.error import UsageError
from cloudy_sql.parse.arg_parser import Parser

parser = Parser()


class TestParser(unittest.TestCase):
    """unittests for Parser"""

    def test_parse_line(self):
        line = "df --params {'hello': 'there'} --username a_snowflake_username"
        param, args = parser.parse_line(params_str="", args_str="", line=line)
        assert param == '{"hello": "there"}'
        assert args == 'df --username a_snowflake_username'

    def test_parse_line(self):
        line = "df --username a_snowflake_username"
        param, args = parser.parse_line(params_str="", args_str="", line=line)
        assert param == ''
        assert args == 'df --username a_snowflake_username'