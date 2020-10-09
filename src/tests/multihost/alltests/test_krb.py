""" Automation of Krb5 tests """
from __future__ import print_function
import pytest
import os
import time
import paramiko
import subprocess
from sssd.testlib.common.utils import sssdTools, LdapOperations
from sssd.testlib.common.expect import pexpect_ssh
from sssd.testlib.common.exceptions import SSHLoginException
from constants import ds_instance_name, ds_suffix
from sssd.testlib.common.utils import SSHClient


#@pytest.mark.usefixtures('setup_sssd_krb')
@pytest.mark.krb5
class TestKrbWithLogin(object):
    def test_0001_krb5_not_working_based_on_k5login(self, multihost):
        """
        :Title: krb5: access_provider = krb5 is not
        working in RHEL8 while restricting logins
        based on .k5login file

        @bugzilla:
        https://bugzilla.redhat.com/show_bug.cgi?id=1734094
        """
        #multihost.client[0].service_sssd('stop')
        client_tool = sssdTools(multihost.client[0])
        domain_params = {'id_provider': 'files',
                         'access_provider': 'krb5',
                         'krb5_realm': 'EXAMPLE1.TEST'}
        #client_tool.sssd_conf('domain/example1', domain_params)
        dmain_delete = {"ldap_user_home_directory": "/home/%u",
                        "ldap_uri": multihost.master[0].sys_hostname,
                        "ldap_search_base": "dc=example,dc=test",
                        "ldap_tls_cacert": "/etc/openldap/cacerts/cacert.pem",
                        "use_fully_qualified_names": "True"}
        #client_tool.sssd_conf('domain/example1', dmain_delete, action='delete')
        #multihost.client[0].service_sssd('start')
        user = 'user5000'
        client_hostname = multihost.client[0].sys_hostname
        #multihost.client[0].run_command("touch /home/user5000/.k5login")
        #multihost.client[0].run_command(f'chown {user}:{user} /home/user5000/.k5login')
        #multihost.client[0].run_command("chmod 664 /home/user5000/.k5login")
        #multihost.client[0].service_sssd('restart')
        #client = pexpect_ssh(client_hostname, user, 'Secret123', debug=False)
        #with pytest.raises(Exception):
        #    client.login()
        #del client
        #multihost.client[0].run_command("rm -vf /home/user5000/.k5login")
        #multihost.client[0].service_sssd('restart')
        client = pexpect_ssh(client_hostname, user, 'Secret123', debug=False)
        try:
            client.login(login_timeout=30, sync_multiplier=5, auto_prompt_reset=False)
        except SSHLoginException:
            #print("!!!! Debug !!!!")
            #time.sleep(50000)
            pytest.fail("%s failed to login" % user)
        else:
            client.logout()
