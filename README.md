# NordVPN_Cli - GNU/Linux NordVPN Client

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
```
NordVPN_Cli is ready to use! :+1:

### Example of connection:

```bash 
$ ./nordvpn_cli.py --country=IT
NordVPN CLI
Version: 1.0.0
Author: killerbyte
Email: killerbyte[at]protonmail[dot]com
Twitter: @killerbyte

[I] - OpenVPN Found: OpenVPN 2.4.3
[I] - Connecting to it13.nordvpn.com.tcp443.ovpn server...
Thu Sep 14 21:44:28 2017 OpenVPN 2.4.3 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Jun 30 2017
Thu Sep 14 21:44:28 2017 library versions: OpenSSL 1.0.2l  25 May 2017, LZO 2.08
Enter Auth Username: ************
Enter Auth Password: ************
........
Thu Sep 14 21:44:44 2017 /sbin/ip addr add dev tun0 10.7.7.43/24 broadcast 10.7.7.255
Thu Sep 14 21:44:44 2017 /sbin/ip route add 95.141.36.10/32 via 192.168.1.1
Thu Sep 14 21:44:44 2017 /sbin/ip route add 0.0.0.0/1 via 10.7.7.1
Thu Sep 14 21:44:44 2017 /sbin/ip route add 128.0.0.0/1 via 10.7.7.1
Thu Sep 14 21:44:44 2017 Initialization Sequence Completed
```
