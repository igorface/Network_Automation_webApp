from scrapli.driver.core import IOSXEDriver
from concurrent.futures import ThreadPoolExecutor
from ntc_templates.parse import parse_output
from core.credentials import get_password, get_username

username = get_username()
password = get_password()


def get_show_vlans(ip_address):
    MY_DEVICE = {
        "host": f"{ip_address}",
        "auth_username": f"{username}",
        "auth_password": f"{password}",
        "auth_strict_key": False,
    }
    with IOSXEDriver(**MY_DEVICE) as conn:
        # Platform drivers will auto-magically handle disabling paging for you
        result = conn.send_command("show vlan")
        output = result.result
        output_parsed = parse_output(platform="arista_eos", command="show vlan", data=output)
    return output_parsed

def get_show_vlans_all(hostnames):
    futures_list = []
    results = []

    with ThreadPoolExecutor(max_workers=17) as executor:
        for hostname in hostnames:
            futures = executor.submit(get_show_vlans, hostname)
            futures_list.append(futures)

        for future in futures_list:
            try:
                result = future.result(timeout=60)
                results.append(result)
            except Exception:
                results.append(None)
    return results

def configure_vlans(hostnames):
    futures_list = []
    results = []

    with ThreadPoolExecutor(max_workers=17) as executor:
        for hostname in hostnames:
            futures = executor.submit(get_show_vlans, hostname)
            futures_list.append(futures)

        for future in futures_list:
            try:
                result = future.result(timeout=60)
                results.append(result)
            except Exception:
                results.append(None)
    return results

def create_eapi_conf_file(device, username, password):
    with open("eapi.conf", "w") as file:
        file.append(f"""
        [connection:veos01]
        host: {device}
        transport: https
        username: {username}
        password: {password}
        """)


if __name__ == "__main__":
    hostnames = (
        "10.0.0.1",
        "10.0.0.2",
        "10.0.0.101",
        "10.0.0.102",
    )

    for hostname in hostnames:
        create_eapi_conf_file(hostname, "admin", "arista")