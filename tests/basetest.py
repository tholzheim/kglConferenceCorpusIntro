'''
Created on 15.11.2021
@author: tholzheim
'''
import unittest
import time

from corpus.eventcorpus import EventCorpus


class Profiler:
    '''
    simple profiler
    '''

    def __init__(self, msg, profile=True):
        '''
        construct me with the given msg and profile active flag

        Args:
            msg(str): the message to show if profiling is active
            profile(bool): True if messages should be shown
        '''
        self.msg = msg
        self.profile = profile
        self.starttime = time.time()
        if profile:
            print(f"Starting {msg} ...")

    def time(self, extraMsg=""):
        '''
        time the action and print if profile is active
        '''
        elapsed = time.time() - self.starttime
        if self.profile:
            print(f"{self.msg}{extraMsg} took {elapsed:5.1f} s")

class BaseTest(unittest.TestCase):
    '''
    Base test class for all OpenResearh migration project test cases
    '''


    def setUp(self,debug:bool=False,profile:bool=True):
        self.debug=debug
        self.profile=profile
        msg=f"test {self._testMethodName}, debug={self.debug}"
        self.profiler=Profiler(msg,profile=profile)
        EventCorpus.download()


    def tearDown(self):
        self.profiler.time()
        pass




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()