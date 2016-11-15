
Intro
=====

Currently only supports Python 2.7

VERSION=0.0.1


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

Do **NOT** enter your `api_key` into the header in step 1. It must be passed manually to the constructor in step 2.

####Step 1: Customize Headers & Optional Query Params
From SearchWeb.constants:
```py
    ###############################################
    ## Enter default-header customizations here. ##
    ###############################################
    HEADERS['Ocp-Apim-Subscription-Key'] = None
    HEADERS['User-Agent'] = user_agent.firefox
    HEADERS['X-Search-ClientIP'] = gethostbyname(gethostname())
    HEADERS['X-MSEdge-ClientID']= None
    HEADERS['Accept'] = None
    HEADERS['Accept-Language'] = None
    HEADERS['X-Search-Location'] = None

    ###############################################
    ##     Enter query customizations here.      ##
    ###############################################
    ## Web Params:
    INCLUDED_PARAMS['cc'] = None              # <--(See https://msdn.microsoft.com/en-us/library/dn783426.aspx#countrycodes)
    INCLUDED_PARAMS['count'] = None           # <--(Enter a number from 0-50. Must by type==str. EX: count of 5 should be "5")
    INCLUDED_PARAMS['freshness'] = None       # <--(Poss values are 'Day', 'Week', or 'Month')
    INCLUDED_PARAMS['mkt'] = None             # <--(See https://msdn.microsoft.com/en-us/library/dn783426.aspx)
    INCLUDED_PARAMS['offset'] = None          # <--(Use this in conjunction with totalEstimatedMatches and count to page. Same format as 'count')
    INCLUDED_PARAMS['responseFilter'] = None  # <--(Poss values are 'Computation', 'Images', 'News', 'RelatedSearches', SpellSuggestions', 'TimeZone', 'Videos', or 'Webpages')
    INCLUDED_PARAMS['safeSearch'] = None      # <--(Poss values are 'Off', 'Moderate', and 'Strict.')
    INCLUDED_PARAMS['setLang'] = None         # <--(See ISO 639-1, 2-letter language codes here: https://www.loc.gov/standards/iso639-2/php/code_list.php)
    INCLUDED_PARAMS['textDecorations'] = None # <--(Case-insensitive boolean. '(t|T)rue', or '(f|F)alse')
    INCLUDED_PARAMS['textFormat'] = None      # <--(Poss values are 'Raw', and 'HTML.' Default is 'Raw' if left blank.)
```


####Step 2: Search For Web Results:
```py
>>> from py-cog-serv.source.SearchWeb import BingWebSearch
>>> search_query = "ENTER YOUR ARBITRARY SEARCH TERMS HERE"
>>> web_searcher = BingWebSearch(api_key=api_key, query=search_query, safe=False, headers=constants.HEADERS, addtnl_params=constants.INCLUDED_PARAMS) 
>>> # see source.SearchWeb.constants list of BASE_QUERY_PARAMS for compatible params. Must be in {param : value} format
>>> return_json = web_searcher.search(limit=50) 
>>> # 50 is the maximum number results returned per query. Pagination is in the works.
```


Notes
=====

2016-11-15: Added support & checking-mechanism for web-search query parameters


Massive swaths of this v5 API interface were graciously stolen from py-bing-search which you can find here: https://github.com/tristantao/py-bing-search


I AM NOT A PROFESSIONAL PROGRAMMER AND JUST STARTING THIS.

PLEASE HELP ME MAKE THIS NOT AWFUL.


TODO
=====
* Parse the return JSON!...like any of it! just do something it's a mess!
* Add image/news/video classes w/ support for API-specific querying
    * Base Endpoint URLs for these are partially built in class "constants"
* Fix query params-checking. **FINISHED-(ALPHA)**
* Parse queries into URLs better. **FINISHED-(ALPHA)**
    * Use requests.utils.quote or some-such to encode things properly.
* Set up error handling for query/second errors. Use time.sleep(1).
* Implement paging with self.current_offset.
* Ensure Python3 compatibility w/ try: except: statement for manual header entry.
    * (Currently using `raw_input`)