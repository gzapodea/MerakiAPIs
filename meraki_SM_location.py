# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems

# !/usr/bin/env python3

import requests
import json
import time
import datetime
import meraki_init
import requests.packages.urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth  # for Basic Auth

from meraki_init import MERAKI_API_KEY, MERAKI_ORG_ID

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

# The following declarations need to be updated based on your lab environment

users_info_list = [{'name': 'Gabi Zapodeanu', 'email': 'gzapodea@cisco.com', 'cell': '+15033094949'},
                   {'name': 'Gabriel Zapodeanu', 'email': 'gabriel.zapodeanu@gmail.com', 'cell': '+15036252333'}]

user_email = 'gzapodea@cisco.com'

MERAKI_URL = 'https://dashboard.meraki.com/api/v0'


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """

    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))



def meraki_get_organizations():
    """
    This function will get the Meraki Organization Id
    API call to /organizations
    :return: Meraki Organization Id
    """
    url = MERAKI_URL + '/organizations'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    org_response = requests.get(url, headers=header, verify=False)
    org_json = org_response.json()
    org_id = org_json[0]['id']
    return org_id


def meraki_get_networks(organization_id):
    """
    This function will return the list of networks associated with the Meraki Organization ID
    API call to /organizations/{organization_id]/networks
    :param organization_id: Meraki Organization ID
    :return: network ids and names
    """
    url = MERAKI_URL + '/organizations/' + str(organization_id) + '/networks'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    networks_response = requests.get(url, headers=header, verify=False)
    networks_json = networks_response.json()
    network_id = networks_json[0]['id']
    network_name = networks_json[0]['name']
    return network_id, network_name


def meraki_get_sm_devices(network_id):
    """
    This function will return the list of networks associated with the Meraki Organization ID
    API call to /networks/{organization_id]/sm/devices
    :param network_id: Meraki network ID
    :return:
    """

    url = MERAKI_URL + '/networks/' + str(network_id) + '/sm/devices?fields=phoneNumber,location'
    print(url)
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    sm_devices_response = requests.get(url, headers=header, verify=False)
    sm_devices_json = sm_devices_response.json()['devices']
    return sm_devices_json


def get_user_cell(users_info, email):
    """
    This function will look up the user cell phone based on his email
    :param users_info: List of all the users info
    :param user_email: user email address
    :return: the user cell phone number
    """

    user_cell = None
    for user in users_info:
        if user['email'] == email:
            user_cell = user['cell']
    return user_cell


def get_location_cell(sm_devices_list, user_cell):
    """
    This function will locate the user based on his cell phone number
    :param sm_devices_list: the list of Meraki SM devices
    :param user_cell: user cell phone number
    :return: the user location
    """
    location = None
    for device in sm_devices_list:
        if device['phoneNumber'] == user_cell:
            pprint(device)
            location = device['location']
    return location


def main():

    pprint(users_info_list)
    # get the Meraki organization id

    meraki_org_id = meraki_get_organizations()
    print('Your Meraki Organization ID is: ', meraki_org_id)

    # get the Meraki networks info

    meraki_network_info = meraki_get_networks(meraki_org_id)
    meraki_network_id = meraki_network_info[0]
    meraki_network_name = meraki_network_info[1]

    print('Your Meraki Network ID is: ', meraki_network_id)
    print('Your Meraki Network Name is: ', meraki_network_name)

    # get the Meraki SM devices

    meraki_sm_devices_list = meraki_get_sm_devices(meraki_network_id)
    #print('Your Meraki SM Devices list: \n')
    #pprint(meraki_sm_devices_list)

    # find out the user cell phone number based on email address

    user_cell = get_user_cell(users_info_list, user_email)
    print('The SM user with the email ', user_email, ' has the cell phone number ', user_cell)

    # find the location for the device with the specified cell phone number

    user_location = get_location_cell(meraki_sm_devices_list,user_cell)
    print('The SM user with the cell phone ', user_cell, ' is located at this address ', user_location)


if __name__ == '__main__':
    main()
