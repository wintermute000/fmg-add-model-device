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

    else:
        print(f"Workspace lock failed. Status code: {response.status_code}")
        return None
    
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

def policy_install(session_token, adom):

    add_policyinstall_scope_list = []

    # Generate list of dictionaries of devices
    for device in device_list:
        policy_install_block = {
            "name": f"{device['name']}",
            "vdom": "root"
            }
        add_policyinstall_scope_list.append(policy_install_block)

    policy_install_data = {
        "session": f"{session_token}",
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "/securityconsole/install/package",
                "data": {
                        
                        "adom": f"{adom}",
                        "pkg": f"{policy_package}",
                        "scope": add_policyinstall_scope_list ,
                        "flags": "none"
                    }
            }
        ]
    }

    response = requests.post(fortimanager_url, json=policy_install_data, headers=headers, verify=False)
    response_json = response.json()

    if response.status_code == 200:
        # Extract session token from the response
        print('Policy install response code =', response.status_code)
        print('Policy install message =', response_json["result"][0]["status"]["message"])
    else:
        print(f"Policy install failed. Status code: {response.status_code}")
        print('Policy install message =', response_json["result"][0]["status"]["message"])

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
        workspace_lock(session_token, adom)
        time.sleep(1)
        add_device_from_blueprint(session_token, adom)
        time.sleep(1)
        add_metavars(session_token, adom)
        time.sleep(1)
        workspace_commit(session_token, adom)
        time.sleep(1)
        device_install(session_token, adom)
        time.sleep(1)
        workspace_commit(session_token, adom)
        time.sleep(1)
        policy_install(session_token, adom)
        time.sleep(1)
        workspace_commit(session_token, adom)
        time.sleep(1)
        workspace_unlock(session_token, adom)
        time.sleep(1)
        logout_from_fortimanager(session_token)

    else:
        print("Login failed. Unable to obtain session token.")
