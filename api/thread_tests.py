import threading
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import configparser



def get_device_config(device_name):
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config[device_name]


def run_commands_on_device(device, commands, enable, parse, conft):
    try:
        with ConnectHandler(**device) as nc:
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
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        return (f"Failed to connect to {device['host']}: {e}")

def RunMassDeviceCommand(devices, commands, enable, parse, conft):
    outputs = []
    lst = devices.split(',')
    devices_config = [get_device_config(device) for device in lst]
    with ConnectHandler.from_list(devices_config) as nc:
        threads = []
        for device in nc:
            t = threading.Thread(target=run_commands_on_device, args=(device, commands, enable, parse, conft))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
            outputs.extend(t.result)
    return outputs
