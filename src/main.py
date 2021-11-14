from corpus.event import EventStorage
from corpus.lookup import CorpusLookup, CorpusLookupConfigure
from tabulate import tabulate
from lodstorage.sql import SQLDB


class ConferenceCorpusIntro:
    """
    Provides access to the ConferenceCorpus.
    Show cases the functions and data available in the ConferenceCorpus
    """

    def __init__(self):
        self.corpus = CorpusLookup(configure=CorpusLookupConfigure.configureCorpusLookup)  # by not providing lookupids we load all datasources
        # now we need to load the datasources
        # with forceUpdate=True the cache is reinitialized by querying the datasources again (takes some time)
        # is done automatically if cache is not available
        print("Loading the datasources (this might take some time)")
        self.corpus.load()  # if the datasources are not cached this takes some time


    def printEventsOfDatasource(self, sourceId:str, limit:int=10):
        """
        Prints the events of the given source to the console

        Args:
            sourceId(str): id of the DataSource
            limit(int): limits the amount of printed events id None print all
        """
        datasource = self.corpus.getDataSource(sourceId)
        events = datasource.eventManager.getList()
        # to print the events with tabulate we need to convert the event objects to dicts
        lod = [vars(entity) for entity in events]
        if limit:
            lod = lod[:limit]
        print(f"Events of {datasource}")
        print(tabulate(lod, headers="keys"))
        return events

    def printEventsOfSeries(self, sourceId:str, seriesAcronym:str, limit:int=10):
        """
        Prints the events of the given series (by acronym) that are known by the given source.

        Args:
            sourceId(str): id of the DataSource
            seriesAcronym(str): acronym identifying the series
            limit(int): limits the amount of printed events id None print all
        """
        datasource = self.corpus.getDataSource(sourceId)
        # During the loading of the datasource the event series and the events are linked together if possible (see EventManager.linkSeriesAndEvent())
        # result of this interlinking is a lookup table
        if seriesAcronym in datasource.eventManager.seriesLookup:
            events = datasource.eventManager.seriesLookup[seriesAcronym]
            lod = [vars(entity) for entity in events]
            if limit:
                lod = lod[:limit]
            print(f"Events of {seriesAcronym} in {sourceId}")
            print(tabulate(lod, headers="keys"))
            return events
        else:
            print(f"The datasource {sourceId} does not have any events linked to the series {seriesAcronym}")
            return None

    def printSqlQueryResult(self):
        """
        Prints the result of an direct query to the database
        """
        # we can also query the database directly e.g. to write complex queries / merge tables / access views
        dbFile = self.printCacheFile()
        sqlDb = SQLDB(dbname=dbFile)
        # now we can directly query the EventCorpus.db abd get LoDs (List of Dicts) as result
        # Try it by writing your own query
        res = sqlDb.query("SELECT * FROM event LIMIT 5")
        print(tabulate(res, headers="keys"))
        return res

    def printDatasourceStats(self):
        """
        prints statistics about the different datasources
        """
        datasourceIds = self.corpus.lookupIds
        stats = []
        for id in datasourceIds:
            events = self.corpus.getDataSource(id).eventManager.getList()
            series = self.corpus.getDataSource(id).eventSeriesManager.getList()
            stats.append({
                "datasource":id,
                "#events":len(events),
                "#series":len(series)
            })
        print("\nDatasource statistics:")
        print(tabulate(stats,headers="keys"))

    def printAvailableDatasourceIds(self):
        """
        Print the IDs of the available datasources

        Returns:
            list of datasource ids
        """
        ids = self.corpus.lookupIds
        print("Available datasource ids: ", ids)
        return ids

    def printCacheFile(self):
        """
        Prints the location of the ConferenceCorpus cache file (sqlite database)

        Returns:
            str absolut path to cache file
        """
        path = EventStorage.getStorageConfig().getCachePath() + "/EventCorpus.db"
        print(f"ConferenceCorpus cache is stored at {path}")
        return path


if __name__ == '__main__':
    cc = ConferenceCorpusIntro()
    cc.printCacheFile()
    cc.printAvailableDatasourceIds()
    cc.printEventsOfDatasource(sourceId="wikidata")
    cc.printEventsOfSeries(sourceId="or", seriesAcronym="AAAI", limit=5)
    cc.printSqlQueryResult()
    cc.printDatasourceStats()

