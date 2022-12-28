from ntc_templates.parse import parse_output
import os.path
from os import path
from fastapi import HTTPException
import re

def ParseCLIOutput(platform, command, cli_output):

    if not os.path.exists('commands/' + platform + '.txt'):

        supported_platforms = os.listdir("commands/")
        supported_platforms_without_ext = [name[:-4] for name in supported_platforms]
        raise HTTPException(status_code=400, detail="Platform not supported. Supported platforms are: "  + ', '.join(supported_platforms_without_ext))
    
    with open('commands/' + platform + '.txt') as f:
        lines = f.readlines()

    supported_commands = [line.strip() for line in lines]
    supported_commands_pattern = "|".join(supported_commands)

    if not re.match(supported_commands_pattern, command):
        raise HTTPException(status_code=400, detail="Command not supported for parsing on this platform. Supported commands for " + platform + " is " + ', '.join(supported_commands)) 

    output = parse_output(platform=platform, command=command, data=cli_output)
    return output

