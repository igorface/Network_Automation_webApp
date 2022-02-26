"""examples.basic_usage.iosxe_driver"""
from scrapli.driver.core import IOSXEDriver
from concurrent.futures import ThreadPoolExecutor
from ntc_templates.parse import parse_output

MY_DEVICE = {
    "host": "10.0.0.1",
    "auth_username": "admin",
    "auth_password": "arista",
    "auth_strict_key": False,
}

def get_show_vlans(ip_address):
    MY_DEVICE = {
        "host": f"{ip_address}",
        "auth_username": "admin",
        "auth_password": "arista",
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
            futures = executor.submit(config_vlans, hostname)
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


if __name__ == "__main__":
    hostnames = (
        "10.0.0.1",
        "10.0.0.2",
        "10.0.0.101",
        "10.0.0.102",
    )

    results = get_show_vlans_all(hostnames)
    for result in results:
        print(result)