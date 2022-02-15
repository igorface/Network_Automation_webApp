import asyncio
import pprint as pp
from ntc_templates.parse import parse_output
from scrapli.driver.core import AsyncEOSDriver

coroutines_list = []

async def gather_version(ip_address):
    device = {
    "host": f"{ip_address}",
    "auth_username": "admin",
    "auth_password": "arista",
    "auth_strict_key": False,
    "transport": "asyncssh",
    "driver": AsyncEOSDriver,
    }
    """Simple function to open a connection and get some data"""
    driver = device.pop("driver")
    conn = driver(**device)
    await conn.open()
    prompt_result = await conn.get_prompt()
    version_result = await conn.send_command("show vlan")
    await conn.close()
    return prompt_result, version_result

async def gather_vlans(ip_address):
    device = {
    "host": f"{ip_address}",
    "auth_username": "admin",
    "auth_password": "arista",
    "auth_strict_key": False,
    "transport": "asyncssh",
    "driver": AsyncEOSDriver,
    }
    """Simple function to open a connection and get some data"""
    driver = device.pop("driver")
    conn = driver(**device)
    await conn.open()
    version_result = await conn.send_command("show vlan")
    await conn.close()
    return version_result

def create_coroutines_list(hostname, function) -> list():
    coroutines_list.append(function({f'hostname'}))
    return coroutines_list

async def main():
    """Function to gather coroutines, await them and print results"""
    # coroutines = [gather_version(device) for device in DEVICES]
    coroutines = create_coroutines_list('10.0.0.1', gather_vlans)
    results = await asyncio.gather(*coroutines)
    for result in results:
        print(f"device prompt: {result[0]}")
        print(f"device show version: {result[1].result}")
        output = result[1].result
        output_parsed = parse_output(platform="arista_eos", command="show vlan", data=output)
        print(output_parsed)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())