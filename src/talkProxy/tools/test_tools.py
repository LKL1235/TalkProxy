import unittest
import logging
class Test(unittest.TestCase):
    
    def test_config(self):
        from talkProxy.tools.config import test
        res = test()