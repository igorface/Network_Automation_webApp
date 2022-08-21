"""examples.basic_usage.iosxe_driver"""
from scrapli.driver.core import NXOSDriver
from pprint import pprint

MY_DEVICE = {
    "host": "10.10.20.177",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
}


def main():
    """Simple example of connecting to an NXOSevice with the NXOSDriver"""
    with NXOSDriver(**MY_DEVICE) as conn:
        # Platform drivers will auto-magically handle disabling paging for you
        response = conn.send_command("show vlan")
        structured_result = response.textfsm_parse_output()
        pprint(structured_result)

    # print(result.result)


if __name__ == "__main__":
    main()