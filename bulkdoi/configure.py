import configparser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(dir_path, 'credentials.ini')

def set_config():
    config = configparser.ConfigParser()
    print('Enter Datacite credentials as prompted. Enter empty line to abort.')
    test_username = input("Enter the Datacite TEST username:")
    if not test_username: return
    test_password = input("Enter the Datacite TEST password:")
    if not test_password: return
    test_credentials = {'username': test_username, 'password': test_password}
    if not test_credentials: return
    print()
    prod_username = input("Enter the Datacite PRODUCTION username:")
    if not prod_username: return
    prod_password = input("Enter the Datacite PRODUCTION password:")
    if not prod_password: return
    prod_credentials = {'username': prod_username, 'password': prod_password}
    if not prod_credentials: return
    config['TEST'] = test_credentials
    config['PRODUCTION'] = prod_credentials
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)
    return make_dict(config)

def get_config():
    if os.path.exists(CONFIG_PATH):
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        return make_dict(config)
    else:
        return set_config()

def make_dict(config):
    return {
        'test': {
            'username': config['TEST']['username'],
            'password': config['TEST']['password']
            },
        'production': {
            'username': config['PRODUCTION']['username'],
            'password': config['PRODUCTION']['password']
        }
    }