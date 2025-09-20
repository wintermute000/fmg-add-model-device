import requests
import json
import urllib3
import os
import pprint
import time

username = os.environ['FMGUSERNAME']
password = os.environ['FMGPASSWORD']
headers = {'Content-Type': 'application/json'}



def login_to_fortimanager():
    login_data = {
        "id": 1,
        "method": "exec",
        "params": [
            {
                "data": {
                    "passwd": password,
                    "user": username
                },
                "url": "/sys/login/user"
            }
        ]
    }

    response = requests.post(fortimanager_url, json=login_data, headers=headers, verify=False)

    if response.status_code == 200:
        # Extract session token from the response
        session_token = response.json().get('session')
        return session_token
    else:
        print(f"Login failed. Status code: {response.status_code}")
        print('Login message =', response_json["result"][0]["status"]["message"])
        return None

def logout_from_fortimanager(session_token):
    logout_data = {
        "session": f"{session_token}",
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "/sys/logout"
            }
        ]
    }

    response = requests.post(fortimanager_url, json=logout_data, headers=headers, verify=False)
    response_json = response.json()

    if response.status_code == 200:
        # Extract session token from the response
        print('Logout response code =', response.status_code)
        print('Logout message =', response_json["result"][0]["status"]["message"])
    else:
        print(f"Logout failed. Status code: {response.status_code}")
        print('Logout message =', response_json["result"][0]["status"]["message"])

def workspace_lock(session_token, adom):
    workspace_lock_payload = {
        "session": f"{session_token}",
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": f"/dvmdb/adom/{adom}/workspace/lock"
                }
        ]
    }

    response = requests.post(fortimanager_url, json=workspace_lock_payload, headers=headers, verify=False)
    response_json = response.json()

    if response.status_code == 200:
        print('Locking workspace response code =', response.status_code)
        print('Locking workspace response message =', response_json["result"][0]["status"]["message"])
        # If ADOM already locked, quit
        if response_json["result"][0]["status"]["message"] == "Workspace is locked by other user":
            print('*******************************************************')
            print('ADOM locked by other user, cannot continue, terminating')
            print('*******************************************************')
            logout_from_fortimanager(session_token)
            quit()

    else:
        print(f"Workspace lock failed. Status code: {response.status_code}")
        # Log out and quit
    
def workspace_unlock(session_token, adom):
    workspace_unlock_payload = {
        "session": f"{session_token}",
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": f"/dvmdb/adom/{adom}/workspace/unlock"
                }
        ]
    }

    response = requests.post(fortimanager_url, json=workspace_unlock_payload, headers=headers, verify=False)
    response_json = response.json()

    if response.status_code == 200:
        print('Unlocking workspace status code =', response.status_code)
        print('Unlocking workspace message =', response_json["result"][0]["status"]["message"])

    else:
        print(f"Workspace Unlock failed. Status code: {response.status_code}")
        print('Unlocking workspace message =', response_json["result"][0]["status"]["message"])
        return None

def workspace_commit(session_token, adom):
    workspace_commit_payload = {
        "session": f"{session_token}",
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": f"/dvmdb/adom/{adom}/workspace/commit"
                }
        ]
    }

    response = requests.post(fortimanager_url, json=workspace_commit_payload, headers=headers, verify=False)
    response_json = response.json()

    if response.status_code == 200:
        print('Commit workspace response code =', response.status_code)
        print('Commit workspace response message =', response_json["result"][0]["status"]["message"])

    else:
        print(f"Workspace commit failed. Status code: {response.status_code}")
        return None

def device_install(session_token, adom):

    add_deviceinstall_scope_list = []

    # Generate list of dictionaries of devices
    for device in device_list:
        install_block = {
            "name": f"{device['name']}",
            "vdom": "root"
            }
        add_deviceinstall_scope_list.append(install_block)

    device_install_data = {
        "session": f"{session_token}",
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "/securityconsole/install/device",
                "data": [
                    {
                        "adom": f"{adom}",
                        "scope": add_deviceinstall_scope_list ,
                        "flags": "none"
                    }
                ]
            }
        ]
    }

    response = requests.post(fortimanager_url, json=device_install_data, headers=headers, verify=False)
    response_json = response.json()

    if response.status_code == 200:
        # Extract session token from the response
        print('Device install response code =', response.status_code)
        print('Device install message =', response_json["result"][0]["status"]["message"])
    else:
        print(f"Device install failed. Status code: {response.status_code}")
        print('Device install message =', response_json["result"][0]["status"]["message"])

def policy_install(session_token, adom, pkg_list):

    # Iterate through the list of dicts like [{'branch': [...]}, {'branchtest': [...]}]
    for group in pkg_list:
        for pkg, devices in group.items():
            # Build scope list for this package
            scope_list = []
            for device in devices:
                scope_list.append({
                    "name": device,
                    "vdom": "root"
                })

            # Build request payload for this package
            policy_install_payload = {
                "session": session_token,
                "id": 1,
                "method": "exec",
                "params": [
                    {
                        "url": "/securityconsole/install/package",
                        "data": {
                            "adom": f"{adom}",
                            "pkg": f"{pkg}",                 # 👈 pkg now comes from dict key
                            "scope": scope_list,        # 👈 device names mapped here
                            "flags": "none"
                        }
                    }
                ]
            }
          
            response = requests.post(fortimanager_url, json=policy_install_payload, headers=headers, verify=False)
            response_json = response.json()

            if response.status_code == 200:
                # Extract session token from the response
                print(f'Policy install for policy package {pkg} response code =', response.status_code)
                print(f'Policy install for policy package {pkg} message =', response_json["result"][0]["status"]["message"])
            else:
                print(f"Policy install for policy package {pkg} failed. Status code: {response.status_code}")
                print(f'Policy install for policy package {pkg} message =', response_json["result"][0]["status"]["message"])

def add_device_from_blueprint(session_token, adom):

    add_dev_list = []

    # Generate list of dictionaries of devices
    for device in device_list:
        add_dev_dict = {
                "adm_usr": "admin",
                "desc": f"{device['description']}",
                "device action": "add_model",
                "device blueprint": f"{device['blueprint']}",
                "latitude": f"{device['latitude']}",
                "longitude": f"{device['longitude']}",
                "mgmt_mode": "fmg",
                "mgt_vdom": "root",
                "name": f"{device['name']}",
                "os_type": 0,
                "os_ver": f"{device['os_ver']}",
                "mr": int(f"{device['mr']}"),
                "platform_str": f"{device['platform_str']}",
                "sn": f"{device['serial']}",
                }
        add_dev_list.append(add_dev_dict) 

    # Generate REST payload    
    add_device_payload = {
        "id": 1,
        "session": f"{session_token}",
        "method": "exec",
        "params": [
            {
                "url": "/dvm/cmd/add/dev-list",
                "data": {
                    "adom": f"{adom}",
                    "add-dev-list": add_dev_list,
                    "flags": "create_task"
                }
            }
        ]
    }
    print("Adding Model Device(s)")
    print("---")
    print(json.dumps(add_device_payload, indent = 6)) 
    print("---")

    response = requests.post(fortimanager_url, json=add_device_payload, headers=headers, verify=False)
    response_json = response.json()

    if response.status_code == 200:
        print('Add device(s) status code =', response.status_code)
        print('Add device(s) message =', response_json["result"][0]["status"]["message"])

    else:
        print(f"Add device(s) failed. Status code: {response.status_code}")
        print('Add device(s) message =', response_json["result"][0]["status"]["message"])
        return None

def add_metavars(session_token, adom):

    add_metavar_list = []

    # Generate dictionaries
    for device, vars in metavar_dict.items():
        for var_name, var_value in vars.items():    
            data_dict = {
                        "data": [
                            {
                            "_scope": [
                                {
                                "name": f"{device}",
                                "vdom": "global"
                                }
                            ],
                            "value": f"{var_value}"
                            }
                        ],
                        "url": f"/pm/config/adom/{adom}/obj/fmg/variable/{var_name}/dynamic_mapping"
                    }
                    
            add_metavar_list.append(data_dict) 
    

    # Generate REST payload    
    add_metavars_payload = {
        "id": 1,
        "session": f"{session_token}",
        "method": "add",
        "params": add_metavar_list
    }
    print("Adding Metadata Variables")
    print("---")
    print(json.dumps(add_metavars_payload, indent = 4)) 
    print("---")

    response = requests.post(fortimanager_url, json=add_metavars_payload, headers=headers, verify=False)
    response_json = response.json()

    if response.status_code == 200:
        print('Add metadata variables status code =', response.status_code)
        print('Add metadata variables =', response_json["result"][0]["status"]["message"])

    else:
        print(f"Add dmetadata variables failed. Status code: {response.status_code}")
        print('Add metadata variables message =', response_json["result"][0]["status"]["message"])
        return None

def get_existing_devices(session_token, adom):
    # Get existing devices
    get_existing_devices_payload = {
        "id": 1,
        "method": "get",
        "params": [
            {
            "fields": [
                "name",
                "sn"
            ],
            "option": [
                "no loadsub"
            ],
            "url": f"/dvmdb/adom/{adom}/device"
            }
        ],
        "session": f"{session_token}",
        "verbose": 1
    }

    response = requests.post(fortimanager_url, json=get_existing_devices_payload, headers=headers, verify=False)
    response_json = response.json()

    if response.status_code == 200:
        print('Get existing devices status code =', response.status_code)
        print('Get existing devices message =', response_json["result"][0]["status"]["message"])
        existing_devices = response_json["result"][0]["data"]
        return existing_devices

    else:
        print(f"Get existing devices failed. Status code: {response.status_code}")
        print('Get existing devices message =', response_json["result"][0]["status"]["message"])
        return None

def check_existing_devices(existing_devices, device_list):
    existing_names = set()   # start with an empty set
    for d in existing_devices:   # loop through each device 
        existing_names.add(d["name"])  # add the "name" value to the set

    # Build a new filtered list
    filtered_devices = []
    for device in device_list:
        if device["name"] not in existing_names:
            filtered_devices.append(device)

    return filtered_devices

def check_existing_metavars(existing_devices, metavars_dict):
    existing_names = set()   # start with an empty set
    for d in existing_devices:   # loop through each device 
        existing_names.add(d["name"])  # add the "name" value to the set

    # Delete matching keys from metavars_dict
    for name in list(metavars_dict.keys()):
        if name in existing_names:
            del metavars_dict[name]

    return metavars_dict

def get_blueprints(session_token, adom, device_list):
    blueprint_dict = {}
    blueprint_tmplist = []

    # Iterate through device list and produce a dictionary of blueprint: [list of devices using]
    for device in device_list:
        blueprint = device["blueprint"]
        if blueprint not in blueprint_dict:
            blueprint_dict[blueprint] = []
            blueprint_tmplist.append(blueprint)
        blueprint_dict[blueprint].append(device["name"])
    
    # Set of blueprint names
    blueprint_set = set(blueprint_tmplist)

    # Convert grouped dict into a list of dictionaries
    blueprint_list = []
    for bp, names in blueprint_dict.items():
        blueprint_list.append({bp: names})
    
    # Get the policy package referenced by each blueprint
    get_blueprint_pkg_payload = {
        "id": 1,
        "method": "get",
        "params": [
            {
            "url": f"/pm/config/adom/{adom}/obj/fmg/device/blueprint"
            }
        ],
        "session": f"{session_token}",
    }

    response = requests.post(fortimanager_url, json=get_blueprint_pkg_payload, headers=headers, verify=False)
    response_json = response.json()
    
    blueprint_pkgs = {}
    for item in response_json["result"][0]["data"]:
        blueprint_name = item["name"]
        pkg_value = item["pkg"]
        blueprint_pkgs[blueprint_name] = pkg_value

    # For blueprint_list
    # {'Blueprint-60F': 'branch', 'BlueprintTest': 'branchtest'}
    # And blueprint_pkgs
    # [{'Blueprint-60F': ['sdbranch3', 'sdbranch4']}, {'BlueprintTest': ['sdbranch5']}]
    # Substitute policy package name for blueprint

    substituted = []
    for entry in blueprint_list:
        new_entry = {}
        for bp, dev_list in entry.items():
            if bp in blueprint_pkgs:
                new_entry[blueprint_pkgs[bp]] = dev_list
            else:
                new_entry[bp] = dev_list  # fallback if no match
        substituted.append(new_entry)

    return substituted

if __name__ == "__main__":
    with open("fmginfo.json", "r") as f:
        config = json.load(f)
        adom = config["adom"]
        fortimanager_url = config["fortimanager_url"]
        policy_package = config["policy_package"]

    with open("devices.json", "r") as d:
        device_list = json.load(d)

    with open("metavars.json", "r") as v:
        metavar_dict = json.load(v)

    # Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Get Session Token
    session_token = login_to_fortimanager()

    # Lock ADOM, add devices, add metadata variables, commit ADOM, unlock ADOM and logout
    if session_token:

        # Filter out existing devices and remove from data structures to skip
        existing_devices = get_existing_devices(session_token, adom)
        time.sleep(1)

        print("Existing devices are:")
        print("---")
        pprint.pprint(existing_devices)
        print("---")

        device_list = check_existing_devices(existing_devices, device_list)
        print("Filtered device list with existing devices removed:")
        print("---")
        pprint.pprint(device_list)
        print("---")

        metavar_dict = check_existing_metavars(existing_devices, metavar_dict)
        print("Filtered metadata variables with existing devices removed:")
        print("---")
        pprint.pprint(metavar_dict)
        print("---")

        # Get list of devices and the policy packages they use as referenced in blueprints
        pkg_list = get_blueprints(session_token, adom, device_list)
        print("List of policy packages and assigne devices as derived from blueprints:")
        print("---")
        pprint.pprint(pkg_list)
        print("---")

        # Lock workspace
        workspace_lock(session_token, adom)
        time.sleep(1)

        # Add devices that do not already exist
        add_device_from_blueprint(session_token, adom)
        time.sleep(1)

        # Add metadata variables and commit
        add_metavars(session_token, adom)
        time.sleep(1)
        workspace_commit(session_token, adom)
        time.sleep(1)

        # Device install and commit
        device_install(session_token, adom)
        time.sleep(1)
        workspace_commit(session_token, adom)
        time.sleep(1)

        # Install  policy package and commit
        policy_install(session_token, adom, pkg_list)
        time.sleep(1)
        workspace_commit(session_token, adom)
        time.sleep(1)

        # Unlock workspace
        workspace_unlock(session_token, adom)
        time.sleep(1)

        # Logout
        logout_from_fortimanager(session_token)

    else:
        print("Login failed. Unable to obtain session token.")
