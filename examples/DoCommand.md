## Do Command
The Do Command is for excecuting commands on a Network device

The do command only has one endpoint:
- /do_command

The Do Command can only connect to 1 device per request, it can do multiple commands however.
If you need to connect to multiple devices at the same time check the DoDeviceCommand


<b>How to use</b>

Send a post request with form data.
It should contain.

- <code>device_type</code> | As string, for example "cisco_ios" or "huawei_vrp". Check a complete list of device type in NetMiko's documentation
- <code>host</code> | As string, hostname/ip of device
- <code>username</code> | As string, login username for ssh.
- <code>password</code> | As string, login password for ssh.
- <code>secret</code> | As string, enable password for device. 
- <code>commands</code> | As string, seperate several with a comma example "command1,command2"
- <code>enable_mode</code> | As bool, if it is True it will activate enable mode when excecuting commands.
- <code>parse</code> | As bool, if it is True it will return the result in a parsed .json format, as long as the command is supported. If else it will return raw cli output.
- <code>conft</code> | As bool, if it is True it will execute the commands in configure terminal.


Example:

```py
import requests
url = "http://localhost:8000/do_command"
form_data = {
    "device_type": "cisco_ios",
    "host": "192.168.50.250",
    "username": "jonas",
    "password": "jonas123",
    "secret": "jonas321",
    "commands": "show clock",
    "enable_mode": True,
    "parse": True,
    "conft": False
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=form_data, headers=headers)
print(response.text)
```
This returns:
```json
[
    [
        {
            "time":"01:13:21.039",
            "timezone":"UTC",
            "dayweek":"Thu",
            "month":"Dec",
            "day":"29",
            "year":"2022"
        }
    ]
]
```
If you disable parsing, it will return:

```json
[
    "01:15:13.419 UTC Thu Dec 29 2022"
]
```

What happends on error? Well you get a HTTP 400 error. Example:
```json
{
    "detail":"Failed to connect to 192.168.50.250: Authentication to device failed.\n\nCommon causes of this problem are:\n1. Invalid username and password\n2. Incorrect SSH-key file\n3. Connecting to the wrong device\n\nDevice settings: cisco_ios 192.168.50.250:22\n\n\nAuthentication failed."
}
```