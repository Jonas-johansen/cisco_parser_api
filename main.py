# Simple Network Automation API
# Developed by Jonas Skaret Johansen, NH Data
# Not yet designed for heavy workloads.
from fastapi import FastAPI, Form, File, Request
from api import ParseCLIOutput, RunDeviceCommand, RunCommand, RunDeviceCommandThreading, ionix_backend
import os
app = FastAPI()


# Allow user to send in CLI Data annd send parser .json output in return
@app.post('/cli_parser')
async def ParserEndpoint(platform: str = Form(), command: str = Form(), cli_output: str = Form()):
    return ParseCLIOutput(platform, command, cli_output) # Runs function ParseCLIOutput as found in api/parse.py

# Excecute a command on a device. Devices are configured in config.ini
@app.post('/do_device_command')
async def DoDeviceCommandEndpoint(devices: str = Form(), commands: str = Form(), enable_mode: bool = Form(), parse: bool = Form(), conft: bool = Form()):
    return RunDeviceCommand(devices, commands, enable_mode, parse, conft)

# Excecute a command on a host directly. No validation is added.
@app.post('/do_command')
async def DoCommandEndpoint(device_type: str = Form(), host: str = Form(), username: str = Form(), password: str = Form(), secret: str = Form(), commands: str = Form(), enable_mode: bool = Form(), parse: bool = Form(), conft: bool = Form()):
    return RunCommand(device_type, host, username, password, secret, commands, enable_mode, parse, conft)

# Excecute a command on a device, connects to each device with a thread. Devices are configured in config.ini
@app.post('/do_device_command_threading')
async def DoDeviceCommandThreadingEndpoint(devices: str = Form(), commands: str = Form(), enable_mode: bool = Form(), parse: bool = Form(), conft: bool = Form()):
    return RunDeviceCommandThreading(devices, commands, enable_mode, parse, conft)
# 1 device connect failure will return a error 400 for the whole batch. I will fix this soon, but be aware atm.

@app.post('/ionix_backend')
async def ionix_backend_endpoint(request: Request):
    data = await request.json()
    devices = data["devices"]
    commands = data["commands"]
    conft = data["conft"]
    enable = data["enable"]
    parsing = data["parsing"]
    print(devices, commands, enable, conft, parsing)
    result = ionix_backend(devices, commands, enable, parsing, conft)
    return result
