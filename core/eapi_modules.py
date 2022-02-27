def create_eapi_conf_file(device, username, password):
    with open("core/eapi.conf", "w") as file:
        device_config_string = (f"""[connection:{device}]
host: {device}
transport: https
username: {username}
password: {password}
""")
        file.write(device_config_string)