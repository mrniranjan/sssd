""" pexpect methods """

import sys
import pexpect
from pexpect import pxssh
#from .exceptions import SSHLoginException
#from .exceptions import Exception


class pexpect_ssh(object):
    """ pexpect methods """
    def __init__(self, hostname, username,
                 password, port=None,
                 encoding='utf-8', debug=False):
        """ Initilized defaults """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.encoding = encoding
        if port is None:
            self.port = 22
        else:
            self.port = port
        self.ssh_options = {'StrictHostKeyChecking': 'no',
                            'UserKnownHostsFile': '/dev/null'}
        self.ssh = pxssh.pxssh(options=self.ssh_options)
        if debug:
            self.ssh.logfile = sys.stdout.buffer

    def login(self):
        """ login to host """
        self.PROMPT = r"\[PEXPECT\][\$\#] "
        options = '%s, %s, %s, %s ' % (self.hostname, self.username,
                                       self.password, 
                                       'port=%s' % (self.port))

        #for arg in kwargs:
        #    options += ', ' + arg
        print(options)
        try:
            #self.ssh.login(options)
            self.ssh.login(self.hostname, self.username, self.password, port=self.port, login_timeout=5, sync_multiplier=5, auto_prompt_reset=False)
        except pexpect.pxssh.ExceptionPxssh:
            raise Exception("%s Failed to login" % self.username)

    def command(self, command, raiseonerr=False):
        """ Run Non interactive Commands """
        self.ssh.sendline(command)
        self.ssh.prompt()
        output_utf8 = self.ssh.before
        self.ssh.sendline("echo $?")
        self.ssh.prompt()
        returncode = self.ssh.before
        ret = returncode.decode('utf-8').split('\r')[1].strip('\n')
        output_str = output_utf8.decode('utf-8')
        if raiseonerr:
            if (int(ret)) != 0:
                raise Exception('Command failed with err: %s' % (output_str))
        return (output_str, ret)

    def expect_command(self, command, password, raiseonerr=False):
        """ Run interactive command prompting for password * """
        self.ssh.sendline(command)
        self.ssh.expect('Password.*.')
        self.ssh.sendline(password)
        cmd = self.ssh.expect(['Password incorrect .*.', r'[#\$] '])
        if cmd == 0:
            print("Password Incorrect")
        elif cmd == 1:
            print("Correct Password")
        output_utf8 = self.ssh.before
        self.ssh.sync_original_prompt()
        self.ssh.set_unique_prompt()
        self.ssh.sendline("echo $?")
        self.ssh.prompt()
        returncode = self.ssh.before.decode('utf-8')
        output_str = output_utf8.decode('utf-8')
        if raiseonerr:
            if (int(returncode)) != 0:
                raise Exception('Command failed with err: %s' % (output_str))
        return(output_str, returncode)

    def logout(self):
        """ Logout of ssh session """
        self.ssh.logout()


def main():
    client_hostname = 'ibm-x3650m4-01-vm-16.ibm2.lab.eng.bos.redhat.com'
    user = 'user5000'
    client = pexpect_ssh(client_hostname, user, 'Secret123', debug=True)
    try:
        #client.login('login_timeout=20', 'sync_multiplier=5', 'auto_prompt_reset=True')
        client.login()
    except Exception:
        raise
        print("failed")
    else:
        print("success")
    
if __name__ == '__main__':
    main()

