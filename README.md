# UK expenditure files

All data is in the `data/*` directory.

The data in `publishers.csv` and `sources.csv` comes from [data.gov.uk](http://data.gov.uk).

Based on this data, a set of statistics as to the quality of the published data has been collected using [SPD Admin](https://github.com/okfn/spd-admin), and is written to the `results.csv` and `runs.csv` files.

## Installation

The tooling for managing the data is written in Python. It is recommended to create a Py3 virtual environment, and to install the required dependencies as follows:

```
pip install -r scripts/requirements.txt
```

The installation will add the `spd-admin` tool to your PATH. Check that with:

```
spd-admin --help
```

## Data model

Data in `data/*` conforms to a data model. Find more about the data model in `datapackage.json`.

## Working with the data

### Collecting publisher data

There is a script that gets all public spending data from [data.gov.uk](http://data.gov.uk/).

```
python scripts/get_data.py
```

This will populate `publishers.csv` and  `sources.csv`. The `period_id` field in `sources.csv` will be automatically filled in by `scripts/get_data.py` thanks to `scripts/period.py`.

### Downloading data files

To download all data files from `sources.csv` and store them locally in `archive/date` run:

```
python scripts/fetch_datafiles.py
```

`date/` in `archive/date` will be the current date as `archive/2015-05-29/`. Those directories will be created by `scripts/fetch_datafiles.py` if they don't exist.

Downloaded files are not stored in this GitHub repository.

### Collecting quality results

[SPD Admin](https://github.com/okfn/spd-admin) collects statistical data on **publishers** and their **sources**, assessing the quality of each published data source, and the overall quality of output per publisher.

#### Configuring SPD Admin

SPD Admin needs a config file. This config sets basic information for running results and deploying the data to a remote.

A typical config file looks like this:

```
# spd-admin.config
{
    "data_dir": "data",
    "result_file": "results.csv",
    "run_file": "runs.csv",
    "source_file": "sources.csv",
    "publisher_file": "publishers.csv",
    "remotes": ["origin"],
    "branch": "master",
    "goodtables_web": "http://goodtables.okfnlabs.org"
}
```

Note that `data_dir` is either an absolute path, or a path **relative to the path of the config file**.

#### Running with SPD Admin

Before running SPD Admin do:

```
python scripts/make_local_sources.py
```

It will create `data/local_sources.csv`. It is a copy of `data/sources.csv` but with local urls.

Then run an http server on port 8000 and run:

```
python scripts/preprocess_sources.py
```

It will create `data/invalid_sources.csv` and `data/clean_sources.csv`. It will populate `data/invalid_sources.csv` with all invalid files in `data/sources.csv` (empty files, html files... etc) that can't be processed by SPD Admin. It will populate `data/clean_sources.csv` with all valid files in `data/sources.csv` that can be processed by SPD Admin.

Then run:

```
spd-admin run spd-admin.json --encoding ISO-8859-2
```

This will run a [Good Tables batch process](http://goodtables.readthedocs.org/en/latest/batch.html) on all the data sources.

Data sources are those in `data/clean_sources.csv`.

A new entry will be appended to the `results.csv` file for each data source that is processed, and a single new entry will be added to the `runs.csv` file to identify this run.

**Important**: *the encoding argument.*

Good Tables can automatically detect encoding, but it can also be wrong.
This allows you to explicitly pass in an encoding to be used to read the data source stream.

Then run:

```
python scripts/make_results.py
```

It will create `data/final_results.csv` and `data/final_runs.csv`. It will populate `data/final_results.csv` with all results from `data/results.csv` and add results for data sources in `data/invalid_sources.csv`.

Then, rename `data/final_results.csv` to `data/results.csv` and `data/final_runs.csv` to `data/runs.csv`.
Finally, run:

```
python scripts/make_performance.py
```

It will create `data/performance.csv` with all publishers performances by period.
