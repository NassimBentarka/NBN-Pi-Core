## PARAMETERS -- EDIT BEFORE USE ##
controller_ip="example.ddns.net"
server_user="administrator"
pi_user="ubuntu"
conn_check="cloudflare.com" # Used by the RPi to periodically check DNS and Internet connectivity. Use any reliable/fast-resolvable domain name.
hport=22000 # The first port in the series to be used as a seed (hport stands for "host port")

## PATHS -- ONLY EDIT IF YOU KNOW WHAT YOU ARE DOING ##
config_dir="generated-config/" # Target directory to append generated config files
sidedoor_conf="sidedoor.conf" # Sidedoor config file to be generated
csv_database= "database/hosts.csv" # Path to the hosts CSV database file
company_list= "database/clients.csv" # Path to the clients CSV database file
payload="payload/sidedoor-pack.tar.gz"