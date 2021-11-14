from src.main import ConferenceCorpusIntro
from tests.basetest import BaseTest


class TestConfereceCorpusIntro(BaseTest):
    """
    tests ConferenceCorpusIntro
    """

    def setUp(self, **kwargs):
        super().setUp(**kwargs)
        self.cc = ConferenceCorpusIntro()

    def tearDown(self):
        super().tearDown()

    def test_loadingOfDatasources(self):
        """
        tests if the datasource are loaded correctly
        """
        datasourceIds = self.cc.printAvailableDatasourceIds()
        for id in datasourceIds:
            events = self.cc.corpus.getDataSource(id).eventManager.getList()
            series = self.cc.corpus.getDataSource(id).eventSeriesManager.getList()
            print(f"{id} has {len(events)} events and {len(series)} series")
            self.assertTrue(len(events) > 1000, f"{id} has too few events")
            self.assertTrue(len(series) > 0, f"{id} has too few series")
