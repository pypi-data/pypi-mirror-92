import logging

import paramiko
from enhancements.modules import Module


class BaseServerInterface(paramiko.ServerInterface, Module):

    def __init__(self, session):
        super().__init__()
        self.session = session


class ServerInterface(BaseServerInterface):

    @classmethod
    def parser_arguments(cls):
        cls.PARSER.add_argument(
            '--disable-ssh',
            dest='disable_ssh',
            action='store_true',
            help='disable ssh'
        )
        cls.PARSER.add_argument(
            '--disable-scp',
            dest='disable_scp',
            action='store_true',
            help='disable scp'
        )
        cls.PARSER.add_argument(
            '--disable-password-auth',
            dest='disable_password_auth',
            action='store_true',
            help='disable password authentication'
        )

        cls.PARSER.add_argument(
            '--disable-pubkey-auth',
            dest='disable_pubkey_auth',
            action='store_true',
            help='disable public key authentication'
        )

    def check_channel_exec_request(self, channel, command):
        if command.decode('utf8').startswith('scp') and (command.find(b' -t ') != -1 or command.find(b' -f ') != -1):
            if not self.args.disable_scp:
                self.session.scp = True
                self.session.scp_command = command
                self.session.scp_channel = channel
                return True

            channel.send_stderr('scp command not allowed!\r\n')
            logging.warning('scp command not allowed!')
            return False

        if not self.args.disable_ssh:
            self.session.sshCommand = command
            return True

        channel.send_stderr('Nicht erlaubt!\r\n')
        logging.warning('Nicht erlaubtes SSH Kommando!')
        return False

    def check_channel_forward_agent_request(self, channel):
        self.session.agent_requested = True
        logging.info("Requested Agent forwarding")
        return True

    def check_channel_shell_request(self, channel):
        if not self.args.disable_ssh:
            self.session.ssh = True
            self.session.ssh_channel = channel
            return True
        return False

    def check_channel_pty_request(self, channel, term, width, height,
                                  pixelwidth, pixelheight, modes):
        if not self.args.disable_ssh:
            self.session.ssh = True
            self.session.sshPtyKArgs = {
                'term': term,
                'width': width,
                'height': height,
                'width_pixels': pixelwidth,
                'height_pixels': pixelheight
            }
            return True
        return False

    def get_allowed_auths(self, username):
        allowed_auths = []
        if not self.args.disable_pubkey_auth:
            allowed_auths.append('publickey')
        if not self.args.disable_password_auth:
            allowed_auths.append('password')
        if allowed_auths:
            logging.info("Authentication types are: %s", ','.join(allowed_auths))
            return ','.join(allowed_auths)
        logging.warning('Allowed authentication is none!')
        return 'none'

    def check_auth_publickey(self, username, key):
        logging.info("try pubkey authentication")
        if self.args.disable_pubkey_auth:
            logging.warning("Public key login attempt, but public key auth was disabled!")
            return paramiko.AUTH_FAILED
        return self.session.authenticator.authenticate(username, key=key)

    def check_auth_password(self, username, password):
        logging.info("try password authentication")

        if self.args.disable_password_auth:
            logging.warning("Password login attempt, but password auth was disabled!")
            return paramiko.AUTH_FAILED
        return self.session.authenticator.authenticate(username, password=password)

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED

    def check_channel_subsystem_request(self, channel, name):
        if name.upper() == 'SFTP':
            self.session.sftp = True
            self.session.sftp_channel = channel
        return super().check_channel_subsystem_request(channel, name)

    def check_port_forward_request(self, address, port):
        logging.info("port forward attempt - address: %s, port: %s", address, port)
        return True

    def cancel_port_forward_request(self, address, port):
        logging.info("port forward cancel - address: %s, port: %s", address, port)


class ProxySFTPServer(paramiko.SFTPServer):
    def start_subsystem(self, name, transport, channel):
        self.server.session.sftp_client_ready.wait()
        self.server.session.sftp_client.subsystem_count += 1
        super().start_subsystem(name, transport, channel)

    def finish_subsystem(self):
        super().finish_subsystem()
        self.server.session.sftp_client.subsystem_count -= 1
        self.server.session.sftp_client.close()
