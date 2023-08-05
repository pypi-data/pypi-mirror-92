# used to parse inline arguments
# enables users to input dict str as params value

class Parser:
    """used to parse inline args passed in sql_to_snowflake magic"""
        
    def parse_line(self, params_str, args_str, line):
        """parse passed in-line arguments"""
        try:
            # split args string into individual parts
            sep_str = line.split(' ')
            # loop over parts in sep_str list
            for i in sep_str:

                # construct the params_str and args_str
                if i.endswith("}"):
                    params_str += i
                elif params_str.startswith("--params") and params_str[-1] != "}":
                    params_str += i + " "
                elif i.startswith("--params"):
                    params_str += i + " "
                else:
                    args_str += i + " "

            # remove space at end of args_string
            args_str = args_str[:-1]

            # configure params_string to be JSON serializable
            params_str = params_str.replace("--params", "")[1:].replace("'", '"')
            return params_str, args_str

        except Exception as e:
            return e
