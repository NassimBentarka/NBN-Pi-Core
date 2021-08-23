#!/bin/bash
#Usage: ./nbn-pi.sh [raspberry_ip]

# Exit when a command fails
set -e

## READ VARIABLES FROM "config.py" ##
python_script='
import sys
d = {}                                    # create a context for variables
exec((open(sys.argv[1], "r").read()), d)  # execute the Python code in that context
for k in sys.argv[2:]:
  print("%s\0" % str(d[k]).split("\0")[0]) # ...and extract your strings NUL-delimited
'
read_python_vars() {
  local python_file=$1; shift
  local varname
  for varname; do
    IFS= read -r -d '' "${varname#*:}"
  done < <(python3 -c "$python_script" "$python_file" "${@%%:*}")
}

read_python_vars config.py pi_user server_user controller_ip

server_user=$(echo -n "${server_user//[[:space:]]/}")
controller_ip=$(echo -n "${controller_ip//[[:space:]]/}")

echo -e "\033[33mCopying the local SSH identity to $pi_user@$1...\033[0m"
ssh-copy-id $pi_user@$1
echo -e "\033[33mRemotely adding the user '$pi_user' to sudoers...\033[0m"
ssh -t $pi_user@$1 'SSH_OPTS="-F /dev/null" sudo echo ""'%$pi_user'"  ALL=(ALL:ALL) NOPASSWD:ALL" | sudo EDITOR="tee -a" visudo'
echo -e "\033[33mRemotely generating an SSH key on $pi_user@$1...\033[0m"
ssh -t $pi_user@$1 "ssh-keygen -t ed25519 -a 100"
echo -e "\033[33mRemotely copying the $pi_user@$1 SSH identity to $server_user@$controller_ip...\033[0m"
ssh -t $pi_user@$1 'SSH_OPTS="-F /dev/null" ServerUser="'$server_user'" && ControllerIP="'$controller_ip'" && ssh-copy-id $ServerUser@$ControllerIP'
echo -e "\033[33mCopying the local SSH identity to $server_user@$controller_ip...\033[0m"
ssh-copy-id $server_user@$controller_ip
ssh -t $server_user@$controller_ip 'SSH_OPTS="-F /dev/null" sudo echo ""'%$server_user'" ALL=(ALL:ALL) NOPASSWD:ALL" | sudo EDITOR="tee -a" visudo'
#ssh -t $1@$2 'sudo echo ""'%$(whoami)'"  ALL=(ALL:ALL) NOPASSWD:ALL" | sudo EDITOR='tee -a' visudo'
echo -e "\033[33mRunning main.py...\033[0m"
python3 main.py $1