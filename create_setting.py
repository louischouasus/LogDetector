# create a template file of setting file


import json


def create_setting_file():
    setting = {}
    setting["ip"] = "192.168.124.1"
    setting["port"] = "22"
    setting["username"] = "admin"
    setting["password"] = "asus#1234"
    setting["file_path"] = "/tmp/syslog.log"

    with open("setting.json", "w") as setting_file:
        json.dump(
            setting,
            setting_file,
            indent=4,
        )


def create_pattern_file():
    pattern = {}
    # list all supported search method and parameters they needed
    pattern["usable pattern_type"] = {}
    pattern["usable pattern_type"]["keyword in time"] = {
        "#Triggering conditions": "The keyword appears more than the threshold in a time range",
        "pattern_name": "pattern name",
        "pattern_type": "keyword in time",
        "keyword": r"a regex string",
        "appeared_threshold": "appears times, in interger",
        "time_range": "second, in interger",
    }

    # add template of user defined patterns
    for i in range(2):
        pattern["pattern " + str(i)] = {
            "pattern_name": "pattern " + str(i),
            "pattern_type": "keyword in time",
            "keyword": "regex string",
            "appeared_threshold": "2",
            "time_range": "100",
            "mail": {
                "mail_to": "mail1@gmail.com;mail2@gmail.com",
                "mail_subject": "!pattern_name detected",
                "mail_content": "!pattern_name detected at !time,  !log",
            },
            "teams": {
                "teams_webhook": "",
                "teams_subject": "!pattern_name detected",
                "teams_content": "!pattern_name detected at !time,  !log",
            },
        }

    with open("pattern.json", "w") as pattern_file:
        json.dump(
            pattern,
            pattern_file,
            indent=4,
        )


if __name__ == "__main__":
    create_pattern_file()
    create_setting_file()
