import sys
import logging
import json
import configparser
from PyViCare.PyViCare import PyViCare

config = configparser.ConfigParser()
config.read("config.ini")

client_id = config["credentials"]["client_id"]
email = config["credentials"]["email"]
password = config["credentials"]["password"]

print(client_id)
print(email)
print(password)

vicare = PyViCare()
vicare.initWithCredentials(email, password, client_id, "token.save")

i = 0
for d in vicare.devices:
    print(d.getModel())

    with open(f"dump{i}.json", mode='w') as output:
        output.write(vicare.devices[i].dump_secure())
        # dump including "secrets"
        # output.write(json.dumps(vicare.devices[i].get_raw_json(), indent=4, sort_keys=True))
    
    i = i+1


