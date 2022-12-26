import os
from ntc_templates.parse import parse_output
from netmiko import ConnectHandler

from fastapi import FastAPI, Form

app = FastAPI()

# Cisco Device Parser - API
# Developed by Jonas Skaret Johansen, NH Data

def run_cisco_command(host, command):
    cisco_device = { 
        "device_type": "cisco_ios_telnet", # for ssh use cisco_ios instead. (telnet is a bit faster)
        "host": host,
        "username": "jonas", # Username for device
        "password": 'jonas123',
        "secret": "jonas123" # Password for device
    }
    with ConnectHandler(**cisco_device) as net_connect:
        net_connect.enable()
        output = net_connect.send_command(command)
    return output


supported_show_commands = ['show logging','show environment temperature','show version','show license','show hosts summary','show snmp community','show ip prefix-list','show interfaces', 'show ip bgp summary', 'show ip route', 'show mac-address-table', 'show ip arp']

@app.post('/zeroinput_showcommand')
async def shcommand(device: str = Form(), command: str = Form()):
    if command in supported_show_commands:
        data = run_cisco_command(device, command)
        command_parsed = parse_output(platform="cisco_ios", command=command, data=data)
        return command_parsed
    else:
        return "Command not supported for parsing, please make sure to write entire command. Supported commands: " + ", ".join(supported_show_commands)

@app.post('/unparsed_command')
async def unparsedcmd(device: str = Form(), command: str = Form()):
    return run_cisco_command(device, command)

@app.post('/show_ip_interface')
async def showipint(device: str = Form(), interface: str = Form()):
    command = "show ip interface " + interface
    data = run_cisco_command(device, command)
    ip_int_parsed = parse_output(platform="cisco_ios", command="show ip interface", data=data)
    return ip_int_parsed


@app.post('/do_traceroute')
async def dotraceroute(device: str = Form(), destination: str = Form()):
    command = "traceroute " + destination
    data = run_cisco_command(device, command)
    traceroute_parsed = parse_output(platform="cisco_ios", command="traceroute", data=data)
    return traceroute_parsed

