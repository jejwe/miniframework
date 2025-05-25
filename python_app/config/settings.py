import os

# --- Database Configuration ---
# In the PHP MiniFramework, database configurations are loaded based on APP_ENV.
# - If APP_ENV == 'prod', it loads 'database.php'.
# - Otherwise, it loads 'database-[APP_ENV].php' (e.g., 'database-dev.php').
#
# The provided PHP files (database.php, database-dev.php, database-test.php)
# all contain identical 'default' database configurations.
# We will define the 'default' configuration here.

DEFAULT_DATABASE_CONFIG = {
    'host': 'localhost',    # Host address
    'port': 3306,           # Port
    'dbname': 'test',       # Database name
    'username': 'root',     # Username
    'passwd': '',           # Password (empty in the original config)
    'charset': 'utf8',      # Character encoding
    'persistent': False     # Whether to use persistent connections
}

# For handling multiple environments in Python, several strategies can be used:
# 1. Environment variables to override specific keys.
# 2. Separate configuration files (e.g., settings_dev.py, settings_prod.py)
#    and an entry point that imports the correct one based on an env variable.
# 3. A dictionary that holds configurations for all environments,
#    and the active one is selected based on an env variable.

# Example of strategy 3:
# ALL_DATABASES = {
# 'development': {
# 'default': DEFAULT_DATABASE_CONFIG.copy() # Start with defaults
#         # Potentially override keys for dev, e.g.:
#         # 'dbname': 'dev_test_db',
#     },
# 'test': {
# 'default': DEFAULT_DATABASE_CONFIG.copy()
#         # 'dbname': 'test_db_instance',
#     },
# 'production': {
# 'default': DEFAULT_DATABASE_CONFIG.copy()
#         # 'host': 'prod_db_host.example.com',
#         # 'username': 'prod_user',
#         # 'passwd': os.environ.get('PROD_DB_PASSWORD') # Load sensitive data from env
#     }
# }
#
# ACTIVE_ENV = os.environ.get('APP_ENV', 'development').lower()
# DATABASES = ALL_DATABASES.get(ACTIVE_ENV, ALL_DATABASES['development'])

# For now, we'll just define the single configuration as per the provided files:
DATABASES = {
    'default': DEFAULT_DATABASE_CONFIG
}

# --- General Application Settings ---
# These are examples of what might typically be in a general config file.
# The PHP project did not have a separate App/Config/config.php.

APP_NAME = "MyConvertedApp"
DEBUG_MODE = True # Set to False in a production environment

# Example of how APP_ENV might be determined (similar to PHP's APP_ENV)
# This would typically be set by the server environment or an .env file.
APP_ENV = os.environ.get('APP_ENV', 'development') # Defaults to 'development' if not set

if APP_ENV == 'production':
    DEBUG_MODE = False
    # Potentially load other production-specific settings or overrides here
elif APP_ENV == 'test':
    DEBUG_MODE = True
    # DATABASES['default']['dbname'] = 'test_actual_db' # Example override
    pass
elif APP_ENV == 'development':
    DEBUG_MODE = True
    pass

# --- CherryPy Specific Configuration ---
# This would typically be defined closer to where the CherryPy app is configured and run.
# However, some global parameters could reside here.
CHERRYPY_CONFIG = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'engine.autoreload.on': DEBUG_MODE, # Autoreload based on DEBUG_MODE
    },
    # Configuration for mounted applications, tools, etc. can also go here
    # For example, to enable MethodDispatcher for all API routes:
    # '/api': {
    # 'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    # 'tools.json_out.on': True # If all API routes return JSON by default
    # }
}

# Example of how to access a specific database setting:
# default_db_host = DATABASES.get('default', {}).get('host')
# print(f"Default DB Host: {default_db_host} (Running in APP_ENV: {APP_ENV})")
