# Simple Network Automation API
# Developed by Jonas Skaret Johansen, NH Data
# Not yet designed for heavy workloads.
from fastapi import FastAPI, Form, HTTPException
from api import ParseCLIOutput, RunDeviceCommand

app = FastAPI()


# Allow user to send in CLI Data annd send parser .json output in return
@app.post('/cli_parser')
async def Parser(platform: str = Form(), command: str = Form(), cli_output: str = Form()):
    return ParseCLIOutput(platform, command, cli_output) # Runs function ParseCLIOutput as found in api/parse.py

# Excecute a command on a device. Devices are configured in config.ini
@app.post('/do_command')
async def DoCommand(device: str = Form(), command: str = Form(), parsing: bool = Form()):
    return RunDeviceCommand(device, command, parsing)

