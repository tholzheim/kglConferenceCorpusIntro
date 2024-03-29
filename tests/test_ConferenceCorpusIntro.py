from kglConferenceCorpusIntro.main import ConferenceCorpusIntro
from tests.basetest import BaseTest


class TestConferenceCorpusIntro(BaseTest):
    """
    tests ConferenceCorpusIntro
    """

    def setUp(self, **kwargs):
        super().setUp(**kwargs)
        self.cc = ConferenceCorpusIntro(force_update=False)

    def tearDown(self):
        super().tearDown()

    def test_loading_of_data_sources(self):
        """
        tests if the datasource are loaded correctly
        """
        datasourceIds = self.cc.get_available_datasource_ids()
        for id in datasourceIds:
            events = self.cc.corpus.getDataSource(id).eventManager.getList()
            series = self.cc.corpus.getDataSource(id).eventSeriesManager.getList()
            print(f"{id} has {len(events)} events and {len(series)} series")
            self.assertTrue(len(events) > 1000, f"{id} has too few events")
            self.assertTrue(len(series) > 0, f"{id} has too few series")
