<div align="center">
  <a href="">
    <img src="files/banner.png" width="800" height="288">
  </a>

  <p align="center">
    Kairos v1.0.0
  </p>
</div>

# Kairos API Security Scanner

Kairos is a comprehensive API security scanner designed to identify common vulnerabilities in your APIs inspired by the OWASP API Top 10. By simply using your API cURL command, Kairos scans and reports potential security flaws to help you safeguard your APIs effectively.

## Features

- **Broken Object Level Authorization (BOLA)**
- **Broken User Authentication (BUA)**
- **Broken Object Property Level Authorization (BOPLA)**
- **Unrestricted Resource Consumption (URC)**
- **Broken Function Level Authorization (BFLA)**
- **Server Side Request Forgery (SSRF)**
- **Security Misconfiguration**
- **Improper Asset/Inventory Management**
- **Excessive Data Exposure**
- **Injection Attacks**
- **Remote Code Execution**

## Log Update
- Version 1.0.0 (7/14/2024) Refactor and can add cURL list file for multiple scan. Must be one line and separated by line 

## Requirements

Before using Kairos, ensure you have the following installed:

- Python 3.6+

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/kairos.git
cd kairos
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

1. **Run Kairos:**
```bash
python3 kairos.py
```

2. **Commands:**
    - **`help`**: Display available commands.
    - **`scan`**: Start a new API scan.
    - **`exit`**: Exit the tool.

### Scanning an API

1. **Input your API cURL command.**

2. **Provide custom files and parameters for different tests:**
    - **Broken Object Level Authorization Test:** Utilize a custom UUID file. If you have a list of valid UUIDs, it will help test this effectively.
    - **Broken User Authentication Test:** Employ a custom file and parameter for fuzzing. Specific payloads, like OTPs, can be provided for testing.
    - **Broken Object Property Level Authorization Test:** Customize HTTP methods and payloads to test if certain methods return unintended responses.
    - **Unrestricted Resource Consumption Test:** Use a custom file and payload parameter to test if there are any limits for requests.
    - **Server Side Request Forgery Test:** Custom payload parameter. Implement a custom payload parameter to check if specific parameters call URLs within the application, potentially replaced by common URL metadata.

    All the payloads are optional, you can adjust based on your need.

### Example

```bash
kairos > scan
cURL > curl -X GET -H "Authorization: Bearer token" http://example.com/api/v1/resource

[-] Custom file for Broken Object Level Authorization Test.
> UUID file: uuid.txt

[-] Custom file and parameter for Broken User Authentication Test.
> Fuzz file: bua_fuzz.txt
> Parameter to fuzz: password

[-] Custom method and payload for Broken Object Property Level Authorization Test.
> HTTP method (GET, POST, PUT, DELETE): PUT
> Enter the field you want to change or add: status
> Enter the value for status: returned
> Enter the field you want to change or add: done

[-] Custom file and payload parameter for Unrestricted Resource Consumption Test.
> Fuzz file: urc_fuzz.txt
> Parameter to fuzz: email

[-] Custom payload parameter for Server Side Request Forgery Test.
> Parameter to fuzz: url
```

## File Structure

- **`kairos.py`**: Main file to run the tool.
- **`discovery/`**: Directory containing modules for discovering endpoints.
  - **`curl_parser.py`**: Parses cURL commands.
- **`scanning/`**: Directory containing various scanning modules.
  - **`excessive_data_exposure.py`**: Checks for excessive data exposure.
  - **`injection_attack.py`**: Checks for injection attacks.
  - **`bola_scanner.py`**: Checks for Broken Object Level Authorization.
  - **`bua_scanner.py`**: Fuzzes for Broken User Authentication.
  - **`bopla.py`**: Tests for Broken Object Property Level Authorization.
  - **`unrestricted_resource_consumption.py`**: Tests for Unrestricted Resource Consumption.
  - **`bfla.py`**: Tests for Broken Function Level Authorization.
  - **`server_side_request_forgery.py`**: Tests for Server Side Request Forgery.
  - **`security_misconfiguration.py`**: Checks for security misconfigurations.
  - **`improper_asset_management.py`**: Tests for improper asset/inventory management.
  - **`remote_code_execution.py`**: Tests for improper asset/inventory management.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.

## Future Updates

Kairos is actively being developed and will be regularly updated with new features, enhancements, and security checks to ensure it remains a robust and comprehensive tool for API security testing.

## Contact

For any questions or suggestions, feel free to reach out to me on [LinkedIn](https://www.linkedin.com/in/rahdianabdi/).
