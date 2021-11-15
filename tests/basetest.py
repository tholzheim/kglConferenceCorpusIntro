'''
Created on 15.11.2021
@author: tholzheim
'''
import os
import unittest
import time

from corpus.eventcorpus import EventCorpus
from wikibot.wikiuser import WikiUser


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
        SmwHelper.createMissingWikiUsers()
        self.debug=debug
        self.profile=profile
        msg=f"test {self._testMethodName}, debug={self.debug}"
        self.profiler=Profiler(msg,profile=profile)
        EventCorpus.download()


    def tearDown(self):
        self.profiler.time()
        pass


class SmwHelper:
    """
    Provides functions to generate missing wikiuser entries
    """

    @classmethod
    def createMissingWikiUsers(cls):
        neededWikiIds = ["or", "orclone"]
        for wikiId in neededWikiIds:
            cls.getSMW_WikiUser(wikiId=wikiId, save=True)


    @classmethod
    def getSMW_WikiUser(cls, wikiId="or", save=False):
        '''
        get semantic media wiki users for SemanticMediawiki.org and openresearch.org
        '''
        iniFile = WikiUser.iniFilePath(wikiId)
        wikiUser = None
        if not os.path.isfile(iniFile):
            wikiDict = None
            if wikiId == "or":
                wikiDict = {"wikiId": wikiId, "email": "noreply@nouser.com", "url": "https://www.openresearch.org",
                            "scriptPath": "/mediawiki/", "version": "MediaWiki 1.31.1"}
            if wikiId == "orclone":
                wikiDict = {"wikiId": wikiId, "email": "noreply@nouser.com",
                            "url": "https://confident.dbis.rwth-aachen.de", "scriptPath": "/or/",
                            "version": "MediaWiki 1.35.1"}
            if wikiId == "cr":
                wikiDict = {"wikiId": wikiId, "email": "noreply@nouser.com", "url": "https://cr.bitplan.com",
                            "scriptPath": "/", "version": "MediaWiki 1.33.4"}

            if wikiDict is None:
                raise Exception("wikiId %s is not known" % wikiId)
            else:
                wikiUser = WikiUser.ofDict(wikiDict, lenient=True)
                if save:
                    wikiUser.save()
        else:
            wikiUser = WikiUser.ofWikiId(wikiId, lenient=True)
        return wikiUser





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()