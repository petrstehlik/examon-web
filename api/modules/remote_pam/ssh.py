import paramiko
from muapi.configurator import Config


class Tunnel:
    def __init__(self):
        self.config = Config()

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __enter__(self):
        self.ssh.connect(self.config['ssh']['server'], username=self.config['ssh']['user'])
        return self.ssh

    def __exit__(self, type, value, traceback):
        self.ssh.close()


class RemotePAM:
    def __init__(self):
        self.ssh = Tunnel()

    def get_uid(self, username):
        uid = None

        with self.ssh as s:
            _, stdout, stderr = s.exec_command("python -c 'import pwd; print(pwd.getpwnam(\"{}\").pw_uid);'"
                                                 .format(username))

            try:
                uid = int(stdout.readline())
            except ValueError:
                pass

        return uid

    def authenticate(self, username, password):
        with self.ssh as s:
            _, stdout, _ = s.exec_command(
                "venv/bin/python -c 'from pam import pam; p = pam(); print(p.authenticate(\"{}\", \"{}\"))'"
                .format(username, password)
            )

            return 'True\n' == stdout.read()
