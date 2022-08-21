"""examples.async_usage.async_multiple_connections"""
import asyncio

from scrapli.driver.core import AsyncIOSXEDriver, AsyncNXOSDriver

dist_rtr01 = {
    "host": "10.10.20.175",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "transport": "asyncssh",
    "driver": AsyncIOSXEDriver,
}

dist_rtr02 = {
    "host": "10.10.20.176",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "transport": "asyncssh",
    "driver": AsyncIOSXEDriver,
}

dist_sw01 = {
    "host": "10.10.20.177",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "transport": "asyncssh",
    "driver": AsyncNXOSDriver,
}

dist_sw02 = {
    "host": "10.10.20.178",
    "auth_username": "cisco",
    "auth_password": "cisco",
    "auth_strict_key": False,
    "transport": "asyncssh",
    "driver": AsyncNXOSDriver,
}

DEVICES = [dist_rtr01, dist_rtr02, dist_sw01, dist_sw02]


async def gather_version(device):
    """Simple function to open a connection and get some data"""
    driver = device.pop("driver")
    conn = driver(**device)
    await conn.open()
    prompt_result = await conn.get_prompt()
    version_result = await conn.send_command("show version")
    await conn.close()
    return prompt_result, version_result


async def main():
    """Function to gather coroutines, await them and print results"""
    coroutines = [gather_version(device) for device in DEVICES]
    results = await asyncio.gather(*coroutines)
    for result in results:
        print(f"device prompt: {result[0]}")
        print(f"device show version: {result[1].result}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())