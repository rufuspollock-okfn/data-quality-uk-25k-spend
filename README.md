# Data quality - UK 25K spend

## Overview

This repository contains a set of statistics on the *quality* of 25K spend data published by the UK government on [data.gov.uk](http://data.gov.uk).

The statistics are a set of data quality results, and are published in the structure required for use in a [Data Quality Dashboard](https://github.com/okfn/data-quality-dashboard).

All data is available in the `data/*` directory. The repository itself is a valid [Data Package](http://dataprotocols.org/data-packages/): see the `datapackage.json` file for more information.

## Who defines "data quality"?

In the case of the UK 25K spend data, we assess quality based on two broad factors:

1. Are the tabular data files accessible at the provided URL?
2. Are the tabular data files themselves structurally valid?
3. Do the data files conform to the [HM Treasury regulations for publishing 25K spend data](https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/198197/Guidance_for_publishing_spend_over__25k.pdf)?

If you have a question or a concern about our methodology, please open an issue. We are open to adjustment based on feedback.

## Databases used in data collection

There is no API on data.gov.uk to concretely return all published 25K spend data, nor to return a list of all ministerial departments that are required to publish 25K spend data.

Due to these restrictions, it is possible that we may have missed publishers and data sources, or, added publishers and data sources that are not subject to the regulations for publishing 25K spend data.

Please [open an issue](https://github.com/okfn/uk-25k-spend-data-quality/issues) if you find this to be the case, so that we can update our scripts and results accordingly.

Currently we aim to analyze the files published by the ministerial departments listed in `data/publisher_lookup.csv`.

All information on publishers (Ministerial Departments) and sources (the data sources they release as 25K spend data) is acquired from [data.gov.uk](http://data.gov.uk).

The lists of publishers and data sources we have identified can be found in these files:

* `data/publishers.csv`
* `data/sources.csv`


## Data generated from running data quality checks

When we run data quality checks against `data/publishers.csv` and `data/sources.csv`, we write the results out to a number of other files, also located in the `data/*` directory. These files are:

* `data/runs.csv`
* `data/results.csv`
* `data/performance.csv`

In addition, we have a file called `instance.json` which provides some metadata to the [Data Quality Dashboard](https://github.com/okfn/data-quality-dashboard) that displays these results. That dashboard is publicly visible here:

* [UK 25K Spend Data Quality](http://uk-25k.openspending.org/)

## Installation

If you want to work with the data here, you first need to set up a Python development environment. It is recommended to create a Python 3 virtual environment, and to install the required dependencies as follows:

```
pip install -r scripts/requirements.txt
```

The installation will add the `dq` tool to your `PATH` (Also available as `dataquality`). Ensure it is installed and available by running the following in your terminal:

```
dq --help
```

## Data model

As the data in `data/*` serves as a database for a [Data Quality Dashboard](https://github.com/okfn/data-quality-dashboard), it conforms to a particular schema. Information about this schema [can be found here](https://github.com/okfn/data-quality-cli/#schema).

## Working with the data

### Data identification

First, we need to build out our `publishers.csv` and `sources.csv`. The following script does just that: acquires references to all data sources we can find on [data.gov.uk](http://data.gov.uk/)
published by the ministerial departments listed in `data/publisher_lookup.csv`
that contain 25k spend data.

```
python scripts/id_data.py
```

After running this script, `data/publishers.csv` and `data/sources.csv` will have entries for the most recent data we could identify as 25k spend data published by those ministerial departments.


### Assessing data quality

[Data Quality CLI](https://github.com/okfn/data-quality-cli) assesses the quality of each data source, and thereby the quality of the data publication of each publisher. It makes this assessment each time it is run, and also builds up an assessment of quality over time.

#### Configuring Data Quality CLI

Data Quality CLI needs a configuration file in order to run against a set of data sources. This configuration file is typically called `dq.json` and located in a repository with the files.

The configuration file is responsible for:

* The file names used to build the data quality database.
* The options passed to the GoodTables batch processor, which runs the data quality assessment.

A typical configuration file looks like this:

```
# dq.json
{
  "data_dir": "data",
  "result_file": "results.csv",
  "run_file": "runs.csv",
  "source_file": "sources.csv",
  "publisher_file": "publishers.csv",
  "remotes": ["origin"],
  "branch": "master",
  "goodtables": {
    "location": "http://goodtables.okfnlabs.org/",
    "processors": ["structure", "schema"],
    "arguments": {
      "pipeline": {
        "post_task": "",
        "options": {}
      },
      "batch": {
        "post_task": ""
      }
    }
  }
}
```

Note that `data_dir` is either an absolute path, or a path **relative to the path of the config file**.

#### Running the Data Quality CLI

```
dq run dq.json
```

Essentially, the data quality run is a [Good Tables batch process](http://goodtables.readthedocs.org/en/latest/batch.html). on each row in `data/sources.csv`. GoodTables has hooks for passing in pre and post task runners for both each individual pipeline, and, the whole batch process.

These task runners are responsible for the actual data quality assessment, building on the raw information the GoodTables collects on all the data sources, and, while the Data Quality CLI ships with default post processing tasks, you may pass in your own custom tasks if they are API compatible, via `dq.json`.

**Important**: *the encoding argument.*

Good Tables can automatically detect encoding, but it can also be wrong.
This allows you to explicitly pass in an encoding to be used to read the data file stream.

Data Quality CLI will fetch the files that were found at the url provided by `data/sources.csv`,and store them locally in the `fetched/*` directory. These data sources should be committed to this repository along with each data quality run that is committed. This helps build an audit trail of the files actually assessed for a give data quality assessment.


### Publish the assessment

Once the results have been collected, publish the assessment by committing and pushing back to GitHub. The Data Quality Dashboard for this dataset will automatically start using the new data.
