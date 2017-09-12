# NordVPN_CLI
Sintax: nordvpn_cli.py [--country=COUNTRY]\[--print-servers\]\[--country-codes\]\[--server=\]<br>
Options:<br>
**--country:** Uses the server with lowest load of the selected Country<br>
**--print-servers:** Gets all servers of the selected Country<br>
**--country-codes:** Gets all country codes in ISO 3166-1 alpha2 format<br>
**--server:** Connects to specified ovpn file server descriptor<br>
Examples:<br>
**nordvpn_cli.py --country=IT --print-servers:** Prints all Standard VPN Italian Servers<br>
**nordvpn_cli.py --country=IT:** Connects to the best Italian Server<br>
**nordvpn_cli.py --country-codes:** Prints ISO 3166-1 alpha2 table<br>
**nordvpn_cli.py --server=it123.nordvpn.tcp443.ovpn:** Connects to specified server descriptor

