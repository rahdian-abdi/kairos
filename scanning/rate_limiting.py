import requests
import json
import time
import shlex
import re
import os

def rate_limiting_test(method, url, headers, body, rl_file=None):
    if rl_file is None:
        print("\033[91m[!] Rate limiting file path is not provided. Exiting.\033[0m")
        return
    elif not os.path.isfile(rl_file):
        print(f"\033[91m[!] The file {rl_file} does not exist or is not a file. Exiting.\033[0m")
        return
    
    # Load fuzzing values from the file
    with open(rl_file, 'r') as file:
        fuzz_values = [line.strip() for line in file.readlines()]


    if method == "GET":
        print("\033[94m" + "Running rate limiting test for GET requests..." + "\033[0m")
        start_time = time.time()
        for i in range(100):
            response = requests.get(url, headers=headers)
            print(f"Request {i+1}: {response.status_code}")
            if response.status_code == 429:
                print("\033[92m" + "[v] Rate limiting detected!" + "\033[0m")
                return
            time.sleep(1 / request_count)
        total_time = time.time() - start_time
        print(f"\033[94mFinished sending {request_count} requests in {total_time:.2f} seconds.\033[0m")
        print("\033[91m" + "[!] No rate limiting detected, API might be vulnerable to LOR!" + "\033[0m")
    else:
        fuzz_param = input("Enter the payload parameter to fuzz: ")
        print(f"\033[94mRunning rate limiting test for {method} requests...\033[0m")
        start_time = time.time()
        for i, fuzz_value in enumerate(fuzz_values):
            if i >= 100:
                break
            # payload = body.copy()
            # payload[fuzz_param] = fuzz_value
            payload = {**body, fuzz_param: int(fuzz_value) if fuzz_value.isdigit() else fuzz_value}
            response = requests.request(method, url, headers=headers, json=payload)
            print(f"Request {i+1}: {response.status_code}")
            if response.status_code == 429:
                print("\033[92m" + "[v] Rate limiting detected!" + "\033[0m")
                return
        total_time = time.time() - start_time
        print(f"\033[94mFinished sending {min(100, len(fuzz_values))} requests in {total_time:.2f} seconds.\033[0m")
        print("\033[91m" + "[!] No rate limiting detected, API might be vulnerable to LOR!" + "\033[0m")
