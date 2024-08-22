from os import getenv
from rich import print as rprint
from napalm import get_network_driver
from typing import Callable
import yaml


USERNAME = getenv("DEVICE_LOGIN")
PASSWORD = getenv("DEVICE_PASSWORD")

with open('inventory.yaml', 'r') as f:
    ip_mgmt = yaml.safe_load(f)


def device_collector(
    ip: str,
    login=USERNAME,
    password=PASSWORD ) -> tuple:
    # Connect to Cisco device:
    ios_driver = get_network_driver(name="ios")
    ios_device = ios_driver(hostname=ip, username=login, password=password)
    ios_device.open()
    facts = ios_device.get_facts()
    config = ios_device.get_config()['running']
    return (facts, config)


data_collector = [ device_collector(ip=ip_addr) for ip_addr in ip_mgmt ]

rprint(data_collector)
