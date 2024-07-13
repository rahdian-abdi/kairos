import readline
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
    -------------------
    scan        - Scan the provided API for vulnerabilities
    exit        - Exit the tool
    """
    print(help_text)

def exit():
    exit_text = "\nGood bye!"
    print(exit_text)

def other_input():
    print("Command not found! Try to type 'help'")    

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
        elif command == 'scan':
            url = input("\ncURL > ").strip()

            # BOLA
            print(f"\n\033[93m[-] Custom file for Broken Object Level Authorization Test.\033[0m\n")
            uuid_file_bola = input("> UUID file: ")
            # BUA
            print(f"\n\033[93m[-] Custom file and parameter for Broken User Authentication Test.\033[0m\n")
            parameter_bua_file = input("> Fuzz file: ")
            fuzz_param_bua = input("> Parameter to fuzz: ").strip()
            # BOPLA
            print(f"\n\033[93m[-] Custom method and payload for Broken Object Property Level Authorization Test.\033[0m\n")
            custom_method_bopla = input("> HTTP method (GET, POST, PUT, DELETE): ").upper()
            custom_body_bopla = {}
            print(f"\n\033[94mCustom payload for BOPLA. Type 'done' when you finish\033[0m\n")
            while True:
                field = input("> Enter the field you want to change or add: ")
                if field.lower() == 'done':
                    break
                value = input(f"> Enter the value for {field}: ")
                custom_body_bopla[field] = value
            # URC
            print(f"\n\033[93m[-] Custom file and payload parameter for Unrestricted Resource Consumption Test.\033[0m\n")
            custom_file_urc = input("> Fuzz file: ")
            fuzz_param_urc = input("> Parameter to fuzz: ")
            # BFLA
            # API6-2023
            # SSRF
            print(f"\n\033[93m[-] Custom payload parameter for Server Side Request Forgery Test.\033[0m\n")
            fuzz_param_ssrf = input(f"> Parameter to fuzz: ")
            # SM
            # IAM
            # API10-2023

            # Main Scan
            scan_api(url, uuid_file_bola, parameter_bua_file, fuzz_param_bua, custom_method_bopla, custom_body_bopla, custom_file_urc, fuzz_param_urc, fuzz_param_ssrf)
            print(f"\nAPI scan is complete!\n")
        elif command == 'exit':
            exit()
            break
        else:
            other_input()

if __name__ == "__main__":
    main()        

