#!/usr/bin/env python3
# Retrieve TLOPO server data

import requests

# reset the selected_account.txt file
with open("./files/selected_account.txt", "w") as sel_user:
    sel_user.write("")
# ------------------------------------------------------------------------------------------
# Retrieves gameserver data and saves it into a file
# ------------------------------------------------------------------------------------------
gameserver_data = (requests.get('https://api.piratesonline.co/shards/')).json()
servers, server_values = [], {}
for server in gameserver_data:
    server_name = gameserver_data[server]['name']
    server_values[server_name] = server
    servers.append(server_name)
servers.sort()

with open("./files/server_data.csv", "w") as serv_file:
    total_population = 0
    for server in servers:
        if gameserver_data[server_values[server]]['available']:
            server_population = gameserver_data[server_values[server]]['population']
            total_population += server_population
    serv_file.write(str(len(servers)) + " " + str(total_population) + "\n")
    for server in servers:
        if not gameserver_data[server_values[server]]['available']:
            serv_file.write(server + ",unavailable,none,none")
        else:
            server_population = str(gameserver_data[server_values[server]]['population'])
            if 'state' not in gameserver_data[server_values[server]]['fleet']:
                serv_file.write(server + ",available," + server_population + ",none")
            else:
                if gameserver_data[server_values[server]]['fleet']['state'] == 'deployed' and \
                gameserver_data[server_values[server]]['fleet']['shipsRemaining'] > 0:
                    fleet_type = (gameserver_data[server_values[server]]['fleet']['type']).upper()
                    ships_remaining = gameserver_data[server_values[server]]['fleet']['shipsRemaining']
                    if ships_remaining == 1:
                        serv_file.write(server + ",available," + server_population + ","
                               + fleet_type + " is deployed. There is 1 ship remaining.")
                    else:
                        serv_file.write(server + ",available," + server_population + "," + fleet_type +
                                    " is deployed. There are " + str(ships_remaining) + " ships remaining.")
        if not server == servers[-1]:
            serv_file.write("\n")