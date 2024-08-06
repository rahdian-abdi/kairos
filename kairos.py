import readline
import os
from discovery.curl_parser import parser_curl
from scanning.excessive_data_exposure import check_excessive_data_exposure
from scanning.injection_attack import check_injection_attacks
from scanning.remote_code_execution import check_rce_vulnerability

from scanning.bola_scanner import check_bola_vulnerability
from scanning.bua_scanner import fuzz_bua_vulnerability
from scanning.bopla import bopla_test
from scanning.unrestricted_resource_consumption import urc_test
from scanning.bfla import bfla_test
# API6:2023 - Unrestricted Access to Sensitive Business Flows
from scanning.server_side_request_forgery import ssrf_test
from scanning.security_misconfiguration import check_security_misconfiguration
from scanning.improper_asset_management import improper_asset_management_test
# API10:2023 - Unsafe Consumption of APIs
from fuzzing.fuzzer import fuzz_api



def print_banner():
    banner = """             
  _         _               
 | |       (_)              
 | | ____ _ _ _ __ ___  ___ 
 | |/ / _` | | '__/ _ \/ __|
 |   < (_| | | | | (_) \__ \ 
 |_|\_\__,_|_|_|  \___/|___/ v1.0.0 

                                                                          
This tool scans APIs for common vulnerabilities inspired by OWASP API Top 10 by simply using your API cURL.
The purposes are to detect and address security flaws to safeguard your APIs effectively.

Find me on \033[94mhttps://www.linkedin.com/in/rahdianabdi/\033[0m

Type 'help' to see available commands
"""
    print(banner)


def show_help():
    help_text = """
    Commands:
    --------------------------
    input       - Enter kairos_options custom payload. Enter 'done' when complete
    payload     - Show the current payload
    fuzz        - Fuzzing randomly the API
    scan        - Scan the provided API for vulnerabilities
    exit        - Exit the tool

    Command for kairos_options:
    ---------------------------
    set curlList <file_location>  : Specify the file containing the list of cURL commands.
    set bolaFile <file_location>  : Specify the custom file for Broken Object Level Authorization.
    set buaFile <file_location>   : Specify the fuzzing file for Broken User Authentication.
    set buaParameter <parameter>  : Specify the parameter to fuzz for Broken User Authentication.
    set boplaMethod <method>      : Specify the HTTP method for Broken Object Property Level Authorization.
    set boplaPayload              : Specify the payload for Broken Object Property Level Authorization. Enter 'done' when finished.
    set urcFile <file_location>   : Specify the fuzzing file for Unrestricted Resource Consumption.
    set urcParameter <parameter>  : Specify the parameter to fuzz for Unrestricted Resource Consumption.
    set ssrfParameter <parameter> : Specify the parameter to fuzz for Server Side Request Forgery.
    """
    print(help_text)

def exit():
    exit_text = "\nGood bye!"
    print(exit_text)

def other_input():
    print("Command not found! Try to type 'help'") 

# Global Variable
curl_list = ""
bola_file = ""
bua_file = ""
bua_parameter = ""
bopla_method = ""
bopla_payload = {}
urc_file = ""
urc_parameter = ""
ssrf_parameter = ""    

def collect_user_input():
    global curl_list, bola_file, bua_file, bua_parameter, bopla_method, bopla_payload, urc_file, urc_parameter, ssrf_parameter
    while True:
        command_options = input("\033[94m" + "kairos_options\033[0m > ").strip()
        chunks_command_options = command_options.split(' ')
        if chunks_command_options[0].lower() == 'set':
            if chunks_command_options[1] == 'curlList':
                curl_list = chunks_command_options[2]
            elif chunks_command_options[1] == 'bolaFile':
                bola_file = chunks_command_options[2]
            elif chunks_command_options[1] == 'buaFile':
                bua_file = chunks_command_options[2]
            elif chunks_command_options[1] == 'buaParameter':
                bua_parameter = chunks_command_options[2]
            elif chunks_command_options[1] == 'boplaMethod':
                bopla_method = chunks_command_options[2]
            elif chunks_command_options[1] == 'boplaPayload':
                while True:
                    field = input("> Enter the field you want to change or add: ")
                    if field.lower() == 'done':
                        break
                    value = input(f"> Enter the value for {field}: ")
                    bopla_payload[field] = value
            elif chunks_command_options[1] == 'urcFile':
                urc_file = chunks_command_options[2]
            elif chunks_command_options[1] == 'urcParameter':
                urc_parameter = chunks_command_options[2]
            elif chunks_command_options[1] == 'ssrfParameter':
                ssrf_parameter = chunks_command_options[2]
            else:
                print(f"Payload is not recognized")    
        elif chunks_command_options[0].lower() == 'done':
            break
        else:
            print(f"Command not recognized!")
def show_user_options():
    options_show = f"""
    Custom Input:
    -------------------
    cURL File        - {curl_list}
    BOLA File        - {bola_file}
    BUA File         - {bua_file}
    BUA Parameter    - {bua_parameter}
    BOPLA Method     - {bopla_method}
    BOPLA Payload    - {bopla_payload}
    URC File         - {urc_file}
    URC Parameter    - {urc_parameter}
    SSRF Parameter   - {ssrf_parameter}
    """
    print(options_show)

def fuzzing_api(base_url):
    method, url, headers, body = parser_curl(base_url)
    print("Running API Fuzzing...")
    print(f"\n╔══════════╣ RANDOM VALUE FUZZING\n")
    fuzz_api(method, url, headers, body)

          

def scan_api(base_url, uuid_file, parameter_bua_file, fuzz_param_bua, custom_method_bopla, custom_body_bopla, urc_fuzz_file, fuzz_param_urc, fuzz_param_ssrf):
    method, url, headers, body_json = parser_curl(base_url)
    print("Running scan...")
    print(f"\n╔══════════╣ BROKEN OBJECT LEVEL AUTHORIZATION\n")
    check_bola_vulnerability(method, url, headers, body_json, uuid_file)
    print(f"\n╔══════════╣ BROKEN USER AUTHENTICATION\n")
    fuzz_bua_vulnerability(method, url, headers, body_json, parameter_bua_file, fuzz_param_bua)
    print(f"\n╔══════════╣ BROKEN OBJECT PROPERTY LEVEL AUTHORIZATION\n")
    bopla_test(method, url, headers, body_json, custom_method_bopla, custom_body_bopla)
    print(f"\n╔══════════╣ UNRESTRICTED RESOURCE CONSUMPTION\n")
    urc_test(method, url, headers, body_json, urc_fuzz_file, fuzz_param_urc)
    print(f"\n╔══════════╣ BROKEN FUNCTION LEVEL AUTHORIZATION\n")
    bfla_test(method, url, headers, body_json)
    # API6 2023
    print(f"\n╔══════════╣ SERVER SIDE REQUEST FORGERY\n")
    ssrf_test(method, url, headers, body_json, fuzz_param_ssrf)
    print(f"\n╔══════════╣ SECURITY MISCONFIGURATION\n")
    check_security_misconfiguration(method, url, headers, body_json)
    print(f"\n╔══════════╣ IMPROVER ASSET/INVENTORY MANAGEMENT\n")
    improper_asset_management_test(method, url, headers, body_json)
    # API10 2023
    print(f"\n╔══════════╣ EXCESSIVE DATA EXPOSURE\n")
    check_excessive_data_exposure(method, url, headers)
    print(f"\n╔══════════╣ INJECTION\n")
    check_injection_attacks(method, url, headers, body_json)
    print(f"\n╔══════════╣ REMOTE CODE EXECUTION\n")
    check_rce_vulnerability(method, url, headers, body_json)


def main():
    print_banner()

    while True:
        command = input("\033[4m" + "kairos\033[0m > ").strip().lower()
        
        if command == 'help':
            show_help()    
        elif command == 'input':
            collect_user_input()
        elif command == 'payload':
            show_user_options()
        elif command == 'fuzz':
            curl_extracted = []
            if curl_list and os.path.isfile(curl_list):
                with open(curl_list, 'r') as curl_raw:
                    curl_extracted = [curl.strip() for curl in curl_raw.readlines()]
                    print("\033[92m" + f"[v] cURL list loaded from {curl_list}" + "\033[0m")
                    for single_url in curl_extracted:
                        fuzzing_api(single_url)
                    print(f"\nAPI scan is complete!\n")
            else:
                print("\033[93m" + f"[!] No cURL file loaded." + "\033[0m")



        elif command == 'scan':
            # Main Scan
            curls = []
            if curl_list and os.path.isfile(curl_list):
                with open (curl_list, 'r') as curl_f:
                    curls = [curl.strip() for curl in curl_f.readlines()]
                print("\033[92m" + f"[v] cURL list loaded from {curl_list}" + "\033[0m")
                for single_url in curls:
                    scan_api(single_url, bola_file, bua_file, bua_parameter, bopla_method, bopla_payload, urc_file, urc_parameter, ssrf_parameter)
                print(f"\nAPI scan is complete!\n")
            else:
                print("\033[93m" + f"[!] No cURL file loaded." + "\033[0m") 
            
        elif command == 'exit':
            exit()
            break
        else:
            other_input()

if __name__ == "__main__":
    main()        

