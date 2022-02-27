def create_eapi_conf_file(device, username, password):
    with open("eapi.conf", "w") as file:
        file.append(f"""
        [connection:veos01]
        host: {device}
        transport: https
        username: {username}
        password: {password}
        """)