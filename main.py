# Simple Network Automation API
# Developed by Jonas Skaret Johansen, NH Data
# Not yet designed for heavy workloads.
from fastapi import FastAPI, Form, HTTPException
from api import ParseCLIOutput, RunDeviceCommand, RunCommand, RunMassDeviceCommand

app = FastAPI()


# Allow user to send in CLI Data annd send parser .json output in return
@app.post('/cli_parser')
async def ParserEndpoint(platform: str = Form(), command: str = Form(), cli_output: str = Form()):
    return ParseCLIOutput(platform, command, cli_output) # Runs function ParseCLIOutput as found in api/parse.py

# Excecute a command on a device. Devices are configured in config.ini
@app.post('/do_device_command')
async def DoDeviceCommandEndpoint(device: str = Form(), command: str = Form(), parsing: bool = Form()):
    return RunDeviceCommand(device, command, parsing)

# Excecute a command on a host directly. No validation is added.
@app.post('/do_command')
async def DoCommandEndpoint(host: str = Form(), username: str = Form(), password: str = Form(), secret: str = Form(), device_type: str = Form(), command: str = Form(), enable_mode: bool = Form()):
    return RunCommand(host, username, password, secret, device_type, command, enable_mode)

@app.post('/do_mass_device_command')
async def DoMassDeviceCommand(devices: str = Form(), command: str = Form(), enable_mode: bool = Form(), parse: bool = Form()):
    return RunMassDeviceCommand(devices, command, enable_mode, parse)