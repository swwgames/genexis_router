import json
import requests
import macaddress
import ipaddress
from logging import Logger
from typing import List
from .data_classes import Firmware, Status, IPv4Status, IPv4Reservation, IPv4DHCPLease, Device

class GenexisRouter:
    def __init__(self, host: str, username: str = 'admin', password: str = 'admin', logger: Logger = None, verify_ssl: bool = False, timeout: int = 10) -> None:
        self.host = host
        if not (self.host.startswith('http://') or self.host.startswith('https://')):
            self.host = f"http://{self.host}"
        self.username = username
        self.password = password
        self.timeout = timeout
        self.logger = logger
        self.session_id = None
        self._verify_ssl = verify_ssl
        if not self._verify_ssl:
            requests.packages.urllib3.disable_warnings()
        self.headers = {"content-type": "application/json"}

    def authorize(self) -> bool:
        try:
            response = self._try_login()
            json_data = response.json()

            if json_data["result"]["result"] == -1:
                raise Exception('Username or password is incorrect')

            if json_data["result"]["result"] == 0:
                self.session_id = json_data["result"]["sessionid"]
                return True
            else:
                raise Exception('No data in response: ' + str(json_data["result"]))

        except (ValueError, KeyError, AttributeError) as e:
            if self.logger:
                self.logger.error("Genexis Integration Exception - Couldn't fetch auth tokens! Response was: %s, Exception: %s",
                                  response.text, str(e))
            return False

    def logout(self) -> None:
        if self.session_id:
            try:
                self.request("session.destroy")
            except Exception as e:
                if self.logger:
                    self.logger.error('Genexis Integration Exception during logout - %s', str(e))
        self.session_id = None

    def _try_login(self) -> requests.Response:
        url = self.host
        payload = {
            "jsonrpc": "2.0",
            "id": 90,
            "method": "session.login",
            "params": {"username": self.username, "password": self.password},
        }
        return requests.post(
            url,
            data=json.dumps(payload),
            timeout=self.timeout,
            verify=self._verify_ssl,
            headers=self.headers
        )

    def _str2bool(self, v) -> bool:
        return str(v).lower() in ("yes", "true", "on")
    
    def request(self, method: str, params: dict = None) -> dict:
        if params is None:
            params = {}
        if not self.session_id:
            raise Exception("Not authorized")
        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": {"sessionid": self.session_id, **params}}

        response = requests.post(
            self.host,
            data=json.dumps(payload),
            headers=self.headers,
            timeout=self.timeout,
            verify=self._verify_ssl
        )
        
        data = response.text
        try:
            json_response = response.json()
            if 'result' not in json_response:
                raise Exception("Router didn't respond with JSON - " + data)
            return json_response
        except ValueError:
            if self.logger:
                self.logger.error(
                    "Genexis Integration Exception - Router didn't respond with JSON. Check if credentials are correct")
            raise Exception('An unknown response - ' + data)

    def query(self, query: str) -> dict:
        return self.request(query)

    def get_status(self) -> Status:
        params = {"sessionid": self.session_id}
        response = self.request("interfaces.get", params)
        result = response.get('result', {})
        response2 = self.request('parental_control.get', params)
        wireless = self.request('wireless.get', params)
        wireless_guest = self.request('wireless.guest.get', params)
        dhcp_data = self.request('clients.get', params)

        clients = dhcp_data['result']['clients']
        mac_ip_dict = {client['macaddr']: client['ipaddr'] for client in clients}

        guest_2g_enable = None
        guest_5g_enable = None
        _2g_enable = None
        _5g_enable = None
        for interface in wireless_guest['result']['wireless_guest']['interfaces']:
            if interface['band'] == '2.4GHz':
                guest_2g_enable = interface['enable']
            elif interface['band'] == '5GHz':
                guest_5g_enable = interface['enable']

        for interface in wireless['result']['wireless']['interfaces']:
            if interface['name'] == 'wlan1':
                _2g_enable = interface['enable']
            elif interface['name'] == 'wlan2':
                _5g_enable = interface['enable']

        status = Status(
            wan_macaddr=macaddress.EUI48(result['internet']['macaddr']) if 'internet' in result else None,
            lan_macaddr=macaddress.EUI48(result['lan']['macaddr']),
            wan_ipv4_addr=ipaddress.IPv4Address(result['internet']['ipaddr']) if 'internet' in result else None,
            lan_ipv4_addr=ipaddress.IPv4Address(result['lan']['ipaddr']) if 'lan' in result else None,
            wan_ipv4_gateway=ipaddress.IPv4Address(result['internet']['gateway']) if 'internet' in result else None,
            wired_total=0,  # Not available yet
            wifi_clients_total=0,  # Not available yet
            guest_clients_total=0,  # Assuming no guest client data available
            clients_total=len(response2.get('result', {}).get('discoveries', [])),
            guest_2g_enable=guest_2g_enable,  # Assuming no data available
            guest_5g_enable=guest_5g_enable,  # Assuming no data available
            wifi_2g_enable=_2g_enable,  # Assuming no data available
            wifi_5g_enable=_5g_enable,  # Assuming no data available
            devices=[]  # Assuming no device data available
        )

        if 'discoveries' in response2['result']:
            for discovery in response2['result']['discoveries']:
                ip_address = mac_ip_dict.get(discovery['mac'], "0.0.0.0")
                status.devices.append(Device(
                    macaddr=macaddress.EUI48(discovery['mac']),
                    ipaddr=ipaddress.IPv4Address(ip_address),
                    hostname=discovery['name']
                ))

        return status

    def get_ipv4_status(self) -> IPv4Status:
        ipv4_status = IPv4Status()
        data = self.request('interfaces.get')
        data2 = self.request('dhcp.get')
        ipv4_status._wan_macaddr = macaddress.EUI48(data['result']['internet']['macaddr'])
        ipv4_status._wan_ipv4_ipaddr = ipaddress.IPv4Address(data['result']['internet']['ipaddr'])
        ipv4_status._wan_ipv4_gateway = ipaddress.IPv4Address(data['result']['internet']['gateway'])
        ipv4_status._wan_ipv4_netmask = ipaddress.IPv4Address(data['result']['internet']['netmask'])
        ipv4_status._wan_ipv4_pridns = ipaddress.IPv4Address(data['result']['internet']['dns']['static_dns'][0])
        ipv4_status._wan_ipv4_snddns = ipaddress.IPv4Address(data['result']['internet']['dns']['static_dns'][1])
        ipv4_status._lan_macaddr = macaddress.EUI48(data['result']['lan']['macaddr'])
        ipv4_status._lan_ipv4_ipaddr = ipaddress.IPv4Address(data['result']['lan']['ipaddr'])
        ipv4_status.lan_ipv4_dhcp_enable = self._str2bool(data2['result']['pool'][0]['enabled'])
        ipv4_status._lan_ipv4_netmask = ipaddress.IPv4Address(data['result']['lan']['netmask'])
        ipv4_status._lan_ipv4_pridns = ipaddress.IPv4Address(data2['result']['pool'][0]['opt_dnsaddr'][0])
        return ipv4_status

    def get_ipv4_reservations(self) -> List[IPv4Reservation]:
        ipv4_reservations = []
        data = self.request('dhcp.static.get')

        for item in data['result']['lan']['staticaddress']:
            ipv4_reservations.append(
                IPv4Reservation(macaddress.EUI48(item['macaddr']), ipaddress.IPv4Address(item['ipaddr']),
                                self._str2bool(item['enable'])))

        return ipv4_reservations
    
    def get_ipv4_dhcp_leases(self) -> List[IPv4DHCPLease]:
        dhcp_leases = []
        data = self.request('clients.get')

        for item in data['result']['clients']:
            dhcp_leases.append(
                IPv4DHCPLease(macaddress.EUI48(item['macaddr']), ipaddress.IPv4Address(item['ipaddr']), item['hostname'],
                              item['expiry']))

        return dhcp_leases

    def reboot(self) -> None:
        if not self.session_id:
            raise Exception("Not authorized")
        payload = {
            "jsonrpc": "2.0",
            "id": 40,
            "method": "reload.set",
            "params": {
                "reboot": 0,
                "factory_default": False,
                "username": self.username,
                "password": self.password,
                "sessionid": self.session_id
            }
        }

        response = requests.post(
            self.host,
            data=json.dumps(payload),
            headers=self.headers,
            timeout=self.timeout,
            verify=self._verify_ssl
        )

        try:
            json_response = response.json()
            if 'result' not in json_response:
                raise Exception("Router didn't respond with JSON - " + response.text)
            
            if json_response['result']['result'] == 0:
                print(json_response['result']['message'])
            else:
                raise Exception("Failed to reboot the router: " + json_response['result']['message'])

        except ValueError:
            if self.logger:
                self.logger.error(
                    "Genexis Integration Exception - Router didn't respond with JSON. Check if credentials are correct")
            raise Exception('An unknown response - ' + response.text)

    def get_firmware(self) -> Firmware:
        params = {"sessionid": self.session_id}
        response = self.request("genui.info", params)
        result = response.get('result', {})
        sysinfo = result.get('sysinfo', {})
        return Firmware(
            hardware_version=result['deviceinfo']['hardware_revision'],
            model=result['deviceinfo']['product_name'],
            firmware_version=sysinfo['firmware_revision']
        )
