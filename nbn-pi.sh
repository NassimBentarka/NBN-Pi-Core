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

ssh-copy-id $pi_user@$1
ssh -t $pi_user@$1 "ssh-keygen -t ed25519 -a 100"
ssh -t $pi_user@$1 'SSH_OPTS="-F /dev/null" ServerUser="'$server_user'" && ControllerIP="'$controller_ip'" && ssh-copy-id ${ServerUser//[[:blank:]]/}@${ControllerIP//[[:blank:]]/}'
#ssh -t $1@$2 'sudo echo ""'%$(whoami)'"  ALL=(ALL:ALL) NOPASSWD:ALL" | sudo EDITOR='tee -a' visudo'
python3 main.py $1