import requests
import json
import re

def check_excessive_data_exposure(method, url, headers=None):
    response = requests.request(method, url, headers=headers)
    
    if response.status_code == 200:
        data = response.text
        sensitive_fields = [
            "ssn", "social_security_number", "tax_id", "itin", "dob", "date_of_birth",
            "email", "phone", "address", "postal_code", "zip_code", "credit_card",
            "card_number", "expiration_date", "cvv", "security_code", "bank_account",
            "account_number", "routing_number", "password", "secret", "api_key",
            "token", "private_key", "secret_key", "medical", "health", "diagnosis",
            "prescription", "insurance", "beneficiary", "policy_number", "license",
            "driver_license", "passport", "deviceid", "device_id", "lat", "long",
            "latitude", "longitude", "mac_address", "imei", "ip_address", "security_question",
            "security_answer", "otp", "one_time_password", "biometric", "fingerprint",
            "facial_recognition", "voice_print", "genetic", "dna", "hiv_status"
        ]

        fields_match = re.findall(r'[a-zA-Z0-9_]*[iI]d', data)
        exposed_fields = [field for field in sensitive_fields if field in data]
        exposed_fields.extend([field for field in fields_match if field not in exposed_fields])

        if exposed_fields or fields_match:
            print(f"\033[91m[!] Excessive data exposure detected: {', '.join(exposed_fields)}\033[0m")
        else:
            print("\033[92m[-] No excessive data exposure detected.\033[0m")
    else:
        print(f"\033[91m[!] Request failed with status code: {response.status_code}\033[0m")
