import requests

url = "http://localhost:8000/cli_parser"
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