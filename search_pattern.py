import regex
from datetime import datetime
from paramiko.channel import ChannelFile
import send_mail
import send_teams


def verify_pattern_dict(pattern_dict: dict):
    for pattern_name in pattern_dict:
        if pattern_name == "usable pattern_type":
            continue
        pattern = pattern_dict[pattern_name]
        if "pattern_type" not in pattern.keys():
            print("no pattern_type")
            return False


def search_pattern(stdout: ChannelFile, patterns_dict: dict):
    # init
    for pattern_name in patterns_dict:
        # add count list to every pattern
        if "count" not in patterns_dict[pattern_name] and pattern_name != "usable pattern_type":
            patterns_dict[pattern_name]["count"] = []
            patterns_dict[pattern_name]["log"] = []

    # read log lines from ssh tail
    for line in iter(stdout.readline, ""):
        print("recieve log line: " + line)
        time = parse_time_from_logline(line)

        # try to find each pattern in log line
        for pattern_name in patterns_dict:
            if pattern_name == "usable pattern_type":
                continue

            pattern = patterns_dict[pattern_name]

            if pattern["pattern_type"] == "keyword in time":
                if regex.search(pattern["keyword"], line) != None:
                    pattern["count"].append(time)
                    pattern["log"].append(line)

                    # pop loglines time interval > time range
                    while pattern["count"] and pattern["count"][-1].timestamp() > pattern["count"][0].timestamp() + int(
                        pattern["time_range"]
                    ):
                        pattern["count"].pop(0)
                        pattern["log"].pop(0)

                    if len(pattern["count"]) >= int(pattern["appeared_threshold"]):
                        trigger_notification(pattern)
                        pattern["count"] = []
                        pattern["log"] = []


def parse_time_from_logline(logline: str) -> datetime:
    try:
        tmp = datetime.strptime(logline[0:15], "%b %d %H:%M:%S").replace(year=datetime.now().year)
        return tmp
    except Exception as e:
        print(e)
        print("failed to parse time from log, use local time")
        return datetime.now()


def trigger_notification(pattern: dict):
    # send mail or teams messages when triggered
    if "mail" in pattern.keys():
        try:
            mail = pattern["mail"]
            subject = mail["mail_subject"]
            content = mail["mail_content"]
        except Exception as e:
            print(f"Failed Loading mail setting in {pattern}")

        for key in pattern:
            if isinstance(pattern[key], str):
                content = regex.sub(r"!" + key, pattern[key], content)
                subject = regex.sub(r"!" + key, pattern[key], subject)

        content = regex.sub(r"!time", str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")), content)
        subject = regex.sub(r"!time", str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")), content)

        content = regex.sub(r"!log", pattern["log"][-1], content)
        subject = regex.sub(r"!log", pattern["log"][-1], content)

        print("Send mail!")
        try:
            send_mail.send_mail(
                to_addr=mail["mail_to"],
                subject=subject,
                body=content,
            )
        except Exception as e:
            print("Failed to send mail!")
            print(e)

    if "teams" in pattern.keys():
        try:
            teams = pattern["teams"]
            webhook = teams["teams_webhook"]
            subject = teams["teams_subject"]
            content = teams["teams_content"]
        except Exception as e:
            print(f"Failed loading teams setting in {pattern}")

        for key in pattern:
            if isinstance(pattern[key], str):
                content = regex.sub(r"!" + key, pattern[key], content)
                subject = regex.sub(r"!" + key, pattern[key], subject)
        content = regex.sub(r"!time", str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")), content)
        subject = regex.sub(r"!time", str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")), subject)

        content = regex.sub(r"!log", pattern["log"][-1], content)
        subject = regex.sub(r"!log", pattern["log"][-1], subject)

        print("Send teams message!")
        try:
            send_teams.send_teams(
                webhook=webhook,
                subject=subject,
                content=content,
            )
        except Exception as e:
            print("Failed to send teams message!")
