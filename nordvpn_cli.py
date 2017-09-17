#!/usr/bin/python
# coding: utf-8

"""NordVPN_CLI
This file is part of NordVPN_CLI.

NordVPN_CLI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

NordVPN_CLI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with NordVPN_CLI.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import zipfile
import re
import subprocess
import sys
import getopt
import urllib
import json
import urllib2
import requests
from terminaltables import AsciiTable


# Defines
__VERSION__ = "1.0.0"
__AUTHOR__ = "killerbyte"
__AUTHOR_EMAIL__ = "killerbyte[at]protonmail[dot]com"
__AUTHOR_TWITTER__ = "@killerbyte"

__INFO_MSG__ = 0
__WARING_MSG__ = 1
__ERROR_MSG__ = 2

__HTTP_RESPONSE_CODE_OK__ = 200

# Errors
__NO_ERRORS__ = 0
__ARGUMENT_PARSING_ERROR__ = 1
__OPENVPN_NOT_FOUND__ERROR__ = 2
__DOWNLOAD_CONFIG_ERROR__ = 3

__OPENVPN_PATH__ = "/usr/sbin/openvpn"
__NORDVPN_REST_API_URL__ = "https://nordvpn.com/wp-admin/admin-ajax.php?"
__NORDVPN_CONFIG_CLI_PATH__ = "/etc/nordvpn_cli/"
__NORDVPN_CONFIG_CLI_FILE__ = "/etc/nordvpn_cli/config.zip"
__NORDVPN_CONFIG_PACKAGE_URL__ = "https://nordvpn.com/api/files/zip"

__NORDVPN_SERVER_COUNTRY__ = {'ch': 'Switzerland',
                              'gr': 'Greece',
                              'cl': 'Chile',
                              'ee': 'Estonia',
                              'eg': 'Egypt',
                              'al': 'Albania',
                              'vn': 'Vietnam',
                              'cz': 'Czech Republic',
                              'cy': 'Cyprus',
                              'ar': 'Argentina',
                              'au': 'Australia',
                              'at': 'Austria',
                              'in': 'India',
                              'cr': 'Costa Rica',
                              'ie': 'Ireland',
                              'id': 'Indonesia',
                              'es': 'Spain',
                              'ru': 'Russia',
                              'nl': 'Netherlands',
                              'pt': 'Portugal',
                              'no': 'Norway',
                              'tw': 'Taiwan',
                              'tr': 'Turkey',
                              'lv': 'Latvia',
                              'nz': 'New Zealand',
                              'lu': 'Luxembourg',
                              'th': 'Thailand',
                              'it': 'Italy',
                              'ro': 'Romania',
                              'uk': 'United Kingdom',
                              'ca': 'Canada',
                              'pl': 'Poland',
                              'be': 'Belgium',
                              'fr': 'France',
                              'bg': 'Bulgaria',
                              'dk': 'Denmark',
                              'hr': 'Croatia',
                              'ua': 'Ukraine',
                              'de': 'Germany',
                              'jp': 'Japan',
                              'hu': 'Hungary',
                              'za': 'South Africa',
                              'hk': 'Hong Kong',
                              'br': 'Brazil',
                              'fi': 'Finland',
                              'is': 'Iceland',
                              'md': 'Moldova',
                              'sg': 'Singapore',
                              'rs': 'Serbia',
                              'ge': 'Georgia',
                              'us': 'United States',
                              'sk': 'Slovakia',
                              'kr': 'South Korea',
                              'si': 'Slovenia',
                              'my': 'Malaysia',
                              'mx': 'Mexico',
                              'se': 'Sweden',
                              'il': 'Israel'}

__NORDVPN_SERVER_TYPES__ = {'dvpn':'Double VPN',
                            'addos':'Anti DDoS',
                            'dedip':'Dedicated IP servers',
                            'svpn':'Standard VPN servers',
                            'p2p':'P2P',
                            'obvpn':'Obfuscated Servers'}


nordvpn_country = None
nordvpn_server = None
nordvpn_type  = None
print_servers = None
print_country_codes = None

def print_banner():
    """
    Prints the software banner
    """
    print 'NordVPN CLI'
    print 'Version: {version}'.format(version=__VERSION__)
    print 'Author: {author}'.format(author=__AUTHOR__)
    print 'Email: {author_email}'.format(author_email=__AUTHOR_EMAIL__)
    print 'Twitter: {author_twitter}'.format(author_twitter=__AUTHOR_TWITTER__)
    print

def print_usage():
    """
    Prints the software usage
    """
    print '''
Syntax: nordvpn_cli.py [--country=COUNTRY][--print-servers][--country-codes][--server=]

Options:
--country           Uses the server with lowest load of the selected Country
--type              Select the server type. Available types:
                    dvpn  = Double VPN
                    addos = Anti DDoS
                    dedip = Dedicated IP servers
                    svpn  = Standard VPN servers
                    p2p   = P2P
                    obvpn = Obfuscated Servers
--print-servers     Gets all servers of the selected Country
--country-codes     Gets all country codes in ISO 3166-1 alpha2 format
--server            Connects to specified ovpn file server descriptor

Examples:
nordvpn_cli.py --country=IT --print-servers             Prints all Standard VPN Italian Servers
nordvpn_cli.py --country=IT --print-servers --type=p2p  Prints all P2P Italian Servers
nordvpn_cli.py --country=IT                             Connects to the best Italian Server
nordvpn_cli.py --country=IT --type=svpn                 Connects to the best Standard VPN Italian server
nordvpn_cli.py --country-codes                          Prints ISO 3166-1 alpha2 table
nordvpn_cli.py --server=it123.nordvpn.tcp443.ovpn       Connects to specified server descriptor
'''


def trace(msg_type, text):
    """
    Prints text to stdout
    :param: Message type
    :param: Message text
    """
    types = ["[I]", "[W]", "[E]"]
    print "{type} - {message}".format(type=types[msg_type], message=text)

def print_country_codes_table(country_codes):
    """
    Prints the country codes as table
    :param country_codes: The country codes table
    """
    table_data = [['ISO 3166-1\r\nalpha2', 'Name']]
    for key in sorted(country_codes):
        table_data.append([key, country_codes[key]])

    table = AsciiTable(table_data)
    print table.table

def print_servers_table(servers):
    """
    Prints the nordvpn servers
    :param servers: The nordvpn servers
    """
    table_data = [['Type', 'Country', 'Domain', 'Load', 'TCP', 'UDP']]
    for server in servers['servers']:
        table_data.append([servers['type'], server['country'], \
                          server['domain'], server['load'], \
                          server['feature']['tcp_file'], \
                          server['feature']['udp_file']])

    table = AsciiTable(table_data)
    print table.table

def check_nordvpn_config_folder():
    """
    Checks the config folder
    :return : True if present, otherwise False
    """
    return os.path.exists(__NORDVPN_CONFIG_CLI_PATH__)


def fetch_nordvpn_server(server_type,
                         server_country,
                         server_sort={'enable':False, 'key':None, 'reverse':False}):
    """
    Gets the NordVPN servers State
    :param server_type: The server type
    :param server_country: The server country
    :param server_sort: Sort property
    :return: The available servers
    """

    result = {}
    # Sets the default parameter if are none
    server_type = __NORDVPN_SERVER_TYPES__['svpn'] if server_type is None \
                                                   else __NORDVPN_SERVER_TYPES__[server_type]
    server_country = __NORDVPN_SERVER_COUNTRY__['us'] if server_country is None else server_country

    query_string = {'group' : server_type, 'country' : __NORDVPN_SERVER_COUNTRY__[server_country], \
                    'action' : 'getGroupRows'}
    full_url = "{base_url_api}{querystring}".format(base_url_api=__NORDVPN_REST_API_URL__, \
                                                        querystring=urllib.urlencode(query_string))
    http_request = requests.get(full_url)
    if http_request.status_code == __HTTP_RESPONSE_CODE_OK__:
        json_response = http_request.text
        deserialized_json = json.loads(json_response)
        result['servers'] = deserialized_json
        result['type'] = server_type
        if len(result['servers']) > 0:
            # Apply the config filename
            for server in result['servers']:
                if server['feature']['openvpn_tcp'] is True:
                    server['feature']['tcp_file'] = "{}{}".format(server['domain'],\
                                                                       ".tcp443.ovpn")
                else:
                    server['feature']['tcp_file'] = "n.d."

                if server['feature']['openvpn_udp'] is True:
                    server['feature']['udp_file'] = "{}{}".format(server['domain'], \
                                                                 ".udp1194.ovpn")
                else:
                    server['feature']['udp_file'] = "n.d."

            # Apply sorting
            if server_sort['enable'] is True:
                result['servers'] = sorted(result['servers'], \
                                           key=lambda server: server[server_sort['key']], \
                                           reverse=server_sort['reverse'])
                    

    return result

def download_nordvpn_config():
    """
    Creates and downloads the nordvpn config files
    :return: True if downloaded or already present
    """
    result = False
    try:
        #if os.path.exists(__NORDVPN_CONFIG_CLI_PATH__) is not True:
        is_config_folder_present = check_nordvpn_config_folder()
        if is_config_folder_present is not True:
            os.mkdir(__NORDVPN_CONFIG_CLI_PATH__)
            trace(__INFO_MSG__, "{} folder created".format(__NORDVPN_CONFIG_CLI_PATH__))

            trace(__INFO_MSG__, "Downloading {} config file..".format(__NORDVPN_CONFIG_CLI_FILE__))
            config_package = urllib2.urlopen(__NORDVPN_CONFIG_PACKAGE_URL__)

            with open(__NORDVPN_CONFIG_CLI_FILE__, 'wb') as output_stream:
                output_stream.write(config_package.read())
            trace(__INFO_MSG__, "{} config file downloaded!".format(__NORDVPN_CONFIG_CLI_FILE__))

            zip_ref = zipfile.ZipFile(__NORDVPN_CONFIG_CLI_FILE__, 'r')
            zip_ref.extractall(__NORDVPN_CONFIG_CLI_PATH__)
            zip_ref.close()
        result = True

    except OSError as os_error:
        print os_error.strerror

    return result

def check_openvpn(openvpn_path):
    """
    Check the openvpn client version
    :param openvpn_path: OpenVPN client Path
    :return: is_present
    """
    is_present = False

    try:
        output = subprocess.Popen(openvpn_path, stdout=subprocess.PIPE)
        cmd_out, cmd_err = output.communicate()
        if cmd_err is None:
            regex_match = re.search(r"\OpenVPN (?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)", cmd_out)
            version = regex_match.group(0)
            trace(__INFO_MSG__, "OpenVPN Found: {}".format(version))
            is_present = True
    except OSError as os_error:
        trace(__ERROR_MSG__, "OpenVPN Not Found!")
        print os_error.strerror

    return is_present

def connect_openvpn(nordvpn_config_file):
    """
    Starts OpenVPN with specified nordvpn config file
    :param nordvpn_server: The NordVPN selected server
    """
    trace(__INFO_MSG__, "Connecting to {} server...".format(nordvpn_config_file))
    command = "{openvpn_path} --config {config_path}{config_file}".format(\
                                        openvpn_path=__OPENVPN_PATH__, \
                                        config_path=__NORDVPN_CONFIG_CLI_PATH__, \
                                        config_file=nordvpn_config_file)
    
    subprocess.call(['bash', '-c', "ip route del 0.0.0.0/1 via 192.168.0.1"])
    
    subprocess.call(['bash', '-c', command])

def main():
    """
    Main Function
    """
    
    print_banner()
    
    is_openvpn_present = check_openvpn(__OPENVPN_PATH__)

    if is_openvpn_present is True:
        is_valid_config_folder = download_nordvpn_config()

        if is_valid_config_folder is not True:
            sys.exit(__DOWNLOAD_CONFIG_ERROR__)
    else:
        sys.exit(__OPENVPN_NOT_FOUND__ERROR__)

    if print_country_codes is True:
        print_country_codes_table(__NORDVPN_SERVER_COUNTRY__)
 
    elif nordvpn_country is not None and print_servers is not None:
        country_servers = fetch_nordvpn_server(server_country=nordvpn_country,
                                               server_type=nordvpn_type)
        if country_servers is not None:
            print_servers_table(country_servers)

    elif nordvpn_country is not None and \
         print_servers is None:

        country_servers = fetch_nordvpn_server(server_country=nordvpn_country,
                                               server_type=nordvpn_type,
                                               server_sort={'enable':True, 'key':'load', 'reverse':False})

        if country_servers is not None:
            connect_openvpn(country_servers['servers'][0]['feature']['tcp_file'])

    elif nordvpn_server is not None:
        connect_openvpn(nordvpn_server)

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hs:c:t:",
                                   ["server=", "country=", "type=", \
                                    "country-codes","print-servers"])
        for opt, arg in opts:
            if opt == '-h':
                print_usage()
                sys.exit()
            elif opt in ("-s", "--server"):
                nordvpn_server = arg
            elif opt in ("-c", "--country"):
                nordvpn_country = str(arg).lower()
            elif opt in ("-t", "--type"):
                nordvpn_type = str(arg).lower()
            elif opt == '--print-servers':
                print_servers = True
            elif opt == '--country-codes':
                print_country_codes = True

        main()

    except getopt.GetoptError:
        print_usage()
        sys.exit(__ARGUMENT_PARSING_ERROR__)
