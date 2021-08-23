#!/bin/bash
# Usage: ./nbn-pi-deploy

# exit when any command fails
set -e
# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap 'echo "Last command: \"${last_command}\" exited with exit code $?."' EXIT

# Logging script output to nbn-pi-deploy.log for debug purposes
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>nbn-pi-deploy.log 2>&1

# Installing executables
echo -e "\033[33mInstalling executables...\033[0m"
sudo mv src/sidedoor /usr/bin/
sudo mv src/sidedoor-watchdog /usr/bin/
sudo mv src/sidedoor-zombiekill /usr/bin/
sudo chmod +x /usr/bin/sidedoor*

# Installing configuration files
echo -e "\033[33mInstalling configuration files...\033[0m"
sudo mkdir -p /etc/sidedoor/
sudo mv src/config/sidedoor.conf /etc/sidedoor/
sudo mv src/config/ssh.conf /etc/sidedoor/

# Installing service files
echo -e "\033[33mInstalling service files...\033[0m"
sudo mv src/services/sidedoor-watchdog.service /etc/systemd/system/
sudo mv src/services/sidedoor.service /etc/systemd/system/
sudo systemctl daemon-reload

# Installing NetworkManager
echo -e "\033[33mInstalling NetworkManager and net-tools...\033[0m"
sudo apt-get update
sudo apt-get -y install network-manager net-tools

# Setting NetworkManager to manage global networking
echo -e "\033[33mSetting NetworkManager to manage global networking...\033[0m"
sudo cat <<'EOF' > /etc/netplan/00-network-manager-all.yaml
network:
    version: 2
    renderer: NetworkManager
EOF
#sudo mv 00-network-manager-all.yaml /etc/netplan/ ## Plan B if EOF above fails.
sudo netplan generate && sudo netplan apply
sudo systemctl restart NetworkManager

# Configuring DNS servers
echo -e "\033[33mConfiguring DNS servers...\033[0m"
sudo nmcli con mod "$(sudo nmcli -m multiline -g NAME con show 2>&1 | head -n 1 | sed 's/^NAME://')" ipv4.dns "1.1.1.1 1.0.0.1" ipv4.ignore-auto-dns yes && sudo nmcli connection up "$(sudo nmcli -m multiline -g NAME con show 2>&1 | head -n 1 | sed 's/^NAME://')"
sudo systemctl restart NetworkManager

# Enabling services
echo -e "\033[33mEnabling NBN-Pi services...\033[0m"
sudo systemctl enable sidedoor.service && sudo systemctl enable sidedoor-watchdog.service

# Starting services
echo -e "\033[33mStarting NBN-Pi services...\033[0m"
sudo systemctl restart sidedoor.service && sudo systemctl restart sidedoor-watchdog.service
echo -e "\033[32mNBN-Pi deployed successfully!\033[0m"