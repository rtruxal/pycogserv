
Intro
=====

Currently only supports Python 2.7

This is an attempt to adapt tristantaos's [py-bing-search] (https://github.com/tristantao/py-bing-search) to Microsoft's new Cognitive Services APIs (aka Bing Search API v5) interface.
Bing has notified their customers that all APIs with 'datamarket' in their endpoint URL will be deactivated on December 15th 2016.

As of now, this tool supports only basic web-search and basic query params detailed in source.SearchWeb.constants
Contributions are welcome and needed!


Installation
============
This module is not yet packaged. Until then, here is a sample import into REPL.
The following assumes your current working directory is '.../PATH/TO/py-cog-serv'
```py
>>> import os, sys
>>> sys.path.append(os.getcwd())
>>> from source.SearchWeb import BingWebSearch
```



Usage
=====

Remember to set the `api_key` as your own.

####For Web Results:
```py
>>> from py-cog-serv.source.SearchWeb import BingWebSearch
>>> search_query = "ENTER YOUR ARBITRARY SEARCH TERMS HERE"
>>> web_searcher = BingWebSearch(api_key=api_key, query=search_query, safe=False, headers=constants.HEADERS, addtnl_params=None) 
>>> # see source.SearchWeb.constants list of BASE_QUERY_PARAMS for compatible params. Must be in {param : value} format
>>> return_json = web_searcher.search(limit=50) 
>>> # 50 is the maximum number results returned per query. Pagination is in the works.
```


Notes
=====

Massive swaths of this v5 API interface were graciously stolen from py-bing-search which you can find here: https://github.com/tristantao/py-bing-search


I AM NOT A PROFESSIONAL PROGRAMMER AND JUST STARTING THIS.

PLEASE HELP ME MAKE THIS NOT AWFUL.


TODO
=====
* Parse the return JSON!...like any of it! just do something it's a mess!
* Add image/news/video classes w/ support for API-specific querying
    * Base Endpoint URLs for these are partially built in class "constants"
* Fix query params-checking
* Parse queries into URLs better.
    * Use requests.utils.quote or some-such to encode things properly.
* Set up error handling for query/second errors. Use time.sleep(1).
* Implement paging with self.current_offset.
* Ensure Python3 compatibility w/ try: except: statement for manual header entry.
    * (Currently using `raw_input`)