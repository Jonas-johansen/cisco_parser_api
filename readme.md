# Network CLI Parser API

The API is a tool that allows you to connect to and execute commands on network equipment, as well as parse the output into a JSON format. It was primarily developed for personal use, so it might not be right for your network / setup.

Please note that the API is somewhat slow, so it may not be suitable for real-time applications. The parsing module is relatively fast, taking about 300 milliseconds, but creating a session with each network device and executing a command can take anywhere from 5-10 seconds with SSH or 2-3 seconds with Telnet.

To improve speed, you can create an SSH or Telnet session pool, which maintains a live connection with each network device at all times. However, this may not be practical for large networks. Instead, you could consider creating a temporary pool that keeps the connection open for 10-15 minutes before resetting. This can significantly improve load times when executing multiple commands on the same device, except for the first command. More documentation on these options will be provided soon.


The API currently has two functions:
- Login to network equipment, execute a command, and parse the output to JSON
- Parse CLI output to JSON (you provide the CLI output in any way you like then post it to the api)
You can configure the network equipment in the config.ini file, or you can set up a database to replace the .ini file. More documentation on these options will be provided soon.

This project uses Netmiko and ntc-templates, and all credit goes to their creators for creating such amazing projects.

To run the API, use uvicorn, or use the provided docker image if needed.

Example post:

```py
import requests

url = "http://api.local/parser"
form_data = {
    "platform": "cisco_ios",
    "command": "show interface",
    "clioutput": """GigabitEthernet4 is administratively down, line protocol is down
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

Developed by Jonas Skaret Johansen, https://nh-data.no. You are free to use and modify the project as you see fit.



