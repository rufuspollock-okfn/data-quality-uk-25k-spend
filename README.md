# data.gov.uk expenditure reports
Set of tools to grab, store and generate reports on expenditure docs and publishers of http://data.gov.uk Defines strong modular approach. Tools use CLI pipelines for data exchange. This way atomic scripts may be mixed in execution chain for different results. For example to get publishers from http://data.gov.uk and store them in DB one can do ```grab_publishers.py | update_db.py --table publisher``` or in case of need to genrate *.xls* report directly ```grab_publishers.py | publishers_xls.py```.

Installation and configuration
------------------------------
Grab data
---------
Generate report
---------------

