import json
import requests
import os

def fuzz_bua_vulnerability(method, url, headers, body=None, parameter_bua_file=None, fuzz_param_bua=None):
    if not os.path.isfile(parameter_bua_file):
        print(f"\033[91m[!] The file {parameter_bua_file} does not exist. Exiting.\033[0m")
        return None, None

    with open(parameter_bua_file, 'r') as file:
        parameter_list = [line.strip() for line in file.readlines()]

    bua_detected = False
    evil_payload = []
    body = {} if body is None else body

    for value in parameter_list:
        # Create a payload with the fuzzed parameter
        payload = {**body, fuzz_param_bua: value}
        
        # Send the request
        response = requests.request(method, url, headers=headers, json=payload)
        
        # Check for successful authentication or other indicators of a BUA vulnerability
        if response.status_code == 200:
            bua_detected = True
            evil_payload.append(value)

    if evil_payload:
        for i, val in enumerate(evil_payload):
            print(f"\033[91m[!] Detected evil payload: {val}\033[0m")
    else:
        print(f"\033[92m[v] No BUA detected!\033[0m")
