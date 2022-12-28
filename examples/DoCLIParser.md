# CLI Output parser

This command is when you want to parse an existing CLI output.


<b>How to use</b>

Send a post request with form data.
It should contain.

- <code>platform</code> | As string, this is the platform to parse from. Example "cisco_ios"
- <code>command</code> | As string, this is the command you entered to get your CLI output. Example "show interfaces"
- <code>cli_output</code> | As string, this is the raw cli output from your device.


Example:

```py
import requests

url = "http://localhost:8000/cli_parser"
form_data = {
    "platform": "cisco_ios",
    "command": "show interface GI4",
    "cli_output": """GigabitEthernet4 is up, line protocol is up
  Hardware is iGbE, address is 0087.7493.7608 (bia 0087.7493.7608)
  Description: wan-asusrtr
  Internet address is 192.168.50.250/24
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full Duplex, 1Gbps, media type is RJ45
  output flow-control is unsupported, input flow-control is unsupported
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:00, output 00:00:00, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 4000 bits/sec, 4 packets/sec
  5 minute output rate 3000 bits/sec, 4 packets/sec
     95199 packets input, 10897490 bytes, 0 no buffer
     Received 81667 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog, 21944 multicast, 0 pause input
     76189 packets output, 8745532 bytes, 0 underruns
     0 output errors, 0 collisions, 0 interface resets
     14628 unknown protocol drops
     0 babbles, 0 late collision, 0 deferred
     1 lost carrier, 0 no carrier, 0 pause output
     0 output buffer failures, 0 output buffers swapped out"""
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=form_data, headers=headers)
print(response.json())
```
This responds with:
```json
[
   {
      "interface":"GigabitEthernet4",
      "link_status":"up",
      "protocol_status":"up",
      "hardware_type":"iGbE",
      "address":"0087.7493.7608",
      "bia":"0087.7493.7608",
      "description":"wan-asusrtr",
      "ip_address":"192.168.50.250/24",
      "mtu":"1500",
      "duplex":"Full Duplex",
      "speed":"1Gbps",
      "media_type":"RJ45",
      "bandwidth":"1000000 Kbit",
      "delay":"10 usec",
      "encapsulation":"ARPA",
      "last_input":"00:00:00",
      "last_output":"00:00:00",
      "last_output_hang":"never",
      "queue_strategy":"fifo",
      "input_rate":"4000",
      "output_rate":"3000",
      "input_packets":"95199",
      "output_packets":"76189",
      "input_errors":"0",
      "crc":"0",
      "abort":"",
      "output_errors":"0",
      "vlan_id":"",
      "vlan_id_inner":"",
      "vlan_id_outer":""
   }
]
```

Lets say the command you enter is not supported for parsing. You will then get a error as follows:

```json
{
   "detail":"Command not supported for parsing on this platform. Supported commands for cisco_ios is dir, show access-list, show access-session, show adjacency, show alert counters, show aliases, show ap summary, show archive, show authentication sessions, show bfd neighbors details, show boot, show capability feature, show cdp neighbors, show cdp neighbors detail, show clock, show controller t1, show crypto ipsec sa detail, show crypto session detail, show dhcp lease, show dmvpn, show dot1x all, show environment power all, show environment temperature, show etherchannel summary, show hosts summary, show interfaces, show interfaces description, show interfaces status, show interfaces switchport, show inventory, show ip access-list, show ip arp, show ip bgp, show ip bgp neighbors, show ip bgp neighbirs advertised-routes, show ip bgp summary, show ip bgp vpn4 all neighbors, show ip cef, show ip cef detail, show ip device tracking all, show ip eigrp interfaces detail, show ip eigrp neighbors, show ip eigrp topology, show ip flow toptalkers, show ip interface brief, show ip interface, show ip mroute, show ip nat translations, show ip ospf database, show ip ospf database network, show ip ospf database router, show ip ospf interface brief, show ip ospf neighbor, show ip prefix-list, show ip route, show ip route summary, show ip vrf interfaces, show ipv6 interface brief, show ipv6 neighbors, show ipv6 route, show isdn status, show isis neighbors, show license, show lldp neighbors, show lldp neighbors detail, show logging, show mac-address-table, show module, show online diag, show module status, show module submodule, show mpls interfaces, show object-group, show platform diag, show port-security interface interface, show power avaliable, show power status, show power supplies, show processes cpu, show redundancy, show route-map, show running-config partition access-list, show running-config partition route-map, show snmp community, show snmp group, show snmp user, show spanning-tree, show standby, show standby brief, show switch detail, show switch detail stack ports, show tacacs, show version, show vlan, show vrf, show vrrp all, show vrrp brief, show vtp status, traceroute, show interface, sh int"
}
```

Now lets say your platform isnt supported, it will then return:

```json
{
    "detail": "Platform not supported."
}

```
What if the command and platform is supported, but your output is bad?
It will simply not return a parsed result, however it will not raise an exception.
Example post:
```py
import requests
url = "http://localhost:8000/cli_parser"
form_data = {
    "platform": "cisco_ios",
    "command": "show interface GI4",
    "cli_output": """DUMMY TEXT"""
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=form_data, headers=headers)
print(response.json())

```
Respone:
```json
[]
```