#!/bin/bash
: '
NordVPN_CLI
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
'

if [ ! -z "$1" ] && [ ! -z "$2" ]; then
    option=$1
    nordvpn_server_domain=$2
    # Gets the default gateway
    default_gw=$(route | awk '/default/ && /UG/ {print $2}')

    if [ $option == "-a" ]; then
        # Adds the connection rule only for nordvpn_server
        route add -host $nordvpn_server_domain gw $default_gw
        if [ $? -eq 0 ]; then
            # Add the reject connections rule
            route add -net 0.0.0.0/0 gw $default_gw metric 10 reject
        fi
    elif [ $option == "-d" ]; then
        # Removes the reject rule
        route del -net 0.0.0.0/0 gw $default_gw metric 10 reject
        # Removes nordvpn_server rule
        route del -host $nordvpn_server_domain gw $default_gw 
    else
        echo "Invalid option, use -a or -d"
    fi

else
    echo "Option not found, use -a or -d [nordvpn_server address]"
fi



