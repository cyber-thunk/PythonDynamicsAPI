"""Sep 29, 2022: Accessing dynamics crm records via graph.
This is POC. In prod, will be looking for job nos & using
those to then look for associated gcts files which will be
retreived via graph api.
"""

import datetime
import json

import msal
import requests


def access_d365_data():
    print_header()
    config_data = get_config_data()
    connect_token_dict = get_token_dict(config_data)
    dynamics_data(connect_token_dict, config_data)


def dynamics_data(token_dict:dict, config_data:dict):
    """Access dynamics data.
    
    Args:
        token_dict (dict): token dict.
        config_data (dict): config dict.
    """
    if not token_dict:
        print(dynamics_data.__name__ + 'Error: No token dict')

    auth_string = f"{token_dict.get('token_type')} {token_dict.get('access_token')}"

    crm_opportunities = requests.get(f"{config_data.get('365_api_url')}opportunities",
                                     headers={'Authorization': auth_string})
    crm_opportunities = crm_opportunities.json()

    opp_names = []
    for opportunity in crm_opportunities.get('value'):
        """This is POC. In prod, will be looking for job nos. Can
        build list of them and then use them to look for associated
        gcts files which will be retreived via graph api.
        """
        try:
            if opportunity.get('actualvalue_base') >= 20000:
                # print(f"{opportunity.get('name')} has revenue of {opportunity.get('actualvalue_base')}")
                opp_names.append(opportunity.get('name'))
        except TypeError:
            print(f"{opportunity.get('name')} has {type(opportunity.get('actualvalue_base'))} for type of revenue")

    print()
    print(opp_names)   


def get_token_dict(config_data:dict)->str:
    """Get token from Azure AD.

    Args:
        config_data (dict): config data.

    Returns:
        token (str): token.
    """
    authority = config_data.get('authority')
    client_id = config_data.get('client_id')
    client_secret = config_data.get('client_value')
    scope = config_data.get('scope')

    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority
    )

    result = app.acquire_token_for_client(scopes=scope)

    if 'access_token' in result:
        token_dict = result
    else:
        token_dict = {}

    return token_dict


def get_config_data()->dict:
    """Get config data from config.json file.

    Returns:
        config_data (dict): config data.
    """
    with open('parameters.json') as config_file:
        config_data = json.load(config_file)

    return config_data


def print_header():
    """Print header"""
    print('----------------------------------------')
    print('Accessing Dynamics CRM records via graph')
    print(str(datetime.datetime.now()))
    print('----------------------------------------')
    print()


if __name__ == '__main__':
    access_d365_data()
