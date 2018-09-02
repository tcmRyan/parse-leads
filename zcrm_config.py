import site
import os
import argparse

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
packages_path = site.getsitepackages()[1]
resources_path = os.path.join(packages_path, 'zcrmsdk', 'resources')
oauth_prop = 'oauth_configuration.properties'


def configure_client(
        redirect_uri,
        accounts_url='https://accounts.zoho.com',
        access_type='offline'):

    # Create a file to avoid MySQL setup
    open(os.path.join(os.path.dirname(resources_path), 'zcrm_oauthtokens.pkl'), 'a').close()

    with open(os.path.join(resources_path, oauth_prop), 'w') as f:
        client_id = 'client_id=' + os.environ['ZCRM_CLIENT_ID']
        client_secret = 'client_secret=' + os.environ['ZCRM_CLIENT_SECRET']
        redirect_url = 'redirect_uri=' + redirect_uri
        token_persistence_path = 'token_persistence_path=' + os.path.dirname(resources_path)
        accounts_url = 'accounts_url=' + accounts_url
        access_type = 'access_type=' + access_type

        config_list = [client_id, client_secret, redirect_url, token_persistence_path, access_type, accounts_url]
        config = '\n'.join(config_list)

        f.write(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client config info.')
    parser.add_argument('redirectUri', help='The redirect uri set during client creation in Zoho')
    args = parser.parse_args()
    configure_client(args.redirectUri)
