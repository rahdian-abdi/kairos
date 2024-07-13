import requests

def mass_assignment_test(method, url, headers, body=None):
    method_updated = input("[-] Enter the HTTP method (GET, POST, PUT, DELETE): ").upper()
    method = method_updated if method_updated else method
    fields_values = {}
    while True:
        field = input("[-] Enter the field you want to change (or type 'done' to finish): ")
        if field.lower() == 'done':
            break
        value = input(f"[-] Enter the value for {field}: ")
        fields_values[field] = value
    body = {} if body is None else body
    mass_assignment_payload = {**body, **fields_values}
    # print(method)
    # print(url)
    # print(headers)
    # print(mass_assignment_payload)
    
    response = requests.request(method, url, headers=headers, json=mass_assignment_payload)
    # print(response.text)
    
    for field in fields_values:
        if field in response.text or response.status_code == 200:
            print(f"\n\033[91m[!] Mass assignment vulnerability detected: {field} and value {fields_values[field]}!\033[0m")
            print(f"\033[91m[!] Mass assignment vulnerability detected: Status code {response.status_code}, change accepted!\033[0m")
        else:
            print(f"\n\033[92m[v] No mass assignment vulnerability detected for field: {field}.\033[0m")