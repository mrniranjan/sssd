import pytest


class TestFun(object):
    def test_abc(self, multihost):
        """ test abc """
        print("test")
        print(multihost.ad[0].domainname)
        ad_domain_name = multihost.ad[0].domainname
