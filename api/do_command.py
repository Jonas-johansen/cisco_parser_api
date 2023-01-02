import logging
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import configparser
from fastapi import HTTPException
import os

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
    print(commands)
    lst = commands.split(',')
    for command in lst:
        if conft:
            output = do_config(nc, commands)
        else:
            output = nc.send_command(command, use_textfsm=parse)
        outputs.append(output)
    return outputs

def do_config(nc, commands):
    lst = commands.split(',')
    output = nc.send_config_set(lst)
    output += nc.save_config()
    return output


def get_device_config(device_name):
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config[device_name]


def RunCommand(device_type, host, username, password, secret, command, enable, parse, conft):
    with connect_to_device(device_type, host, username, password, secret) as nc:
        return run_commands(nc, command, enable, parse, conft)
        
        
def RunDeviceCommand(devices, commands, enable, parse, conft):
    outputs = []
    lst = devices.split(',')
    for device in lst:
        config_device = get_device_config(device)
        with connect_to_device(**config_device) as nc:
            output = run_commands(nc, commands, enable, parse, conft)
        outputs.append(output)
    return outputs

        
        
from concurrent.futures import ThreadPoolExecutor

def RunDeviceCommandThreading(devices, commands, enable, parse, conft):
    def connect_to_device_and_run_commands(device):
        config_device = get_device_config(device)
        try:
            with connect_to_device(**config_device) as nc:
                output = run_commands(nc, commands, enable=enable, parse=parse, conft=conft)
            return output
        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            return f"Failed to connect to {device}: {e}"

    lst = devices.split(',')
    with ThreadPoolExecutor() as executor:
        results = [executor.submit(connect_to_device_and_run_commands, device) for device in lst]
    return [result.result() for result in results]

        
def ionix_backend(devices, commands, enable, parse, conft):
    def connect_to_device_and_run_commands_ionix(device):
        try:
            with connect_to_device(**device) as nc:
                output = run_commands_ionix(nc, commands, enable=enable, parse=parse, conft=conft)
            return output
        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            return f"Failed to connect to {device}: {e}"

    with ThreadPoolExecutor() as executor:
        results = [executor.submit(connect_to_device_and_run_commands_ionix, device) for device in devices]
    return [result.result() for result in results]


def run_commands_ionix(nc, commands, enable, parse, conft):
    if enable:
        nc.enable()
    outputs = []
    for command in commands:
        if conft:
            output = do_config_ionix(nc, commands)
        else:
            output = nc.send_command(command, use_textfsm=parse)
        outputs.append(output)
    return outputs

def do_config_ionix(nc, commands):
    output = nc.send_config_set(commands)
    output += nc.save_config()
    return output


def get_running_config_intro(devices):
    def connect_to_device_and_get_config(device):
        try:
            with connect_to_device(**device) as nc:
                output = get_device_config(nc)
            return output
        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            return f"Failed to connect to {device}: {e}"
    with ThreadPoolExecutor() as executor:
        results = [executor.submit(connect_to_device_and_get_config, device) for device in devices]
    return [result.result() for result in results]


def get_device_config(nc):
    nc.enable()
    output = nc.send_command('show running-config', use_ttp=True, ttp_template='parsing_templates/show_running.ttp')
    return output

