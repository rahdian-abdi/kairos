from urllib.parse import urlparse
import requests


def improper_asset_management_test(method, url, headers, body=None):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    common_endpoints = [
    "/admin/", "/debug/", "/test/", "/old/", "/v1/", "/v2/", "/v1/test/", "/v2/test/", "/api/v1/", "/api/v2/",
    "/config/", "/configurations/", "/settings/", "/dev/", "/development/", "/staging/", "/stage/", "/qa/", "/quality_assurance/",
    "/backup/", "/backups/", "/old_version/", "/deprecated/", "/obsolete/", "/examples/", "/sample/", "/samples/", "/hidden/",
    "/internal/", "/private/", "/public/", "/secure/", "/unsecure/", "/tmp/", "/temporary/", "/temp/", "/old_api/", "/legacy/",
    "/unused/", "/testing/", "/data/", "/database/", "/db/", "/logs/", "/log/", "/files/", "/uploads/", "/download/", "/downloads/",
    "/export/", "/import/", "/admin_panel/", "/management/", "/manager/", "/superadmin/", "/superuser/", "/root/", "/master/",
    "/system/", "/support/", "/help/", "/info/", "/information/", "/assets/", "/resources/", "/docs/", "/documentation/", "/scripts/",
    "/script/", "/cgi-bin/", "/server-status/", "/status/", "/monitor/", "/monitoring/", "/error/", "/errors/", "/auth/", "/authentication/",
    "/login/", "/logout/", "/signin/", "/signup/", "/register/", "/user/", "/users/", "/account/", "/accounts/", "/profile/", "/profiles/",
    "/session/", "/sessions/", "/token/", "/tokens/", "/access/", "/permissions/", "/privileges/", "/roles/", "/role/", "/group/", "/groups/",
    "/membership/", "/memberships/", "/subscription/", "/subscriptions/", "/api/v3/", "/api/v4/", "/api/v5/", "/v3/", "/v4/", "/v5/",
    "/secure_api/", "/public_api/", "/private_api/", "/services/", "/service/", "/endpoint/", "/endpoints/"
    ]

    method = 'GET' if method == 'POST' or method == 'PUT' else method

    discovered_endpoints = []
    for endpoint in common_endpoints:
        url = base_url + endpoint
        response = requests.request(method, url, headers=headers)
        if response.status_code != 404:
            discovered_endpoints.append(endpoint)
    
    if discovered_endpoints:
        for _, discover in enumerate(discovered_endpoints):
            print("\033[91m[v] Deprecated Endpoints Found:\033[0m", discover)
    else:
         print("\033[92m[!] No improper asset management issues found.\033[0m")