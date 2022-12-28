# Simple Network Automation API
# Developed by Jonas Skaret Johansen, NH Data
# Not yet designed for heavy workloads.
from fastapi import FastAPI, Form, File
from api import ParseCLIOutput, RunDeviceCommand, RunCommand, RunDeviceCommandThreading
from typing import List
import tempfile
import os
app = FastAPI()

os.environ['TMPDIR'] = os.getcwd()
fd, file_path = tempfile.mkstemp()

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
async def DoCommandEndpoint(device_type: str = Form(), host: str = Form(), username: str = Form(), password: str = Form(), secret: str = Form(), commands: str = Form(), enable: bool = Form(), parse: bool = Form(), conft: bool = Form()):
    return RunCommand(device_type, host, username, password, secret, commands, enable, parse, conft)


@app.post('/do_device_command_threading')
async def DoDeviceCommandEndpointThreading(devices: str = Form(), commands: str = Form(), enable_mode: bool = Form(), parse: bool = Form(), conft: bool = Form()):
    return RunDeviceCommandThreading(devices, commands, enable_mode, parse, conft)

