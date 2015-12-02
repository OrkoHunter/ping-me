 **These files operate on a private server which serves the database for ping- me.**

* Dependencies 
	* [`tornado`](https://github.com/tornadoweb/tornado) : A Python web framework and asynchronous networking library
	* [`torndb`](https://github.com/bdarnell/torndb) : A lightweight wrapper around MySQLdb. Originally part of the Tornado framework.

* Files :
	  * **`request.py`** : Recieves POST request from the user. The requests are of two types : 

            1. Configuration settings
            2. Reminders

	Both are received, processed and then the database is changed accordingly.

     * **`put.py`** : Scrapes message from database if the next ping is within 60 seconds.
