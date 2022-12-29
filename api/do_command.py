import logging
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import configparser
from fastapi import HTTPException


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

# Example using a database instead of config.ini
# import os
# import mysql.connector

# mysql_user = os.getenv('mysql_user', 'root')
# mysql_password = os.getenv('mysql_pass', '123123')
# mysql_database = os.getenv('mysql_db', 'db1')
# mysql_host = os.getenv('mysql_host', 'localhost')
# def get_device_config(device_name):
#     conn = mysql.connector.connect(user=mysql_user, password=mysql_password, host=mysql_host, database=mysql_database)
#     cursor = conn.cursor()
#     query = f"""SELECT
#     hostname as host,
#     device_secret as secret,
#     device_password as password
#     FROM NetworkDevices
#     WHERE hostname = %s
#     """
#     cursor.execute(query, (device_name,))
#     result = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return result[0]

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

        


