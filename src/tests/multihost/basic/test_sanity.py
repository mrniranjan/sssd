""" Sanity Test cases """


class Testsanitysssd(object):
    """ Sanity Test cases """

    def test_check_sssd_running(self, multihost):
        """ Verify sssd process is running """
        sssd_proc = ['sssd', 'sssd_be', 'sssd_nss', 'sssd_pam']
        for proc in sssd_proc:
            ps_cmd = 'pidof %s' % proc
            cmd = multihost.master[0].run_command(ps_cmd)
            assert cmd.returncode == 0
