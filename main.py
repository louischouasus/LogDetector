import json
import connect_to_router
import send_mail
import create_setting
import search_pattern
import os
import time


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

    sleep_length = 10

    while True:
        ssh_client = connect_to_router.connect_to_router(**ssh_setting)
        stdin, stdout, stderr = connect_to_router.tail_syslog(ssh_client, ssh_setting["file_path"])
        search_pattern.search_pattern(stdout, patterns_dict)

        print(f"reconnecting... {sleep_length}")
        time.sleep(sleep_length)
        sleep_length *= 2
