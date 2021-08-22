#!/usr/bin/env python3
from objects import *
import pyfiglet

# Major function #1
def config_generator(hport):
    lines = ["CONTROLLER_SERVER_USER=" + server_user, "DOMAIN=" + controller_ip, "RPORT=" + str(hport), "PI_USER=" + pi_user, "CONNCHECK=" + conn_check]
    if os.path.exists(config_dir + sidedoor_conf):
        copyfile(config_dir + sidedoor_conf, config_dir + sidedoor_conf + ".bak")    #Backup previous configuration file
    append_to_file(config_dir + sidedoor_conf, lines) #Append configuration lines

#Major function #2
def script_push(pi_user, raspberry_ip):
    cmd1="scp -rp " + payload + " " + pi_user + "@" + raspberry_ip + ":/home/" + pi_user + "/"
    cmd2="scp -rp " + config_dir + sidedoor_conf + " " + pi_user + "@" + raspberry_ip + ":/home/" + pi_user + "/"
    cmd3="ssh " + pi_user + "@" + raspberry_ip + " \'" + "sudo tar -xzvf sidedoor-pack.tar.gz && chmod +x sidedoor-pack/nbn-pi-deploy.sh" "\'"
    cmd4="ssh " + pi_user + "@" + raspberry_ip + " \"" +"sudo mv " + "/home/" + pi_user + "/" + sidedoor_conf + " /etc/sidedoor/sidedoor.conf" "\""
    print("Running: ", cmd1)
    run(cmd1)
    print("Running: ", cmd2)
    run(cmd2)
    print("Running: ", cmd3)
    run(cmd3)
    print("Running: ", cmd4)
    run(cmd4)
    print("Finished running script_push")

def runtime(id, hport):
    if os.path.exists(csv_database) == False:
        run(str("touch " + csv_database))
    id = row_index(csv_database)
    print(pyfiglet.figlet_format("NBN-Pi"))
    print("Credits: Nassim Bentarka | GitHub: @nassimosaz\n\nThis script configures the RPi to be deployed for a given company.\n")
    raspberry_ip = input("Please enter the Raspberry Pi IP or hostname: ")
    company_name = input_inquire(company_list,"Please choose the company name:")
    hport = hport + id
    config_generator(hport) #Main Element #1
    script_push(pi_user, raspberry_ip) #Main Element #2
    csv_append(csv_database,id, hport, company_name)
    testing()

if __name__ == '__main__':
    runtime(id, hport)