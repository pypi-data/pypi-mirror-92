import platform
import os
import yaml


if not os.getenv('CLOUDY_SQL_HOME'):
    if platform.system().lower() != 'windows':
        os.environ['CLOUDY_SQL_HOME'] = os.getenv('HOME')
    else:
        os.environ['CLOUDY_SQL_HOME'] = os.getenv('USERPROFILE')

# Create configuration
profiles_path = os.path.join(os.getenv("CLOUDY_SQL_HOME"), ".cloudy_sql/configuration_profiles.yml")
default_profiles_path: str = os.path.join(os.path.dirname(__file__),
                                          'configurations/default_configuration_profiles.yml')

#  If the configuration path does not exist - then a default configuration will be created
if not os.path.exists(profiles_path):

    # Set the path for the default configuration if it does not exist
    cloudy_profiles = os.path.join(os.getenv("CLOUDY_SQL_HOME"), ".cloudy_sql")
    if not os.path.exists(cloudy_profiles):
        os.mkdir(cloudy_profiles)

    # Load the default configuration
    with open(default_profiles_path, 'r') as default_stream:
        profiles_configuration = yaml.safe_load(default_stream)

    # Write the default configuration
    with open(profiles_path, 'w') as stream:
        _ = yaml.dump(profiles_configuration, stream)


def load_ipython_extension(ipython):
    """register magics function when opened in IPython environment"""
    from cloudy_sql.magics.sql_to_snowflake import sql_to_snowflake, close_connection
    from cloudy_sql.snowflake_objects.write_snowflake import SnowflakeWriter

    ipython.register_magic_function(
        sql_to_snowflake, magic_kind="cell"
    )

    ipython.register_magic_function(
        close_connection, magic_kind="line"
    )
