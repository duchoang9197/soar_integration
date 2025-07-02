from tracecat_registry import registry, RegistrySecret, secrets

akamai_secret = RegistrySecret(
    name="akamai",
    keys=["AKAMAI_CLIENT_TOKEN", "AKAMAI_CLIENT_SECRET", "AKAMAI_ACCESS_TOKEN", "AKAMAI_HOST"]
)

@registry.register(
    default_title="Akamai API Call",
    description="Gọi API Akamai sử dụng EdgeGrid",
    display_group="Akamai",
    namespace="integrations.akamai",
    secrets=[akamai_secret],
)
def call_akamai_api(
    path: Annotated[str, Doc("Đường dẫn API (ví dụ: /identity-management/v3/user-profile)")],
    method: Annotated[str, Doc("Phương thức HTTP (GET, POST, v.v.)")],
    headers: Annotated[dict, Doc("Headers bổ sung")],
    params: Annotated[dict, Doc("Tham số truy vấn")],
    body: Annotated[dict, Doc("Dữ liệu gửi đi")],
):
    import requests
    from urllib.parse import urljoin
    from akamai.edgegrid import EdgeGridAuth

    session = requests.Session()
    session.auth = EdgeGridAuth(
        client_token=secrets.get("AKAMAI_CLIENT_TOKEN"),
        client_secret=secrets.get("AKAMAI_CLIENT_SECRET"),
        access_token=secrets.get("AKAMAI_ACCESS_TOKEN")
    )

    base_url = f"https://{secrets.get('AKAMAI_HOST')}"
    url = urljoin(base_url, path)

    response = session.request(method=method, url=url, headers=headers, params=params, json=body)
    return response.json()
