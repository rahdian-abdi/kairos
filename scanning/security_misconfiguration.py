import requests

def check_security_misconfiguration(method, url, headers, body=None):
    if body is None:
        body = {}

    try:
        response = requests.request(method, url, headers=headers, json=body)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"\033[91m[!] An error occurred: {e}\033[0m")
        return
    
    security_headers = [
        "Strict-Transport-Security", 
        "Content-Security-Policy", 
        "X-Content-Type-Options", 
        "X-Frame-Options", 
        "X-XSS-Protection"
    ]
    
    missing_headers = [header for header in security_headers if header not in response.headers]
    
    if missing_headers:
        print("\033[91m[!] Security misconfiguration detected! Missing headers:\033[0m", missing_headers)
    else:
        print("\033[92m[v] No security misconfiguration detected. All security headers are present.\033[0m")
    
    cors_headers = [
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Credentials", "true")
    ]
    
    for header, value in cors_headers:
        if response.headers.get(header) == value:
            print(f"\033[91m[!] Dangerous CORS configuration detected: {header} is set to '{value}'!\033[0m")
