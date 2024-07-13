import json
import requests
import re

def bfla_test(method, url, headers, body=None):
    modified_urls = []
    if "user" in url or "users" in url:
        modified_urls.append(re.sub(r"user(s)?", r"admin\1", url))
        modified_urls.append(re.sub(r"user(s)?", r"administrator\1", url))

    if not modified_urls:
        print("\033[92m[v] No user-related keywords found in URL.\033[0m")
        modified_urls.append(url)

    methods = ['GET', 'POST', 'PUT', 'DELETE']
    modified_body = body.copy() if body else {}
    if 'is_admin' in modified_body:
        modified_body['is_admin'] = True
    elif 'isAdmin' in modified_body:
        modified_body['isAdmin'] = True
    else:
        modified_body['is_admin'] = True

    for m in methods:
        if m == 'GET' or m == 'DELETE':
            for mod_url in modified_urls:
                if not modified_urls:
                    print(f"[-] Testing modified URL: {mod_url}")
                    response = requests.request(m, mod_url, headers=headers)

                    if response.status_code == 200:
                        print(f"\033[91m[!] Method {m}: BFLA vulnerability detected! Unauthorized access granted.\033[0m")
                    else:
                        print(f"\033[92m[v] Method {m}: No BFLA vulnerability. Unauthorized access denied.\033[0m")
        else:
            for mod_url in modified_urls:
                print(f"[-] Testing modified URL: {mod_url}")

                response = requests.request(m, mod_url, headers=headers, json=modified_body)

                if response.status_code == 200:
                    print(f"\033[91m[!] Method {m}: BFLA vulnerability detected! Unauthorized access granted.\033[0m")
                else:
                    print(f"\033[92m[v] Method {m}: No BFLA vulnerability. Unauthorized access denied.\033[0m")            
