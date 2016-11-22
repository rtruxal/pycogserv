
Intro
=====

VERSION=0.0.3 | supports Python 2.7


####An Overly Explanatory Intro to Cognitive Services aka Bing Search API v5
 
 This code has been designed as a teaching tool. Where applicable, efficiency has been sacrificed to make functionality clear. The first file you should check out is `py-cog-serv.source.constants`. Snippits of it are shown in the "Usage" section below. As of now, this tool supports only basic web-search. Contributions are welcome and needed!


Installation
============
This module is not yet packaged. Until then, here is a sample import into REPL.

```py
>>> import os, sys
>>> os.path.exists(os.path.normpath('/path/to/py-cog-serve/'))
True
>>> sys.path.append(os.path.normpath('/path/to/py-cog-serve/'))
>>> from source.SearchWeb import BingWebSearch
```


Usage
=====
####Step 1: Customize Headers & Optional Query Params

Study constants.py, it will guide you through the decisions you're in charge of making. The tool will take care of their implementation. Keep in mind the API-key must be passed manually to the constructor in step 2.
 
From `source.constants.user_constants`:
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
    INCLUDED_PARAMS['cc'] = None               # <--(See static_constants.COUNTRY_CODES below for available options)
    INCLUDED_PARAMS['count'] = None            # <--(Enter a number from 0-50. Must by type==str. EX: count of 5 should be "5")
    INCLUDED_PARAMS['freshness'] = None        # <--(Poss values are 'Day', 'Week', or 'Month')
    INCLUDED_PARAMS['mkt'] = None              # <--(See static_constants.MARKET_CODES below for available options)
    INCLUDED_PARAMS['offset'] = None           # <--(Use this in conjunction with totalEstimatedMatches and count to page. Same format as 'count')
    INCLUDED_PARAMS['responseFilter'] = None   # <--(Poss values are 'Computation', 'Images', 'News', 'RelatedSearches', SpellSuggestions', 'TimeZone', 'Videos', or 'Webpages')
    INCLUDED_PARAMS['safeSearch'] = None       # <--(Poss values are 'Off', 'Moderate', and 'Strict.')
    INCLUDED_PARAMS['setLang'] = None          # <--(See ISO 639-1, 2-letter language codes here: https://www.loc.gov/standards/iso639-2/php/code_list.php)
    INCLUDED_PARAMS['textDecorations'] = None  # <--(Case-insensitive boolean. '(t|T)rue', or '(f|F)alse')
    INCLUDED_PARAMS['textFormat'] = None       # <--(Poss values are 'Raw', and 'HTML.' Default is 'Raw' if left blank.)
```

 You'll notice that `constants.py` has two classes included in it: `user_constants` and `static_constants`. 
 * `user_constants` gives access to the default headers and query-modifiers used when a `BingWebSearch` object is instantiated.
 * `static_constants` can be used as reference. Check out:
    * `static_constants.COUNTRY_CODES`
    * `static_constants.MARKET_CODES`
    * `static_constants.ERROR_CODES`
    * `static_constants.SPECIALTY_APIS`
    * `static_constants.BASE_ENDPOINT` as well as the alternative formats of the other `static_constant.XXX_ENDPOINT`s listed.



####Step 2: Search For Web Results:
```py
>>> from source.SearchWeb import BingWebSearch

>>> search_query = "ENTER YOUR ARBITRARY SEARCH TERMS HERE"
>>> api_key = "ENTER ONE OF YOUR API KEYS HERE"

>>> # First things first, we instantiate the seach interface object.
>>> web_searcher = BingWebSearch(api_key=api_key, query=search_query, safe=False, headers=constants.HEADERS, addtnl_params=constants.INCLUDED_PARAMS) 
>>> # see source.constants.static_constants.BASE_QUERY_PARAMS for compatible params. Must be in {param : value} format
 
>>> # Quickly notice that the web_searcher instance will keep track of your 'offset' value every time you call the .search() method.
>>> web_searcher.current_offset
0
>>> # 0 makes sense. We haven't run .search() yet, and we didn't alter user_constants.INCLUDED_PARAMS['offset'] = None.

>>> # .search() returns a list of WebResult objects. Each WebResult is __repr__'d with its display URL.
>>> packaged_json = web_searcher.search() 

>>> # The default number of results requested is 50, the maximum # of results Bing will return per query.
>>> len(packaged_json)
50

>>> # Let's check the web_searcher's offset value again 
>>> web_searcher.current_offset
50

>>> # Now we know that running web_searcher.search() again will return the next 50 results.
>>> packaged_json_2 = web_searcher.search()
>>> web_searcher.current_offset
100
>>> packaged_json == packaged_json_2
False
```



Notes
=====

2016-11-15: Added support & checking-mechanism for web-search query parameters
2016-11-18: Added separate modules for Universal constants and validators.
2016-11-22: Added support for paging. Offloaded all URL encoding to requests for congruence.

Massive swaths of this v5 API interface were graciously stolen from py-bing-search which you can find here: https://github.com/tristantao/py-bing-search


I AM NOT A PROFESSIONAL DEV AND JUST STARTING THIS.

PLEASE HELP ME FIX CURRENT IF/ELSE HELL.


TODO
=====
* Parse the return JSON!...like any of it! just do something it's a mess! **FINISHED-(ALPHA)**
* Add image/news/video classes w/ support for API-specific querying
* Fix query params-checking. **FINISHED-(ALPHA)**
* Parse queries into URLs better. **FINISHED-(ALPHA)**
    * Use requests.utils.quote or some-such to encode things properly.**FINISHED-(ALPHA)**
* Set up error handling for query/second errors. Use time.sleep(1). **FINISHED-(ALPHA)**
* Implement paging with self.current_offset. **FINISHED-(ALPHA)**
* Ensure Python3 compatibility w/ try: except: statement for manual header entry.
    * (Currently using `raw_input`)