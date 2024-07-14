import json
import requests
import os
from tqdm import tqdm
from time import sleep

def fuzz_bua_vulnerability(method, url, headers, body=None, parameter_bua_file=None, fuzz_param_bua=None):
    if not os.path.isfile(parameter_bua_file):
        print(f"\033[91m[!] The file {parameter_bua_file} does not exist. Exiting.\033[0m")
        return None, None

    with open(parameter_bua_file, 'r') as file:
        parameter_list = [line.strip() for line in file.readlines()]

    total = len(parameter_list)
    bua_detected = False
    evil_payload = []
    body = {} if body is None else body

    with tqdm(total=total, desc="[-] Fuzzing Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        for value in parameter_list:
            payload = {**body, fuzz_param_bua: value}
            
            response = requests.request(method, url, headers=headers, json=payload)
            
            if response.status_code == 200:
                bua_detected = True
                evil_payload.append(value)

            pbar.update(1)
            sleep(0.1) 

    if evil_payload:
        for i, val in enumerate(evil_payload):
            print(f"\033[91m[!] Detected evil payload: {val}\033[0m")
    else:
        print(f"\033[92m[v] No BUA is detected!\033[0m")