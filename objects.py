import subprocess
import csv
from csv import DictWriter
import fileinput
from shutil import copyfile
import os.path
from sys import stderr
import inquirer
from config import *
import tarfile

# Define generic functions
def run(cmd):
    a = subprocess.run([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,)
    print(a.stdout.decode('utf-8'))
    print(a.stderr.decode('utf-8'))
    run.exitcode = a.returncode

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

def append_to_file(file_name, lines_to_append, method="w+"):
    # DEFAULT -- To open the file in truncate/overwrite mode use (method = 'w+')
    # To open the file in append & read mode use (method = 'a+')
    with open(file_name, method) as file_object:
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

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

# Define specific functions

def csv_company_append(csv_file, name):
    fields = ['COMPANY NAME']
    dict={'COMPANY NAME':name}
    write_csv(csv_file, fields, dict)

def csv_append(csv_file,id, hport, name):
    fields = ['HOST ID','REVERSE SSH PORT','COMPANY NAME']
    dict={'HOST ID':id,'REVERSE SSH PORT':hport,'COMPANY NAME':name}
    write_csv(csv_file, fields, dict)

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
        csv_company_append(clients_list,name)
        print("\n")
        print(csv_to_list(clients_list))
        print("\n")

def testing():
    status=run("ssh " + str(server_user) + "@" + str(controller_ip) + " \"ssh " + str(pi_user) + "@localhost -p " + str(hport) + " \'echo It Works. --Acknowledged by the RPi\'\"")
    return status

def post_install(raspberry_ip): #Deprecated function
    run("ssh " + pi_user + "@" + raspberry_ip + " \"sudo apt-get update && sudo apt-get -y install network-manager && \"") 
