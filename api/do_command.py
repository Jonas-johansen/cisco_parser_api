from pydantic import BaseModel
from ntc_templates.parse import parse_output
from netmiko import ConnectHandler
import configparser
from fastapi import HTTPException
import re

# For debugging purposes (Creates a debug.log file)
#---
# import logging
# logging.basicConfig(filename="debug.log", level=logging.DEBUG)
# logger = logging.getLogger("netmiko")

# Excecute a command on any device, as long as it is supported by NetMiko
def RunCommand(host, username, password, secret, device_type, command, enable):
    device = {
        "device_type": device_type,
        "host": host,
        "username": username,
        "password": password,
        "secret": secret
    }
    with ConnectHandler(**device) as nc:
        if enable:
            nc.enable()
        output = nc.send_command(command)
    return output


# Import devices.
def get_device_config(device_name):
    config = configparser.ConfigParser()
    config.read("config.ini")
    device_config = config[device_name]
    return device_config

# Run command on presaved device
def RunDeviceCommand(device, command, parsing):
    # Get config by device ID.
    device = get_device_config(device)
    if parsing:
        # Reads commands of platform type.
        with open('commands/' + device['device_type'] + '.txt') as f:
            lines = f.readlines()
        # Remove \n from each item in list    
        supported_commands = [line.strip() for line in lines]
        # Adds to regex list. This is used so that if the command is "show ip interface gi4" it will still match the command "show ip interface"
        supported_commands_pattern = "|".join(supported_commands)
        # Throw exception if the platform does not support parsing of the command as specified.
        if not re.match(supported_commands_pattern, command):
            raise HTTPException(status_code=400, detail="Command not supported for parsing on this platform. Supported commands for " + device['device_type'] + " is " + ', '.join(supported_commands)) 

    match device['device_type']:
        case 'cisco_ios':
            return do_cisco_ios_command(device, command, parsing)
        case 'cisco_ios_telnet':
            return do_cisco_ios_command(device, command, parsing)
        case 'huawei_vrp':
            return do_huawei_vrp_command(device, command, parsing)



# Mass automation

def RunMassDeviceCommand(devices, command, enable, parse):
    outputs = []
    lst = devices.split(',')
    for device in lst:
        config_device = get_device_config(device)
        with ConnectHandler(**config_device) as nc:
            if enable:
                nc.enable()
            output = nc.send_command(command, use_textfsm=parse)
        outputs.append(output)
    return outputs
        


# OS specific commands

def do_cisco_ios_command(device, command, parsing):
    with ConnectHandler(**device) as nc:
        nc.fast_cli = True
        nc.enable() # Activates enable mode. If you only use certain show commands you can remove this. 
        if parsing:
            output = nc.send_command(command, use_textfsm=True) # Uses the ntc-templates library to parse the output to .json. 
                                                                # You can use use_genie=True if you rather want to use the cisco Genie parsers.
                                                                # You can not use both.
        else:
            output = nc.send_command(command)
    return output

