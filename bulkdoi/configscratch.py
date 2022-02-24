import configparser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(dir_path, 'credentials.ini')

def set_config():
    config = configparser.ConfigParser()
    test_username = input("Enter the Datacite TEST username:")
    test_password = input("Enter the Datacite TEST password:")
    test_credentials = {'username': test_username, 'password': test_password}
    print()
    prod_username = input("Enter the Datacite PRODUCTION username:")
    prod_password = input("Enter the Datacite PRODUCTION password:")
    prod_credentials = {'username': prod_username, 'password': prod_password}
    config['TEST'] = test_credentials
    config['PRODUCTION'] = prod_credentials
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)
    return config

def get_config():
    if os.path.exists(CONFIG_PATH):
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        return config
    else:
        return set_config()
