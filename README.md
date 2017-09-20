# NordVPN_Cli - GNU/Linux NordVPN Client
![python_shields](https://img.shields.io/badge/python-2.7-blue.svg) ![pep8_shields](https://img.shields.io/badge/PEP%208-compliant-brightgreen.svg) ![build_pass](https://img.shields.io/travis/rust-lang/rust.svg) ![build_stable](https://img.shields.io/pypi/status/Django.svg)


NordVPN_Cli is an unofficial bash application written in python that helps you to configure and manage all NordVPN servers. 

### Requirements

 * OpenVPN client
 * Python 2.7.x
 * root privilegies
 * Naturally, Internet Connection

### Installation

For first, install all python requirements:
```bash
$ pip install -r requirements.txt
```

With root account, set the execution and SUID bits, otherwise use the sudo command:
```text
# chmod 4755 nordvpn_cli.py
```
This step is required because openvpn must be used with root privilegies

Check the execution running ```./nordvpn_cli.py -h```. You will see an output like this if your installation is correct:
```bash
Sintax: nordvpn_cli.py [--country=COUNTRY][--print-servers][--country-codes][--server=]

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
nordvpn_cli.py --server=it123.nordvpn.tcp443.ovpn --killswitch  Connects to specified server descriptor
```
NordVPN_Cli is ready to use! :+1:

### Example:

[![asciicast](https://asciinema.org/a/2M8XTCKvz4IZw2t1ybEUk4BC9.png)](https://asciinema.org/a/2M8XTCKvz4IZw2t1ybEUk4BC9)
