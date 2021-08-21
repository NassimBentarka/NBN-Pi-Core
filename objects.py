import subprocess
import csv
from csv import DictWriter
import fileinput
from shutil import copyfile
import os.path
import inquirer
from config import *

# Define generic functions
def run(cmd):
    a = subprocess.run([cmd], stdout=subprocess.PIPE, shell=True)
    print(a.stdout.decode('utf-8'))

def csv_to_list(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

def csv_read_cell(csv_file, x, y):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1

def write_csv(csv_file, field_names, dict):
    with open(csv_file, 'a') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        dictwriter_object.writerow(dict)
        f_object.close()

def string_replace(filename, source, dest):
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(source, dest), end='')

def append_to_file(file_name, lines_to_append):
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        appendEOL = False
        # Move read cursor to the start of file.
        file_object.seek(0)
        # Check if file is not empty
        data = file_object.read(100)
        if len(data) > 0:
            appendEOL = True
        # Iterate over each string in the list
        for line in lines_to_append:
            # If file is not empty then append '\n' before first line for
            # other lines always append '\n' before appending line
            if appendEOL == True:
                file_object.write("\n")
            else:
                appendEOL = True
            # Append element at the end of file
            file_object.write(line)

def row_index(csv_file):
    file = open(csv_file)
    reader = csv.reader(file)
    lines = len(list(reader))
    return lines

# Define specific functions

def csv_company_append(csv_file, name):
    fields = ['COMPANY NAME']
    dict={'COMPANY NAME':name}
    write_csv(csv_file, fields, dict)

def csv_append(csv_file,id, hport, name):
    fields = ['HOST ID','REVERSE SSH PORT','COMPANY NAME']
    dict={'HOST ID':id,'REVERSE SSH PORT':hport,'COMPANY NAME':name}
    write_csv(csv_file, fields, dict)

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

def input_inquire(list,message):
    questions = [
    inquirer.List('names',
                    message,
                    choices=csv_to_list(list),
                ),
    ]
    answers = inquirer.prompt(questions)
    answers_str = ' '.join(map(str, answers["names"]))
    return answers_str

def add_company():
    while True:
        name = input("Enter company name: ")
        csv_company_append(company_list,name)
        print("\n")
        print(csv_to_list(company_list))
        print("\n")

def testing():
    status=run("ssh " + server_user + "@" + controller_ip + " \"ssh " + pi_user + "@localhost -p " + hport + " \'echo It Works. --Acknowledged by the RPi\'\"")
    return status

def post_install(raspberry_ip):
    run("ssh " + pi_user + "@" + raspberry_ip + " \"sudo apt-get update && sudo apt-get -y install network-manager && \"") #Obfsucated function
