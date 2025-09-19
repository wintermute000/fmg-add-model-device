Script to add model devices to FortiManager
---

Tested on 7.6.4 and FG-60F on 7.6.4

Requirements:
- Blueprint including policy package assignment (https://docs.fortinet.com/document/fortimanager/7.6.4/administration-guide/55038/using-device-blueprints-for-model-devices)
- Single policy package (roadmap: support for multiple policy packages)
- FortiManager administrative user with JSON RPC read/write access
- FortiManager username as environmental variable (EXPORT FMGUSERNAME=xyz)
- FortiManager password as environmental variable (EXPORT FMGPASSWORD=xyz)
- Workspace mode (comment out lock/unlock/commit if not required)
- FortiManager attributes (ADOM, policy package, URL) in fmginfo.json as a dictionary - example fmginfo.json.example provided - <b> to use, rename to fmginfo.json! </b>
- Device attributes in devices.json as list of dictionaries
- Meta variables in metavars.json as a dictionary of dictionaries

##Full credit to the FortiManager API How-To
- https://how-to-fortimanager-api.readthedocs.io/en/latest/001_fmg_json_api_introduction.html


##API Best Practices
- https://docs.fortinet.com/document/fortimanager/7.6.0/api-best-practices/500458/introduction

##Mass Deployment Guide
- https://docs.fortinet.com/document/fortimanager/7.4.0/mass-provisioning-using-fortimanager/253438/introduction
