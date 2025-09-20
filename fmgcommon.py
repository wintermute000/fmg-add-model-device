import requests
import json
import urllib3

headers = {'Content-Type': 'application/json'}

def login(username, password, fortimanager_url):
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
    response_json = response.json()

    if response.status_code == 200:
        # Extract session token from the response
        session_token = response.json().get('session')
        return session_token
    else:
        print(f"Login failed. Status code: {response.status_code}")
        print('Login message =', response_json["result"][0]["status"]["message"])
        return None

def logout(session_token, fortimanager_url):
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

def lock(session_token, adom, fortimanager_url):
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
            logout(session_token, fortimanager_url)
            quit()

    else:
        print(f"Workspace lock failed. Status code: {response.status_code}")
        # Log out and quit
    
def unlock(session_token, adom, fortimanager_url):
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


def commit(session_token, adom, fortimanager_url):
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

