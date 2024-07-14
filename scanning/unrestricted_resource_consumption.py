import requests
import json
import time
import shlex
import re
import os

def urc_test(method, url, headers, body=None, urc_fuzz_file=None, fuzz_param_urc=None):
    if urc_fuzz_file is None:
        print("\033[91m[!] Unrestricated resource consumption file path is not provided.\033[0m")
        return
    elif not os.path.isfile(urc_fuzz_file):
        print(f"\033[91m[!] The file {urc_fuzz_file} does not exist or is not a file.\033[0m")
        return
    
    with open(urc_fuzz_file, 'r') as file:
        fuzz_values = [line.strip() for line in file.readlines()]

    body = {} if body is None else body  
    request_count = 15  


    if method == "GET":
        print("\033[94m" + "Unrestricated resource consumption test for GET requests..." + "\033[0m")
        start_time = time.time()
        for i in range(15):
            response = requests.get(url, headers=headers)
            print(f"Request {i+1}: {response.status_code}")
            if response.status_code == 429:
                print("\033[92m" + "[v] Limiting request detected!" + "\033[0m")
                return
            time.sleep(1 / request_count)
        total_time = time.time() - start_time
        print(f"\033[94mFinished sending {request_count} requests in {total_time:.2f} seconds.\033[0m")
        print("\033[91m" + "[!] No limiting request detected, higher possibility for Unrestricated Resource consumption vulnerability!" + "\033[0m")
    else:
        print(f"\033[94mRunning rate limiting test for {method} requests...\033[0m")
        start_time = time.time()
        for i, fuzz_value in enumerate(fuzz_values):
            if i >= 15:
                break
            payload = {**body, fuzz_param_urc: int(fuzz_value) if fuzz_value.isdigit() else fuzz_value}
            response = requests.request(method, url, headers=headers, json=payload)
            print(f"Request {i+1}: {response.status_code}")
            if response.status_code == 429:
                print("\033[92m" + "[v] Limiting request detected!" + "\033[0m")
                return
        total_time = time.time() - start_time
        print(f"\033[94mFinished sending {min(100, len(fuzz_values))} requests in {total_time:.2f} seconds.\033[0m")
        print("\033[91m" + "[!] No limiting request detected, higher possibility for Unrestricated Resource consumption vulnerability!" + "\033[0m")
