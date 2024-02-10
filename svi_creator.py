#azzalinko11 version 1.0

#import libs
import credentials_file
import requests
import csv
import json
# Import the Prisma SASE SDK API constructor etc
from prisma_sase import API, jd

# Instantiate the Prisma SASEx API constructor
sdk = API()

# Call Prisma SASE API login and creds from "credentials_file.py" file using the Interactive helpers (Handle SAML2.0 login and MSP functions too!).
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
                        row['DNS1'],
                        row['DNS2']
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
            "network_context_id": row['CONTEXT_ID'],
            "bypass_pair": None,
            "service_link_config": None,
            "scope": row['Scope'],
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
            "vrf_context_id": row['VRF_ID'],
        }
        svi_objects.append(svi_object)
        # Store element_id and site_id separately
        element_id = row['ELEMENT_ID']
        site_id = row['SITE_ID']


#convert to json and strip brackets
svi_data_cov_json = json.dumps(svi_objects, indent = 4)[1:-1]
print(svi_data_cov_json)


# Send the POST request to add the address objects with error handling
success_count = 0
failure_count = 0

# Read the SVI list from the CSV file
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    
    for obj in svi_objects:
        try:
            # Extract element_id and site_id directly from the CSV row
            row = next(reader)
            element_id = row['ELEMENT_ID']
            site_id = row['SITE_ID']

            svi_data_json = json.dumps(obj, indent=4)

            response = sdk.post.interfaces(
                site_id=site_id,
                element_id=element_id,
                data=svi_data_json,
                api_version="v4.17"
            )

            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx status codes)

            if response.status_code == 200:
                success_count += 1
                print(f'Successfully added SVI interface: {obj["name"]}')
            else:
                failure_count += 1
                print(f'Failed to add SVI interface: {obj["name"]}, Status Code: {response.status_code}, Response: {response.text}')

        except StopIteration:
            # StopIteration indicates the end of the CSV file
            break

        except requests.exceptions.RequestException as e:
            failure_count += 1
            print(f'Exception occurred while adding SVI interface: {obj["name"]}, Error: {e}')

print(f'Successfully added {success_count} SVI interfaces. Failed to add {failure_count} interfaces.')
