## Do Device Command
The Do Device Command is for excecuting commands on Network devicess configured in the config.ini file.

There is two endpoints here.

- /do_device_command
- /do_device_command_threading

The only difference between the two is that _threading creates a thread for each device it connects to. 
Thus, this is optimal when excecuting commands on several devices at a time.


<b>How to use</b>

Send a post request with form data.
It should contain.

- <code>devices</code> | As string, seperate several with a comma example "device1,device2"
- <code>commands</code> | As string, seperate several with a comma example "command1,command2"
- <code>enable_mode</code> | As bool, if it is True it will activate enable mode when excecuting commands.
- <code>parse</code> | As bool, if it is True it will return the result in a parsed .json format, as long as the command is supported. If else it will return raw cli output.
- <code>conft</code> | As bool, if it is True it will execute the commands in configure terminal.


Example request:

```py

import requests

url = "http://localhost:8000/do_device_command"
form_data = {
    "devices": "example1",
    "commands": "show clock,clock set 01:00:00 29 december 2022,show clock",
    "enable_mode": True,
    "parse": True,
    "conft": False
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=form_data, headers=headers)
print(response.json())

```

This will return:

```json
[
    [
        [
            {
                'time': '23:10:57.377',
                'timezone': 'UTC',
                'dayweek': 'Wed',
                'month': 'Dec',
                'day': '28', 
                'year': '2022'
            }
        ],
         '', 
         [
            {
                'time': '01:00:00.083',
                'timezone': 'UTC',
                'dayweek': 'Thu',
                 'month': 'Dec',
                  'day': '29',
                   'year': '2022'
            }
        ]
    ]
]
```
As you can see, the time was changed after running the show clock command a second time.

The Do Device Command will return in a following format:
```py
    for device in devices:
        for command_output in command_outputs:
            print(command_output)
```

Example with multiple devices, using threading:

```py

import requests

url = "http://localhost:8000/do_device_command_threading"
form_data = {
    "devices": "example1,example2",
    "commands": "show clock,clock set 01:00:00 29 december 2022,show clock",
    "enable_mode": True,
    "parse": True,
    "conft": False
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=form_data, headers=headers)
print(response.json())
```
This will return:
```json
[
   [
      [
         {
            "time":"01:01:01.817",
            "timezone":"UTC",
            "dayweek":"Thu",
            "month":"Dec",
            "day":"29",
            "year":"2022"
         }
      ],
      "",
      [
         {
            "time":"01:00:00.083",
            "timezone":"UTC",
            "dayweek":"Thu",
            "month":"Dec",
            "day":"29",
            "year":"2022"
         }
      ]
   ],
   [
      [
         {
            "time":"23:17:24.907",
            "timezone":"UTC",
            "dayweek":"Wed",
            "month":"Dec",
            "day":"28",
            "year":"2022"
         }
      ],
      "",
      [
         {
            "time":"01:00:00.079",
            "timezone":"UTC",
            "dayweek":"Thu",
            "month":"Dec",
            "day":"29",
            "year":"2022"
         }
      ]
   ]
]
```
As you can see here it gives the output from both devices. It will return the output in witch the order it is given. For example, example1 device comes first and example2 comes second.


Here is the .ini file for example1 and example2
```ini

[DEFAULT]
username = nhadmin 
password = jonas123
secret = jonas321
; You can also set device_type default if your network only consists of the same device type.
; device_type = cisco_ios_telnet

[example1]
host = 192.168.50.250
device_type = cisco_ios

; unique ID for you equipment. It is best practise to use hostname here.
[example2]
host = 192.168.50.251
device_type = cisco_ios
; if you need to override default values, do this.
; secret = jonas321 
```

Now what happens if it fails to connect to a device?
Well you get an HTTP 400 error, example:

```json
{
    "detail":"Failed to connect to 192.168.50.250: Authentication to device failed.\n\nCommon causes of this problem are:\n1. Invalid username and password\n2. Incorrect SSH-key file\n3. Connecting to the wrong device\n\nDevice settings: cisco_ios 192.168.50.250:22\n\n\nAuthentication failed."
}

```
