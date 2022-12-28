from ntc_templates.parse import parse_output
import os.path
from os import path
from fastapi import HTTPException
import re

def ParseCLIOutput(platform, command, cli_output):
# You could remove all command validation and hope ntc-templates find a match, however i recommend keeping it here so you dont get http 500 errors.
    # Check if platform file exists in command/ folder.
    if not os.path.exists('commands/' + platform + '.txt'):
        # Get all file names from commands/ folder.
        supported_platforms = os.listdir("commands/")
        # Remove the ".txt" extension from each filename
        supported_platforms_without_ext = [name[:-4] for name in supported_platforms]
        raise HTTPException(status_code=400, detail="Platform not supported. Supported platforms are: "  + ', '.join(supported_platforms_without_ext))
    
    # Get contens of file
    with open('commands/' + platform + '.txt') as f:
        lines = f.readlines()

    # Remove \n from each item in list    
    supported_commands = [line.strip() for line in lines]
    supported_commands_pattern = "|".join(supported_commands)
        
    # Throw exception if the platform does not support parsing of the command as specified.
    if not re.match(supported_commands_pattern, command):
        raise HTTPException(status_code=400, detail="Command not supported for parsing on this platform. Supported commands for " + platform + " is " + ', '.join(supported_commands)) 
    
    # Parse cli output using ntc-templates parsing module
    output = parse_output(platform=platform, command=command, data=cli_output)
    return output
