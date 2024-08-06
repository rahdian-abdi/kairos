import requests
import random
import string
import time
from typing import Dict, Any

def fuzz_value(value: Any) -> Any:
	if isinstance(value, str):
		return ''.join(random.choices(string.printable, k=len(value)))
	elif isinstance(value, int):
		return random.randint(-1000000, 1000000)
	elif isinstance(value, float):
		return random.uniform(-1000000, 1000000)
	elif isinstance(value, bool):
		return random.choice([True, False])
	elif isinstance(value, list):
		return [fuzz_value(v) for v in value]
	elif isinstance(value, dict):
		return {k: fuzz_value(v) for k,v in value.items()}
	else:
		return value

def fuzz_dict(data: Dict[str, Any]) -> Dict[str, Any]:
	return {k: fuzz_value(v) for k, v in data.items()}

def fuzz_api(method: str, url: str, headers: Dict[str, Any]=None, body: Dict[str, Any]=None):
	fuzzed_headers = fuzz_dict(headers) if headers else {}
	fuzzed_body = fuzz_dict(body) if body else {}
	try:
		response = requests.request(method, url, headers=fuzzed_headers, json=fuzzed_body, timeout=5)
		print(f"\033[93m[!] Status Code: {response.status_code}\033[0m")
		print(f"\033[93m[!] Analyzing response: {response.text}\033[0m")
	except requests.exceptions.RequestException as e:
		print(f"\033[93m[!]Error while requesting: {str(e)}\033[0m")			