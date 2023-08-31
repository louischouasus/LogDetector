import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mail_addr = "logdetector.asus@gmail.com"
mail_password = "owdactfyqvnlkhmv"


def send_mail(to_addr: str, subject: str, body: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = mail_addr
    msg["To"] = to_addr
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(mail_addr, mail_password)
            smtp.sendmail(from_addr=mail_addr, to_addrs=to_addr, msg=msg.as_string())
            smtp.quit()
        except Exception as e:
            print("Something wrong while sending mail: ", e)
