import os
from ntc_templates.parse import parse_output
from netmiko import ConnectHandler
import configparser
from fastapi import FastAPI, Form, HTTPException

app = FastAPI()

def get_device_config(device_name):
    config = configparser.ConfigParser()
    config.read("config.ini")
    device_config = config[device_name]
    return device_config

# Cisco Device Parser - API
# Developed by Jonas Skaret Johansen, NH Data
# Not yet designed for heavy workloads.
def run_cisco_command(device, command):
    cisco_device = get_device_config(device)
    with ConnectHandler(**cisco_device) as net_connect:
        net_connect.fast_cli = True
        net_connect.enable()
        output = net_connect.send_command(command)
    return output


supported_show_commands = ['show logging','show environment temperature','show version','show license','show hosts summary','show snmp community','show ip prefix-list','show interfaces', 'show ip bgp summary', 'show ip route', 'show mac-address-table', 'show ip arp']


@app.post('/zeroinput_showcommand')
async def shcommand(device: str = Form(), command: str = Form()):
    if not command.startswith("show "):
        raise HTTPException(status_code=400, detail="Command must start with 'show '")
    if command not in supported_show_commands:
        raise HTTPException(status_code=400, detail="Command not supported for parsing. Supported commands: " +
                            ", ".join(supported_show_commands))

    # Run the command and parse the output
    data = run_cisco_command(device, command)
    command_parsed = parse_output(platform="cisco_ios", command=command, data=data)
    return command_parsed

@app.post('/unparsed_command')
async def unparsedcmd(device: str = Form(), command: str = Form()):
    return run_cisco_command(device, command)

@app.post('/show_ip_interface')
async def showipint(device: str = Form(), interface: str = Form()):
    command = f"show ip interface {interface}"
    data = run_cisco_command(device, command)
    ip_int_parsed = parse_output(platform="cisco_ios", command="show ip interface", data=data)
    return ip_int_parsed


@app.post('/do_traceroute')
async def dotraceroute(device: str = Form(), destination: str = Form()):
    command = "traceroute " + destination
    data = run_cisco_command(device, command)
    traceroute_parsed = parse_output(platform="cisco_ios", command="traceroute", data=data)
    return traceroute_parsed

@app.post('/show_ip_route')
async def show_ip_route(device: str = Form(), network: str = Form()):
    command = f"show ip route {network}"
    data = run_cisco_command(device, command)
    route_parsed = parse_output(platform="cisco_ios", command="show ip route", data=data)
    return route_parsed

