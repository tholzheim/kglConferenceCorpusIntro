import sys
from os.path import expanduser
from logging import Logger, DEBUG, StreamHandler

from corpus.event import EventStorage
from corpus.lookup import CorpusLookup, CorpusLookupConfigure
from corpus.utils.download import Download
from tabulate import tabulate
from lodstorage.sql import SQLDB


class ConferenceCorpusIntro:
    """
    Provides access to the ConferenceCorpus.
    Showcases the functions and data available in the ConferenceCorpus
    """

    def __init__(self, force_update: bool = False, debug: bool = True):
        self.logger = Logger(name=self.__class__.__name__)
        if debug:
            self.logger.setLevel(DEBUG)
            self.logger.addHandler(StreamHandler(sys.stdout))
        # If you want the complete dblp datasource set onlySample to False
        # Note: This might be not necessary in a newer version of ConferenceCorpus but currently there is a bug
        #       and the dblp dump must be provided beforehand
        # Once downloaded set forceUpdate to "False", to not download the dump everytime
        RawDataSources.downloadDblp(only_sample=True, force_update=force_update)
        # by not providing lookup ids we load all data sources
        self.corpus = CorpusLookup(configure=CorpusLookupConfigure.configureCorpusLookup, lookupIds=None)
        # now we need to load the data sources
        # with forceUpdate=True the cache is reinitialized by querying the datasources or dumps of the datasources
        # is done automatically if cache is not available
        self.logger.debug("Loading the data sources (this might take some time)")
        self.corpus.load(forceUpdate=force_update)  # if the data sources are not cached this takes some time
        # the data sources are now loaded and each datasource contains an EventManager and EventSeriesManager (there
        # are datasource were only of both is filled with entities)

    def get_events_of_data_source(self, source_id: str, limit: int = 10):
        """
        Prints the events of the given source to the console

        Args:
            source_id(str): id of the DataSource
            limit(int): limits the amount of printed events id None print all
        """
        datasource = self.corpus.getDataSource(source_id)
        events = datasource.eventManager.getList()
        # to print the events with tabulate we need to convert the event objects to dicts
        lod = [vars(entity) for entity in events]
        if limit:
            lod = lod[:limit]
        self.logger.debug(f"Events of {datasource}")
        self.logger.debug(tabulate(lod, headers="keys"))
        return events

    def get_events_of_series(self, source_id: str, series_acronym: str, limit: int = 10):
        """
        Get the events of the given series (by acronym) that are known by the given source.

        Args:
            source_id(str): id of the DataSource
            series_acronym(str): acronym identifying the series
            limit(int): limits the amount of printed events id None print all
        """
        datasource = self.corpus.getDataSource(source_id)
        # During the loading of the datasource the event series and the events are linked together if possible
        # (see EventManager.linkSeriesAndEvent())
        # result of this interlinking is a lookup table
        if series_acronym in datasource.eventManager.seriesLookup:
            events = datasource.eventManager.seriesLookup[series_acronym]
            lod = [vars(entity) for entity in events]
            if limit:
                lod = lod[:limit]
            self.logger.debug(f"Events of {series_acronym} in {source_id}")
            self.logger.debug(tabulate(lod, headers="keys"))
            return events
        else:
            self.logger.debug(f"The datasource {source_id} does not have any events linked to the series {series_acronym}")
            return None

    def query_corpus_db(self, sql_query: str = None):
        """
        Prints the result of a direct query to the database
        """
        if sql_query is None:
            sql_query = "SELECT * FROM event LIMIT 5"
        # we can also query the database directly e.g. to write complex queries / merge tables / access views
        db_file = self.gat_cache_file()
        sql_db = SQLDB(dbname=db_file)
        # now we can directly query the EventCorpus.db abd get LoDs (List of Dicts) as result
        # Try it by writing your own query
        res = sql_db.query(sql_query)
        self.logger.debug(tabulate(res, headers="keys"))
        return res

    def get_datasource_stats(self):
        """
        prints statistics about the different data sources
        """
        datasource_ids = self.corpus.lookupIds
        stats = []
        for datasource_id in datasource_ids:
            events = self.corpus.getDataSource(datasource_id).eventManager.getList()
            series = self.corpus.getDataSource(datasource_id).eventSeriesManager.getList()
            stats.append({
                "datasource": datasource_id,
                "#events": len(events),
                "#series": len(series)
            })
        self.logger.debug("\nDatasource statistics:")
        self.logger.debug(tabulate(stats, headers="keys"))
        return stats

    def get_available_datasource_ids(self):
        """
        Get the IDs of the available data sources

        Returns:
            list of datasource ids
        """
        ids = self.corpus.lookupIds
        self.logger.debug("Available datasource ids: ", ids)
        return ids

    def gat_cache_file(self):
        """
        Get the location of the ConferenceCorpus cache file (sqlite database)

        Returns:
            str absolut path to cache file
        """
        path = EventStorage.getStorageConfig().getCachePath() + "/EventCorpus.db"
        self.logger.debug(f"ConferenceCorpus cache is stored at {path}")
        return path


class RawDataSources:
    """
    Manages the download of raw data sources that are needed to init the ConferenceCorpus
    """

    @classmethod
    def downloadDblp(cls, only_sample: bool = True, force_update: bool = False):
        """
        download the dblp xml dump

        Args:
             only_sample(bool): If False the complete xml dump is downloaded (~4GB). Otherwise, only a sample is downloaded.
             force_update(bool): If True the file will be downloaded even if already existent
        """
        sample_url = "https://github.com/WolfgangFahl/ConferenceCorpus/wiki/data/dblpsample.xml.gz"
        dump_url = "https://dblp.uni-trier.de/xml/dblp.xml.gz"
        if only_sample:
            url = sample_url
        else:
            url = dump_url
        home = expanduser("~")
        Download.downloadBackupFile(
                url=url,
                fileName="dblp.xml",
                targetDirectory=f"{home}/.dblp",
                force=force_update,
                profile=True)


if __name__ == '__main__':
    cc = ConferenceCorpusIntro()
    cc.gat_cache_file()
    cc.get_available_datasource_ids()
    cc.get_events_of_data_source(source_id="wikidata")
    cc.get_events_of_series(source_id="or", series_acronym="AAAI", limit=5)
    cc.query_corpus_db()
    cc.get_datasource_stats()
