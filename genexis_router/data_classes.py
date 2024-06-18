import macaddress
import ipaddress
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Firmware:
    hardware_version: str
    model: str
    firmware_version: str

@dataclass
class Interface:
    macaddr: Optional[str] = None
    ipaddr: Optional[str] = None
    netmask: Optional[str] = None
    rx_packets: Optional[int] = None
    rx_octets: Optional[int] = None
    tx_packets: Optional[int] = None
    tx_octets: Optional[int] = None
    speed: Optional[int] = None
    status: Optional[str] = None
    duplex: Optional[str] = None
    domain_name: Optional[str] = None
    ip6addr: Optional[List[str]] = field(default_factory=list)

@dataclass
class Device:
    macaddr: macaddress.EUI48
    ipaddr: ipaddress.IPv4Address
    hostname: str

    @property
    def mac_address(self) -> str:
        return str(self.macaddr)

    @property
    def ip_address(self) -> str:
        return str(self.ipaddr)

@dataclass
class Status:
    wan_macaddr: Optional[macaddress.EUI48] = None
    lan_macaddr: macaddress.EUI48 = None
    wan_ipv4_addr: Optional[ipaddress.IPv4Address] = None
    lan_ipv4_addr: Optional[ipaddress.IPv4Address] = None
    wan_ipv4_gateway: Optional[ipaddress.IPv4Address] = None
    wired_total: int = 0
    wifi_clients_total: int = 0
    guest_clients_total: int = 0
    clients_total: int = 0
    guest_2g_enable: bool = False
    guest_5g_enable: bool = False
    wifi_2g_enable: bool = False
    wifi_5g_enable: bool = False
    devices: List[Device] = field(default_factory=list)

    @property
    def wan_mac_address(self) -> Optional[str]:
        return str(self.wan_macaddr) if self.wan_macaddr else None

    @property
    def lan_mac_address(self) -> str:
        return str(self.lan_macaddr)

    @property
    def wan_ipv4_address(self) -> Optional[str]:
        return str(self.wan_ipv4_addr) if self.wan_ipv4_addr else None

    @property
    def lan_ipv4_address(self) -> Optional[str]:
        return str(self.lan_ipv4_addr) if self.lan_ipv4_addr else None

    @property
    def wan_ipv4_gateway_address(self) -> Optional[str]:
        return str(self.wan_ipv4_gateway) if self.wan_ipv4_gateway else None

@dataclass
class IPv4Reservation:
    _macaddr: macaddress.EUI48
    _ipaddr: ipaddress.IPv4Address
    enabled: bool

    @property
    def macaddr(self) -> str:
        return str(self._macaddr)

    @property
    def macaddress(self) -> macaddress.EUI48:
        return self._macaddr

    @property
    def ipaddr(self) -> str:
        return str(self._ipaddr)

    @property
    def ipaddress(self) -> ipaddress.IPv4Address:
        return self._ipaddr
    
@dataclass
class IPv4DHCPLease:
    _macaddr: macaddress.EUI48
    _ipaddr: ipaddress.IPv4Address
    hostname: str
    lease_time: str

    @property
    def macaddr(self) -> str:
        return str(self._macaddr)

    @property
    def macaddress(self) -> macaddress.EUI48:
        return self._macaddr

    @property
    def ipaddr(self) -> str:
        return str(self._ipaddr)

    @property
    def ipaddress(self) -> ipaddress.IPv4Address:
        return self._ipaddr
    
@dataclass
class IPv4Status:
    _wan_macaddr: macaddress.EUI48
    _wan_ipv4_ipaddr: ipaddress.IPv4Address
    _wan_ipv4_gateway: ipaddress.IPv4Address
    _wan_ipv4_netmask: ipaddress.IPv4Address
    _wan_ipv4_pridns: ipaddress.IPv4Address
    _wan_ipv4_snddns: ipaddress.IPv4Address
    _lan_macaddr: macaddress.EUI48
    _lan_ipv4_ipaddr: ipaddress.IPv4Address
    lan_ipv4_dhcp_enable: bool
    _lan_ipv4_netmask: ipaddress.IPv4Address
    _lan_ipv4_pridns: Optional[ipaddress.IPv4Address] = None

    @property
    def wan_macaddr(self) -> str:
        return str(self._wan_macaddr)

    @property
    def wan_macaddress(self) -> macaddress.EUI48:
        return self._wan_macaddr

    @property
    def wan_ipv4_ipaddr(self) -> str:
        return str(self._wan_ipv4_ipaddr)

    @property
    def wan_ipv4_ipaddress(self) -> ipaddress.IPv4Address:
        return self._wan_ipv4_ipaddr

    @property
    def wan_ipv4_gateway(self) -> str:
        return str(self._wan_ipv4_gateway)

    @property
    def wan_ipv4_gateway_address(self) -> ipaddress.IPv4Address:
        return self._wan_ipv4_gateway

    @property
    def wan_ipv4_netmask(self) -> str:
        return str(self._wan_ipv4_netmask)

    @property
    def wan_ipv4_netmask_address(self) -> ipaddress.IPv4Address:
        return self._wan_ipv4_netmask

    @property
    def wan_ipv4_pridns(self) -> str:
        return str(self._wan_ipv4_pridns)

    @property
    def wan_ipv4_pridns_address(self) -> ipaddress.IPv4Address:
        return self._wan_ipv4_pridns

    @property
    def wan_ipv4_snddns(self) -> str:
        return str(self._wan_ipv4_snddns)

    @property
    def wan_ipv4_snddns_address(self) -> ipaddress.IPv4Address:
        return self._wan_ipv4_snddns

    @property
    def lan_macaddr(self) -> str:
        return str(self._lan_macaddr)

    @property
    def lan_macaddress(self) -> macaddress.EUI48:
        return self._lan_macaddr

    @property
    def lan_ipv4_ipaddr(self) -> str:
        return str(self._lan_ipv4_ipaddr)

    @property
    def lan_ipv4_ipaddress(self) -> ipaddress.IPv4Address:
        return self._lan_ipv4_ipaddr

    @property
    def lan_ipv4_netmask(self) -> str:
        return str(self._lan_ipv4_netmask)

    @property
    def lan_ipv4_netmask_address(self) -> ipaddress.IPv4Address:
        return self._lan_ipv4_netmask

    @property
    def lan_ipv4_pridns(self) -> str:
        return str(self._lan_ipv4_pridns)
