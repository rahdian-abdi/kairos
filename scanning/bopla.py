import requests

def bopla_test(method, url, headers, body=None, custom_method=None, custom_body=None):
    method = custom_method if custom_method else method
    body = {} if body is None else body
    mass_assignment_payload = {**body, **custom_body}
    
    response = requests.request(method, url, headers=headers, json=mass_assignment_payload)
    
    for field in custom_body:
        if field in response.text or response.status_code == 200:
            print(f"\033[91m[!] BOPLA vulnerability detected: {field} and value {custom_body[field]}!\033[0m") if method != 'GET' else print('')
            print(f"\033[91m[!] BOPLA assignment vulnerability detected: Status code {response.status_code}, change accepted!\033[0m") if method != 'GET' else print('')
        else:
            print(f"\n\033[92m[v] No BOPLA vulnerability detected for field: {field}.\033[0m")

    methods = ['GET','POST','PUT','DELETE','HEAD','OPTIONS','TRACE','CONNECT','PATCH']
    print(f"\n\033[93m[-] Further inspect response for every methods\033[0m\n")
    for m in methods:
        response = requests.request(m, url, headers=headers)
        print(f"\033[93mResponse for method {m}\033[0m")
        print(f"Response status: {response.status_code}")
        print(f"Response Content: {response.content}\n")
