import pymsteams


def send_teams(webhook, subject, content):
    try:
        myTeamsMessage = pymsteams.connectorcard(webhook)
    except Exception as e:
        print("Failed to connect to Teams: ", e)
        return

    myTeamsMessage.text(content)
    myTeamsMessage.title(subject)

    myTeamsMessage.send()
