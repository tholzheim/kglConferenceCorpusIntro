[![Build](https://github.com/tholzheim/kglConferenceCorpusIntro/actions/workflows/build.yml/badge.svg)](https://github.com/tholzheim/kglConferenceCorpusIntro/actions/workflows/build.yml)
[![GitHub issues](https://img.shields.io/github/issues/tholzheim/kglConferenceCorpusIntro)](https://github.com/tholzheim/kglConferenceCorpusIntro/issues)
# Introduction to the usage of the ConferenceCorpus

This project demonstrates how [ConferenceCorpus](https://github.com/WolfgangFahl/ConferenceCorpus) can be integrated into a project and how the data can be loaded and accessed.


## Requirements

### System Requirements
* [python](https://www.python.org/) >3.6 (with the [tkinter](https://docs.python.org/3/library/tkinter.html) package)
* \>= 4GB RAM

### OS Specific Preparations
* [Windows setup](./docs/windows_setup.md)

### Data Sources Requirements
Before running the tests ensure that the raw data of the data sources is downloaded by running the following scripts:
```
$ scripts/install
$ scripts/getbackup
$ scripts/getofflinedata
```

## Testing
To test if the data sources of the ConferenceCorpus are loaded correctly run `$scripts/test`. 
The script runs a [Test](./tests/test_ConferenceCorpusIntro.py) that loads all data sources from the previously downloaded raw data.
Running the test the first time takes about ~5 min but when running it again it will load the data from its cache (`$HOME/.conferenceCorpus/EventCorpus.db`) taking ~40 seconds.
To enforce a reloading from the data sources itself, set forceUpdate to `True` when loading the data sources.

The output of the test sould look like this:
```bash
$ bash scripts/test
Starting test test_loadingOfDatasources, debug=False ...
Loading the datasources (this might take some time)
configureCorpusLookup callback called
Warning - using full /home/vmt14/.dblp/dblp.xml dataset ~0.0m records!
Warning - using full /home/vmt14/.dblp/dblp.xml dataset ~0.0m records!
Available datasource ids:  ['confref', 'crossref', 'dblp', 'gnd', 'wikidata', 'wikicfp', 'or', 'or-backup', 'orclone', 'orclone-backup']
confref has 37945 events and 4857 series
crossref has 49280 events and 1 series
dblp has 47891 events and 5256 series
gnd has 1000000 events and 1 series
wikidata has 7508 events and 4254 series
wikicfp has 87987 events and 6019 series
or has 9473 events and 1058 series
or-backup has 9231 events and 1028 series
orclone has 9477 events and 1086 series
orclone-backup has 9338 events and 1057 series
test test_loadingOfDatasources, debug=False took 286.1 s
.
----------------------------------------------------------------------
Ran 1 test in 286.119s

OK
```

You can also check if the data sources at there storage location:

|location|data sources|
|---|---|
|`$HOME/.conferencecorpus/`|wikicfp,crossref and confref also the EventCorpus.db is stored here |
|`$HOME/.dblp/`|dblp (to get the  complete data dump (~4GB) see [ConferenceCorpusIntro](./src/main.py))|
|`$HOME/.or/`|openresearch ([original](https://www.openresearch.org/wiki/Main_Page) and [clone](https://confident.dbis.rwth-aachen.de/or/index.php?title=Main_Page)) wiki-Markup files|

## Integrating and Using the ConferenceCorpus

The procedure on how to load and access the ConferenceCorpus is described in the class [ConferenceCorpusIntro](./src/main.py).
An overview of the different data sources can be found in the [official wiki](http://wiki.bitplan.com/index.php/ConferenceCorpus)