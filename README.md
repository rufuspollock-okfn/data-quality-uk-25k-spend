# data.gov.uk expenditure reports
Set of tools to grab, store and generate reports on expenditure docs and publishers of http://data.gov.uk Defines strong modular approach. Tools use CLI pipelines for data exchange. This way atomic scripts may be mixed in execution chain for different results. For example to get publishers from http://data.gov.uk and store them in DB one can do: ```sh
grab_publishers.py | update_db.py --table publisher
```
Or in case of need to genrate *.xls* report directly:
```sh
grab_publishers.py | publishers_xls.py
```

Installation and configuration
------------------------------
Scripts utilize sqlite DB for storing grabbed data. For DB init run:
```sh
python init_db.py
```

Create a reports dir where all reports will be generated to. And then update ```settings.py``` with correct ```REPORTS_PATH```.

If necessary update other options of ```settings.py```.

Grab data
---------
Two scripts are used for data grabbing:
* ```grab_publishers.py``` — grab all publishers and output in *stdout*.
```sh
# Grab all publishers and store in DB
grab_publishers.py | update_db.py --table publisher
```
* ```grab_files.py``` — grab all files for publishers passed in *stdin* and print in *stdout*.
```sh
# Get all publishers from DB, grab their files and store in DB
extract_db.py --table publisher | grab_files.py | update_db.py --table datafile
```

All records in DB will have unique ```ID```. There are no duplicating records.

Publishers report
-----------------
Get all publishers sorted by type and create .xls report:
```sh
extract_db.py --table publisher --orderby type | publishers_xls.py
```

Files report
------------
Get all files and create .xls report. Files will be grouped by publisher:
```sh
extract_db.py --table datafile | datafiles_xls.py
```

Other tools
-----------
* ```update_db --table <table name>``` — gets *stdin* input strings, split them by ```settings.py:CSV_DELIMETER``` and store in ```<table name>``` DB table.
* ```extract_db --table <table name>[ --orderby <column name>]``` — get data from DB and output in *stdout*. Sort data if optional param specified.
