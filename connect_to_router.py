import paramiko


def connect_to_router(ip: str, port: int, username: str, password: str, **kwargs):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=port, username=username, password=password)
    return ssh


def disconnect_from_router(ssh: paramiko.SSHClient):
    ssh.close()
    return


def cat_syslog(ssh: paramiko.SSHClient, syslog_path: str):
    stdin, stdout, stderr = ssh.exec_command(f"cat {syslog_path}")
    lines = stdout.readlines()
    return lines


def tail_syslog(ssh: paramiko.SSHClient, syslog_path: str):
    stdin, stdout, stderr = ssh.exec_command(f"tail -f {syslog_path}", timeout=10)
    return stdin, stdout, stderr
