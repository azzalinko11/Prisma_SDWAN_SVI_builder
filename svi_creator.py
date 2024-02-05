#azzalinko11 version 0.1

#import libs
import credentials_file
import requests
import prisma_sase
import csv
import json
# Import the Prisma SASE SDK API constructor etc
from prisma_sase import API, jd

# Instantiate the Prisma SASEx API constructor
sdk = API()

# Call Prisma SASE API login and credentaisl from "credentials_file.py" file using the Interactive helpers (Handle SAML2.0 login and MSP functions too!).
sdk.interactive.login_secret(client_id=credentials_file.client_id, 
                             client_secret=credentials_file.client_secret, 
                             tsg_id=credentials_file.scope)

# Path to the CSV file containing the SVI/Interfae list
csv_file = 'svi_import.csv'

# Read the SVI list from the CSV file

svi_objects = []
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        svi_object = {
            "name": row['INT_Name'],
            "description": row['Description'],
            "type": "vlan",
            "attached_lan_networks": None,
            "site_wan_interface_ids": None,
            "mac_address": None,
            "mtu": 1500,
            "ipv4_config": {
                "type": "static",
                "static_config": {
                    "address": row['IP_Addr'],
                },
                "dhcp_config": None,
                "dns_v4_config": {
                    "name_servers": [
                        "8.8.8.8"
                    ]
                },
                "routes": None
            },
            "dhcp_relay": None,
            "ethernet_port": {
                "full_duplex": False,
                "speed": 0
            },
            "admin_up": True,
            "nat_address": None,
            "nat_port": 0,
            "used_for": "lan",
            "bound_interfaces": None,
            "sub_interface": None,
            "pppoe_config": None,
            "parent": None,
            "network_context_id": "1705878522813001696",
            "bypass_pair": None,
            "service_link_config": None,
            "scope": "local",
            "tags": None,
            "nat_zone_id": None,
            "devicemgmt_policysetstack_id": None,
            "nat_pools": None,
            "directed_broadcast": False,
            "ipfixcollectorcontext_id": None,
            "ipfixfiltercontext_id": None,
            "secondary_ip_configs": None,
            "static_arp_configs": None,
            "cellular_config": None,
            "multicast_config": {
                "multicast_enabled": False,
                "igmp_version": "IGMPV3",
                "dr_priority": 1,
                "igmp_static_joins": None
            },
            "ipv6_config": None,
            "nat_address_v6": None,
            "nat_port_v6": 0,
            "poe_enabled": False,
            "power_usage_threshold": 0,
            "lldp_enabled": False,
            "switch_port_config": None,
            "vlan_config": {
                "voice_enabled": False,
                "vlan_id": row['VLAN_ID'],
                "mstp_instance": 0
            },
            "interface_profile_id": None,
            "authentication_config": None,
            "peer_bypasspair_wan_port_type": "none",
            "vrf_context_id": "1705517929068015496"
        }
        svi_objects.append(svi_object)

#convert to json and strip brackets
svi_data_cov_json = json.dumps(svi_objects, indent = 4)[1:-1]
print(svi_data_cov_json)


# Send the POST request to add the address objects, will update to error handling in an updated release
success_count = 0
failure_count = 0

for obj in svi_objects:
    svi_data_json = json.dumps(obj, indent=4)
    
    response = sdk.post.interfaces(
        site_id='1705604220721000796',
        element_id='1705534739582007296',
        data=svi_data_json,
        api_version="v4.17"
    )

