# Genexis Router API

This project connects to the Genexis router and retrieves data from the router.

## Features

- Authorization and session management with the Genexis router
- Retrieve router status and device information
- Fetch IPv4 status, DHCP leases, and reservations
- Reboot the router
- Retrieve firmware information

## Installation

To install this project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/swwgames/genexis_router.git
    ```

2. Navigate to the project directory:
    ```sh
    cd genexis_router
    ```

3. Install the library:
    ```sh
    pip install .
    ```

## Usage

Here's an example of how to use the `GenexisRouter` class to connect to a Genexis router and retrieve status information:

```python
from logging import getLogger
from genexis_router import GenexisRouter

# Initialize the logger (optional)
logger = getLogger(__name__)

# Initialize the GenexisRouter

host = "http://192.168.1.254/api"
username = "admin"
password = "YourPassword"

router = GenexisRouter(host, username, password)
try:
    router.authorize()  # authorizing

    response = router.get_status() # Get status info
    print(response)

    # Get firmware info - returns Firmware
    firmware = router.get_firmware()
    print(firmware)

    # Get Address reservations, sort by ipaddr
    reservations = router.get_ipv4_reservations()
    reservations.sort(key=lambda a: a.ipaddr)
    for res in reservations:
        print(f"{res.macaddr} {res.ipaddr:16s} {'Permanent':12}")

    # Get DHCP leases, sort by ipaddr
    leases = router.get_ipv4_dhcp_leases()
    leases.sort(key=lambda a: a.ipaddr)
    for lease in leases:
        print(f"{lease.macaddr} {lease.ipaddr:16s} {lease.hostname:36} {lease.lease_time:12}")

    router.reboot
    # Reboots the router
finally:
    router.logout()   # Always logout
```
## Functions
| Function | Args | Description | Return |
|---|---|---|---|
| get_firmware |   | Gets firmware info about the router | [Firmware](#firmware) |
| get_status |   | Gets status about the router info including wifi statuses and connected devices info | [Status](#status) |
| get_ipv4_status |   | Gets WAN and LAN IPv4 status info, gateway, DNS, netmask | [IPv4Status](#IPv4Status) |
| get_ipv4_reservations |   | Gets IPv4 reserved addresses (static) | [[IPv4Reservation]](#IPv4Reservation) |
| get_ipv4_dhcp_leases |   | Gets IPv4 addresses assigned via DHCP | [[IPv4DHCPLease]](#IPv4DHCPLease) | 
| reboot |   | reboot router |
| authorize |   | authorize for actions |
| logout |   | logout after all is done |

## Dataclass
### <a id="firmware">Firmware</a>
| Field | Description | Type |
| --- |----|----|
| hardware_version | Returns like - 1.4 | str |
| model | Returns like - Platinum-7840 | str |
| firmware_version | Returns like - geneos-lunar-3.16.0-R | str |

### <a id="status">Status</a>
| Field | Description | Type |
|---|---|---|
| wan_macaddr | router wan mac address | str, None |
| wan_macaddress | router wan mac address | macaddress.EUI48, None |
| lan_macaddr | router lan mac address | str |
| lan_macaddress | router lan mac address | macaddress.EUI48 |
| wan_ipv4_addr | router wan ipv4 address | str, None |
| wan_ipv4_address | router wan ipv4 address | ipaddress.IPv4Address, None |
| lan_ipv4_addr | router lan ipv4 address | str, None |
| lan_ipv4_address | router lan ipv4 address | ipaddress.IPv4Address, None |
| wan_ipv4_gateway | router wan ipv4 gateway | str, None |
| wan_ipv4_gateway_address | router wan ipv4 gateway address | ipaddress.IPv4Address, None |
| clients_total | Total amount of all connected clients | int |
| guest_2g_enable | Is guest wifi 2.4G enabled | bool |
| guest_5g_enable | Is guest wifi 5G enabled | bool, None |
| wifi_2g_enable | Is host wifi 2.4G enabled | bool |
| wifi_5g_enable | Is host wifi 5G enabled | bool, None |
| devices | List of all connectedd devices | list[[Device](#device)] |

### <a id="device">Device</a>
| Field | Description | Type |
| --- |---|---|
| macaddr | client mac address | str |
| macaddress | client mac address | macaddress |
| ipaddr | client ip address | str |
| ipaddress | client ip address | ipaddress |
| hostname | client hostname | str |

### <a id="IPv4Reservation">IPv4Reservation</a>
| Field | Description | Type |
| --- |---|---|
| macaddr | client mac address | str |
| macaddress| client mac address | macaddress |
| ipaddr | client ip address | str |
| ipaddress | client ip address | ipaddress |
| enabled | enabled | bool |

### <a id="IPv4DHCPLease">IPv4DHCPLease</a>
| Field | Description | Type |
| --- |---|---|
| macaddr | client mac address | str |
| macaddress | client mac address | macaddress |
| ipaddr | client ip address | str |
| ipaddress | client ip address | ipaddress |
| hostname | client hostname | str |
| lease_time | ip address lease time | str |

### <a id="IPv4Status">IPv4Status</a>
| Field | Description | Type |
| --- |---|---|
| wan_macaddr | router mac address | str |
| wan_macaddress | router mac address | macaddress |
| wan_ipv4_ipaddr | router mac address | str, None |
| wan_ipv4_ipaddress | router mac address | ipaddress.IPv4Address, None |
| wan_ipv4_gateway | router WAN gateway IP address | str, None |
| wan_ipv4_gateway_address | router WAN gateway IP address | ipaddress.IPv4Address, None |
| wan_ipv4_netmask | router WAN gateway IP netmask | str, None |
| wan_ipv4_netmask_address | router WAN gateway IP netmask | ipaddress.IPv4Address, None |
| wan_ipv4_pridns | router primary dns server | str |
| wan_ipv4_pridns_address | router primary dns server | ipaddress |
| wan_ipv4_snddns | router secondary dns server | str |
| wan_ipv4_snddns_address | router secondary dns server | ipaddress |
| lan_macaddr | router mac address | str |
| lan_macaddress | router mac address | macaddress |
| lan_ipv4_ipaddr | router LAN IP address | str |
| lan_ipv4_ipaddress | router LAN IP address | ipaddress |
| lan_ipv4_dhcp_enable | router LAN DHCP enabled | bool |
| lan_ipv4_netmask | router LAN gateway IP netmask | str |
| lan_ipv4_netmask_address | router LAN gateway IP netmask | ipaddress |
| lan_ipv4_pridns | ip adress given out by dhcp server | str |

### Contributing
We welcome contributions to the Genexis Router API project! Please follow these guidelines to contribute:

1. Fork the repository.
2. Create a new branch with a descriptive name for your feature or bugfix.
3. Make your changes and ensure that the code passes all tests.
4. Submit a pull request with a clear description of your changes.

### License
This project is licensed under an open-source license. See the LICENSE file for more information.