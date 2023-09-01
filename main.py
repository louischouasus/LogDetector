import json
import connect_to_router
import create_setting
import search_pattern
import os
import time
import paramiko


def load_ssh_setting(file_path: str):
    try:
        with open(file_path, "r") as file:
            ssh_setting = json.load(file)
    except Exception as e:
        print(e)
        print("Something wrong while loading setting file")
        raise e
    return ssh_setting


def load_detect_pattern(file_path: str):
    try:
        with open(file_path, "r") as file:
            ssh_setting = json.load(file)
    except Exception as e:
        print(e)
        print("Something wrong while loading pattern file")
        raise e
    return ssh_setting


if __name__ == "__main__":
    setting_file_path = "setting.json"
    pattern_file_path = "pattern.json"

    if not os.path.exists(setting_file_path):
        print("Can't find setting file, creat a setting template.")
        create_setting.create_setting_file()

    if not os.path.exists(pattern_file_path):
        create_setting.create_pattern_file()
        print("Can't find pattern file, creat a pattern template.")

    ssh_setting = load_ssh_setting(setting_file_path)
    patterns_dict = load_detect_pattern(pattern_file_path)
    while True:
        sleep_length = 10

        ssh_client = connect_to_router.connect_to_router("192.168.124.1", 22, "admin", "asus#1234")
        stdin, stdout, stderr = connect_to_router.tail_syslog(ssh_client, ssh_setting["file_path"])
        while ssh_client.invoke_shell().active:
            try:
                search_pattern.search_pattern(ssh_client, stdout, patterns_dict)
            except Exception as e:
                pass
        print(f"reconnecting... {sleep_length}")
        time.sleep(sleep_length)
        sleep_length *= 2
