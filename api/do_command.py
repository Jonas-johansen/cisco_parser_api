import re
import logging
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import configparser
from fastapi import HTTPException
import threading

logging.basicConfig(filename="sessions.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")


def connect_to_device(device_type, host, username, password, secret):
    try: 
        device = {
            "device_type": device_type,
            "host": host,
            "username": username,
            "password": password,
            "secret": secret
        }
        return ConnectHandler(**device)
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        print(f"Failed to connect to {device['host']}: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to connect to {device['host']}: {e}")


def run_commands(nc, commands, enable, parse, conft):
    if enable:
        nc.enable()
    outputs = []
    for command in commands:
        if conft:
            output = nc.send_config(command)
        else:
            output = nc.send_command(command, use_textfsm=parse)
        outputs.append(output)
    return outputs


def get_device_config(device_name):
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config[device_name]


def RunCommand(device_type, host, username, password, secret, command, enable, parse, conft):
    with connect_to_device(device_type, host, username, password, secret) as nc:
        return run_commands(nc, command, enable, parse, conft)
    
def RunDeviceCommand(device, commands, parsing, enable, conft):
    # device_type = get_device_config(device)["device_type"]
    # if parsing:
    #     with open(f"commands/{device_type}.txt") as f:
    #         supported_commands = [line.strip() for line in f.readlines()]
    #     supported_commands_pattern = "|".join(supported_commands)
    #     if not re.match(supported_commands_pattern, commands):
    #         raise HTTPException(
    #             status_code=400,
    #             detail=f"Command not supported for parsing on this platform. Supported commands for {device_type} are {', '.join(supported_commands)}."
    #         )
    device_config = get_device_config(device)
    with ConnectHandler(**device_config) as nc:
        return run_commands(nc, commands, enable, parsing, conft)
        
        
def RunMassDeviceCommand(devices, commands, enable, parse, conft):
    outputs = []
    lst = devices.split(',')
    for device in lst:
        config_device = get_device_config(device)
        with connect_to_device(config_device) as nc:
            output = run_commands(nc, commands, enable, parse, conft)
        outputs.append(output)
    return outputs

        
        
