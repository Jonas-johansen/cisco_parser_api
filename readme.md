# Simple Network Automation API

The API is a tool that allows you to connect to and execute commands on network equipment, as well as parse the output into a JSON format. It was primarily developed for personal use, so it might not be right for your network / setup.

Please note that the API is somewhat slow, so it may not be suitable for real-time applications. The parsing module is relatively fast, taking about 20 milliseconds, but creating a session with each network device and executing a command can take anywhere from 1-2 seconds with SSH or 2-3 seconds with Telnet. By using the do_device_command_threading module it will use pythons threading library to connect to several devices at the same time. Witch greatly improve load times when excecuting mass commands on several devices.


The API currently has two functions:
- Login to network equipment, execute a commands, and parse the output to JSON | It can connect to several devices at the same time.
- Parse CLI output to JSON (you provide the CLI output in any way you like then post it to the api)
You can configure the network equipment in the config.ini file, or you can set up a database to replace the .ini file. More documentation on these options will be provided soon.

This project uses Netmiko and ntc-templates, and all credit goes to their creators for creating such amazing projects.
I strongly recommend checking out both Netmiko and ntc-templates before using this project.

Please be aware: Be VERY VERY carefull using this API in production, especially with enable and conft mode!!

To run the API, use uvicorn, or use the provided docker image if needed.

Example post:

```py
import requests

url = "http://api.local/cli_parser"
form_data = {
    "platform": "cisco_ios",
    "command": "show interface",
    "cli_output": """GigabitEthernet4 is administratively down, line protocol is down
  Hardware is iGbE, address is 5d6a.e6f5.38f2 (bia 5d6a.e6f5.38f2)
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Auto Duplex, Auto Speed, media type is RJ45"""
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=form_data, headers=headers)
print(response.status_code)
print(response.json())

```

Example response:
```json
[
    {
        "interface": "GigabitEthernet4",
        "link_status": "administratively down",
        "protocol_status": "down",
        "hardware_type": "iGbE",
        "address": "5d6a.e6f5.38f2",
        "bia": "5d6a.e6f5.38f2",
        "description": "",
        "ip_address": "",
        "mtu": "1500",
        "duplex": "Auto Duplex",
        "speed": "Auto Speed",
        "media_type": "RJ45",
        "bandwidth": "1000000 Kbit",
        "delay": "10 usec",
        "encapsulation": "ARPA",
        "last_input": "",
        "last_output": "",
        "last_output_hang": "",
        "queue_strategy": "",
        "input_rate": "",
        "output_rate": "",
        "input_packets": "",
        "output_packets": "",
        "input_errors": "",
        "crc": "",
        "abort": "",
        "output_errors": "",
        "vlan_id": "",
        "vlan_id_inner": "",
        "vlan_id_outer": ""
    }
]
```
In this case, you can see only about half of the interface cli output was provided, therefore alot of the fields are empty.

Developed by Jonas Skaret Johansen, https://nh-data.no. 
You are free to use and modify the project as you see fit.






