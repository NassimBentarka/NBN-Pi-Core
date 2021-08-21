#!/usr/bin/env python3
from objects import *
import pyfiglet

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

runtime(id, hport)
