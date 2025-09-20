# Script to add model devices to FortiManager
---

Tested on 7.6.4 and FG-60F on 7.6.4

## Features and Requirements:
- Blueprint(s) (https://docs.fortinet.com/document/fortimanager/7.6.4/administration-guide/55038/using-device-blueprints-for-model-devices)
- Policy packag(es) and all templates assigned via blueprint(s) - supports multiple blueprints
- FortiManager administrative user with JSON RPC read/write access
- FortiManager username as environmental variable (EXPORT FMGUSERNAME=xyz)
- FortiManager password as environmental variable (EXPORT FMGPASSWORD=xyz)
- Compatible with workspace mode with error handling if already locked (comment out lock/unlock/commit if not required)
- Devices that already exist will be skipped - matches on device name only
- Common functions (login, logout, lock, unlock, commit, device install, policy package install) are imported from fmgcommon.py

## Usage
- python3 fmg-add-model-device.py
- needs input files in format as per examples provided
    - FortiManager attributes (ADOM, URL) in fmginfo.json as a dictionary - example fmginfo.json.example provided - <b> to use, rename to fmginfo.json! </b>
    - Device attributes in devices.json as list of dictionaries
    - Meta variables in metavars.json as a dictionary of dictionaries

## FortiManager API How-To
- https://how-to-fortimanager-api.readthedocs.io/en/latest/001_fmg_json_api_introduction.html

## API Best Practices
- https://docs.fortinet.com/document/fortimanager/7.6.0/api-best-practices/500458/introduction

## Mass Deployment Guide
- https://docs.fortinet.com/document/fortimanager/7.4.0/mass-provisioning-using-fortimanager/253438/introduction

## Example
- Example clean run without duplicate devices using json examples provided
    - sdbranch3 and sdbranch4 utilise the blueprint "Blueprint-60F" and policy package "branch"
    - sdbranch5 utilises the blueprint "BlueprintTest" and policy package "branchtest"

<img width="1879" height="236" alt="add model devices to fmg" src="https://github.com/user-attachments/assets/5035868e-47f5-415a-b674-d1e67e9cffea" />

```
Get existing devices status code = 200
Get existing devices message = OK
Existing devices are:
---
[{'name': 'sdbranch-hub1', 'oid': 6501, 'sn': 'FGVMMLTM24051093'},
 {'name': 'sdbranch1', 'oid': 6878, 'sn': 'FGT60FTK20026512'},
 {'name': 'sdbranch2', 'oid': 7060, 'sn': 'FGT60FTK20058168'}]
---
Filtered device list with existing devices removed:
---
[{'blueprint': 'Blueprint-60F',
  'description': 'Branch 3 - Parkville',
  'latitude': '-37.7787036',
  'longitude': '144.9426083',
  'mr': 6,
  'name': 'sdbranch3',
  'os_ver': '7.0',
  'platform_str': 'FortiGate-60F',
  'serial': 'FGT60FTK19000148'},
 {'blueprint': 'Blueprint-60F',
  'description': 'Branch 4 - Chadstone',
  'latitude': '-37.88784649999999',
  'longitude': '145.082586',
  'mr': 6,
  'name': 'sdbranch4',
  'os_ver': '7.0',
  'platform_str': 'FortiGate-60F',
  'serial': 'FGT60FTK20052158'},
 {'blueprint': 'BlueprintTest',
  'description': 'Branch 5 - Brunswick',
  'latitude': '-37.7670402',
  'longitude': '144.9621239',
  'mr': 6,
  'name': 'sdbranch5',
  'os_ver': '7.0',
  'platform_str': 'FortiGate-60F',
  'serial': 'FGT60FTK20094976'}]
---
Filtered metadata variables with existing devices removed:
---
{'sdbranch3': {'AP_intf': '10.137.136.65/26',
               'Internal_Intf': '10.137.137.1/24',
               'LAN_intf': '10.137.136.129/26',
               'WLAN_intf': '10.137.136.193/26',
               'branch_id': '3',
               'fortilink_intf': '10.137.136.1/26',
               'hostname': 'sdbranch3'},
 'sdbranch4': {'AP_intf': '10.137.138.65/26',
               'Internal_Intf': '10.137.139.1/24',
               'LAN_intf': '10.137.138.129/26',
               'WLAN_intf': '10.137.138.193/26',
               'branch_id': '4',
               'fortilink_intf': '10.137.138.1/26',
               'hostname': 'sdbranch4'},
 'sdbranch5': {'AP_intf': '10.137.140.65/26',
               'Internal_Intf': '10.137.141.1/24',
               'LAN_intf': '10.137.140.129/26',
               'WLAN_intf': '10.137.140.193/26',
               'branch_id': '4',
               'fortilink_intf': '10.137.140.1/26',
               'hostname': 'sdbranch5'}}
---
List of policy packages and assigned devices as derived from blueprints:
---
[{'branch': ['sdbranch3', 'sdbranch4']}, {'branchtest': ['sdbranch5']}]
---
Locking workspace before proceeding
---
Locking workspace response code = 200
Locking workspace response message = OK
---
Adding Model Device(s)
---
{
      "id": 1,
      "session": "39l9qQ1DcDGs2y5Fdd2f5XmUoP6Yx34W8ZSIkj6DAlEofw04WkCGSdaqzz674sa+KzXxgo9iz0r4dJgVq7Y45g==",
      "method": "exec",
      "params": [
            {
                  "url": "/dvm/cmd/add/dev-list",
                  "data": {
                        "adom": "sdbranch",
                        "add-dev-list": [
                              {
                                    "adm_usr": "admin",
                                    "desc": "Branch 3 - Parkville",
                                    "device action": "add_model",
                                    "device blueprint": "Blueprint-60F",
                                    "latitude": "-37.7787036",
                                    "longitude": "144.9426083",
                                    "mgmt_mode": "fmg",
                                    "mgt_vdom": "root",
                                    "name": "sdbranch3",
                                    "os_type": 0,
                                    "os_ver": "7.0",
                                    "mr": 6,
                                    "platform_str": "FortiGate-60F",
                                    "sn": "FGT60FTK19000148"
                              },
                              {
                                    "adm_usr": "admin",
                                    "desc": "Branch 4 - Chadstone",
                                    "device action": "add_model",
                                    "device blueprint": "Blueprint-60F",
                                    "latitude": "-37.88784649999999",
                                    "longitude": "145.082586",
                                    "mgmt_mode": "fmg",
                                    "mgt_vdom": "root",
                                    "name": "sdbranch4",
                                    "os_type": 0,
                                    "os_ver": "7.0",
                                    "mr": 6,
                                    "platform_str": "FortiGate-60F",
                                    "sn": "FGT60FTK20052158"
                              },
                              {
                                    "adm_usr": "admin",
                                    "desc": "Branch 5 - Brunswick",
                                    "device action": "add_model",
                                    "device blueprint": "BlueprintTest",
                                    "latitude": "-37.7670402",
                                    "longitude": "144.9621239",
                                    "mgmt_mode": "fmg",
                                    "mgt_vdom": "root",
                                    "name": "sdbranch5",
                                    "os_type": 0,
                                    "os_ver": "7.0",
                                    "mr": 6,
                                    "platform_str": "FortiGate-60F",
                                    "sn": "FGT60FTK20094976"
                              }
                        ],
                        "flags": "create_task"
                  }
            }
      ]
}
---
Add device(s) status code = 200
Add device(s) message = OK
---
Adding Metadata Variables
---
{
    "id": 1,
    "session": "39l9qQ1DcDGs2y5Fdd2f5XmUoP6Yx34W8ZSIkj6DAlEofw04WkCGSdaqzz674sa+KzXxgo9iz0r4dJgVq7Y45g==",
    "method": "add",
    "params": [
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch3",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.136.65/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/AP_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch3",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.137.1/24"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/Internal_Intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch3",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.136.129/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/LAN_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch3",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.136.193/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/WLAN_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch3",
                            "vdom": "global"
                        }
                    ],
                    "value": "3"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/branch_id/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch3",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.136.1/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/fortilink_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch3",
                            "vdom": "global"
                        }
                    ],
                    "value": "sdbranch3"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/hostname/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch4",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.138.65/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/AP_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch4",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.139.1/24"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/Internal_Intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch4",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.138.129/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/LAN_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch4",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.138.193/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/WLAN_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch4",
                            "vdom": "global"
                        }
                    ],
                    "value": "4"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/branch_id/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch4",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.138.1/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/fortilink_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch4",
                            "vdom": "global"
                        }
                    ],
                    "value": "sdbranch4"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/hostname/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch5",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.140.65/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/AP_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch5",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.141.1/24"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/Internal_Intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch5",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.140.129/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/LAN_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch5",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.140.193/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/WLAN_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch5",
                            "vdom": "global"
                        }
                    ],
                    "value": "4"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/branch_id/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch5",
                            "vdom": "global"
                        }
                    ],
                    "value": "10.137.140.1/26"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/fortilink_intf/dynamic_mapping"
        },
        {
            "data": [
                {
                    "_scope": [
                        {
                            "name": "sdbranch5",
                            "vdom": "global"
                        }
                    ],
                    "value": "sdbranch5"
                }
            ],
            "url": "/pm/config/adom/sdbranch/obj/fmg/variable/hostname/dynamic_mapping"
        }
    ]
}
---
Add metadata variables status code = 200
Add metadata variables = OK
Commit workspace response code = 200
Commit workspace response message = OK
---
Installing device(s)
---
Device install response code = 200
Device install message = OK
Commit workspace response code = 200
Commit workspace response message = OK
---
Installing policy package(s)
---
Policy install for policy package branch response code = 200
Policy install for policy package branch message = OK
Policy install for policy package branchtest response code = 200
Policy install for policy package branchtest message = OK
Commit workspace response code = 200
Commit workspace response message = OK
---
Unlocking workspace and logging out from session
---
Unlocking workspace status code = 200
Unlocking workspace message = OK
Logout response code = 200
Logout message = OK
---

```
