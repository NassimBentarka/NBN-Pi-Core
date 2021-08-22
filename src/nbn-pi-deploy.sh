#!/bin/bash
# Usage: ./nbn-pi-deploy

# Logging script output to nbn-pi-deploy.log for debug purposes
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>nbn-pi-deploy.log 2>&1

# Adding $USER to sudoers and extracting payload
sudo echo '%$(whoami)  ALL=(ALL:ALL) NOPASSWD:ALL' | sudo EDITOR='tee -a' visudo
tar -xzvf nbn-pi-payload.tar.gz

# Installing executables
sudo mv src/sidedoor /usr/bin/
sudo mv src/sidedoor-watchdog /usr/bin/
sudo mv src/sidedoor-zombiekill /usr/bin/
sudo chmod +x /usr/bin/sidedoor*

# Installing configuration files
sudo mv src/config/sidedoor.conf /etc/sidedoor/config/
sudo mv src/config/ssh.conf /etc/sidedoor/config/

# Installing service files
sudo mv src/services/sidedoor-watchdog.service /etc/systemd/system/
sudo mv src/services/sidedoor.service /etc/systemd/system/
sudo systemctl daemon-reload

# Installing & Configuring NetworkManager
sudo apt-get update
sudo apt-get -y install network-manager net-tools

# Setting NetworkManager to manage networking
sudo cat <<'EOF' > /etc/netplan/00-network-manager-all.yaml
network:
    version: 2
    renderer: NetworkManager
EOF
sudo mv 00-network-manager-all.yaml /etc/netplan/
sudo netplan generate && sudo netplan apply
sudo systemctl restart NetworkManager

# Configuring DNS
sudo nmcli con mod "$(sudo nmcli -m multiline -g NAME con show 2>&1 | head -n 1 | sed 's/^NAME://')" ipv4.dns "1.1.1.1 1.0.0.1" ipv4.ignore-auto-dns yes && sudo nmcli connection up "$(sudo nmcli -m multiline -g NAME con show 2>&1 | head -n 1 | sed 's/^NAME://')"
sudo systemctl restart NetworkManager

# Enabling services
sudo systemctl enable sidedoor.service && sudo systemctl enable sidedoor-watchdog.service

# Starting services
sudo systemctl start sidedoor.service && sudo systemctl start sidedoor-watchdog.service

