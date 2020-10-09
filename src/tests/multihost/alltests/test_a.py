import pytest 
import subprocess

class TestFun(object):
    def test_0001(self, multihost):
        """ test1 """
        try:
             multihost.client[0].run_command('abc')
        except subprocess.CalledProcessError:
            print("!!!!!!!!!!!!!!!!!!!!!!hey i am in exception!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

