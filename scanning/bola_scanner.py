import requests
import re
import uuid
import os
from time import sleep
from tqdm import tqdm

def check_bola_vulnerability(method, url, headers, body, uuid_file=None):
    uuids_to_test = []

    if uuid_file and os.path.isfile(uuid_file):
        with open(uuid_file, 'r') as file:
            uuids_to_test = [line.strip() for line in file.readlines()]
        print("\033[92m" + f"[v] UUIDs loaded from {uuid_file}" + "\033[0m")
    else:
        print("\033[93m" + "[!] No UUID file provided or file does not exist, generating random UUIDs" + "\033[0m")

    path_param_match = re.search(r'/([a-zA-Z0-9_-]*:?[0-9a-fA-F-]{36}|\d+)(/|$)', url)
    if path_param_match:
        base_url = url[:path_param_match.start()] + url[path_param_match.end():]
        id_in_path = path_param_match.group(1)  # Take first match

        if re.match(r'^[a-zA-Z0-9_-]*:[0-9a-fA-F-]{36}$', id_in_path) or re.match(r'^[0-9a-fA-F-]{36}$', id_in_path):  # Check if the ID is a (prefixed) UUID
            print("\033[92m" + "[v] UUID or prefixed UUID found in path!" + "\033[0m")
            prefix = id_in_path.split(':')[0] if ':' in id_in_path else ''
            if not uuids_to_test:
                uuids_to_test = [f"{prefix}:{str(uuid.uuid4())}" if prefix else str(uuid.uuid4()) for _ in range(10)]
            
            total = len(uuids_to_test)
            with tqdm(total=total, desc="Fuzzing Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
                for test_uuid in uuids_to_test:
                    test_url = url[:path_param_match.start()+1] + test_uuid + url[path_param_match.end()-1:]
                    response = requests.request(method, test_url, headers=headers, json=body)
                    if response.status_code == 200:
                        print("\033[91m" + f"[!] BOLA vulnerability detected with UUID {test_uuid}!" + "\033[0m")
                        return
                    pbar.update(1)
                    sleep(0.1)
            print("\033[92m" + "[-] No BOLA detected with provided UUIDs" + "\033[0m")
        else:  # The ID is an integer
            print("\033[92m" + "[v] Integer ID found in path!" + "\033[0m")
            total = 10
            with tqdm(total=total, desc="Fuzzing Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
                for test_id in range(1, 11):
                    test_url = url[:path_param_match.start()+1] + str(test_id) + url[path_param_match.end()-1:]
                    response = requests.request(method, test_url, headers=headers, json=body)
                    if response.status_code == 200:
                        print("\033[91m" + f"[!] BOLA vulnerability detected with ID {test_id}!" + "\033[0m")
                        return
                    pbar.update(1)
                    sleep(0.1)
            print("\033[92m" + "[-] No BOLA detected with provided integer IDs" + "\033[0m")
    else:
        print("\033[93m" + f"[!] No ID found in path!" + "\033[0m")

    if '?' in url:
        base_url, query_params = url.split('?', 1)
        param_match = re.search(r'([a-zA-Z0-9_]*[iI]d)=([0-9a-fA-F-]{36}|\d+)', query_params)
        if param_match:
            param_name = param_match.group(1)
            param_value = param_match.group(2)

            if re.match(r'^[0-9a-fA-F-]{36}$', param_value): 
                print("\033[92m" + "[v] UUID found in query parameter!" + "\033[0m")
                if not uuids_to_test:
                    uuids_to_test = [str(uuid.uuid4()) for _ in range(10)]
                
                total = len(uuids_to_test)
                with tqdm(total=total, desc="Fuzzing Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
                    for test_uuid in uuids_to_test:
                        test_url = f"{base_url}?{param_name}={test_uuid}"
                        response = requests.request(method, test_url, headers=headers, json=body)
                        if response.status_code == 200:
                            print("\033[91m" + f"[!] BOLA vulnerability detected with UUID {test_uuid}!" + "\033[0m")
                            return
                        pbar.update(1)
                        sleep(0.1)
                print("\033[92m" + "[-] No BOLA detected with provided UUIDs" + "\033[0m")
            else: 
                print("\033[92m" + "[v] Integer ID found in query parameter!" + "\033[0m")
                total = 10
                with tqdm(total=total, desc="Fuzzing Progress", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
                    for test_id in range(1, 11):
                        test_url = f"{base_url}?{param_name}={test_id}"
                        response = requests.request(method, test_url, headers=headers, json=body)
                        if response.status_code == 200:
                            print("\033[91m" + f"[!] BOLA vulnerability detected with ID {test_id}!" + "\033[0m")
                            return
                        pbar.update(1)
                        sleep(0.1)
                print("\033[92m" + "[-] No BOLA detected with provided integer IDs" + "\033[0m")
        else:
            print("\033[93m" + "[!] No ID parameter found in URL!" + "\033[0m")
    else:
        print("\033[93m" + "[!] No query parameters found in URL!" + "\033[0m")
