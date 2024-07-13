import json
import requests
import shlex

def parser_curl(curl_command):
    try:
        curl_tokens = shlex.split(curl_command)

        url = None
        for token in curl_tokens:
            if token.startswith("http://") or token.startswith("https://"):
                url = token
                break
        if not url:
            raise ValueError("URL not found in curl command.")

        headers = {}
        for i, token in enumerate(curl_tokens):
            if token == '--header' or token == '-H':
                header_value_index = i + 1
                if header_value_index < len(curl_tokens):
                    header_value = curl_tokens[header_value_index]
                    if ':' in header_value:
                        header_name, header_content = header_value.split(':', 1)
                        headers[header_name.strip()] = header_content.strip()

        body_data = None                       
        for i, token in enumerate(curl_tokens):
            if token == '--data' or token == '-d':
                data_value_index = i + 1
                if data_value_index < len(curl_tokens):
                    body_data = curl_tokens[data_value_index]
                break

        method = 'GET'        
        for token in curl_tokens:
            if token.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']:
                method = token.upper()
                break
        
        print(f"") 
        print(f"")        
        print(f"[+] Method: {method}")
        print(f"[+] Scanning API at URL: {url}")
        print(f"[+] Headers: {headers}")
        print(f"[+] Body: {body_data}")
        print(f"")
        print(f"")
        
        if body_data:
            try:
                body_json = json.loads(body_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")
                body_json = None
        else:
            body_json = None

        return method, url, headers, body_json

    except ValueError as ve:
        print(f"Error parsing curl command: {ve}")
    except IndexError as ie:
        print(f"Invalid curl command format: {ie}")