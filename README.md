
Intro
=====

VERSION=0.0.2 | supports Python 2.7


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
 You'll notice that `constants.py` has two classes included in it: `user_constants` and `static_constants`. 
 * `user_constants` gives access to the default headers and query-modifiers used when a `BingWebSearch` object is instantiated.
 * `static_constants` can be used as reference. Check out:
    * `static_constants.COUNTRY_CODES`
    * `static_constants.MARKET_CODES`
    * `static_constants.ERROR_CODES`
    * `static_constants.SPECIALTY_APIS`
    * `static_constants.BASE_ENDPOINT` as well as the alternative formats of the other `static_constant.XXX_ENDPOINT`s listed.

Study the constants page, it will guide you through the decisions you're in charge of making. The tool will take care of their implementation. Keep in mind the API-key must be passed manually to the constructor in step 2.
 
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


####Step 2: Search For Web Results:
```py
>>> from py-cog-serv.source.SearchWeb import BingWebSearch
>>> search_query = "ENTER YOUR ARBITRARY SEARCH TERMS HERE"
>>> web_searcher = BingWebSearch(api_key=api_key, query=search_query, safe=False, headers=constants.HEADERS, addtnl_params=constants.INCLUDED_PARAMS) 
>>> # see source.constants.static_constants.BASE_QUERY_PARAMS for compatible params. Must be in {param : value} format
>>> return_json = web_searcher.search(limit=50) 
>>> # 50 is the maximum number results returned per query. Pagination is in the works.
```



Notes
=====

2016-11-15: Added support & checking-mechanism for web-search query parameters
2016-11-18: Added separate modules for Universal constants and validators.

Massive swaths of this v5 API interface were graciously stolen from py-bing-search which you can find here: https://github.com/tristantao/py-bing-search


I AM NOT A PROFESSIONAL PROGRAMMER AND JUST STARTING THIS.

PLEASE HELP ME MAKE THIS NOT AWFUL.


TODO
=====
* Parse the return JSON!...like any of it! just do something it's a mess!
* Add image/news/video classes w/ support for API-specific querying
* Fix query params-checking. **FINISHED-(ALPHA)**
* Parse queries into URLs better. **FINISHED-(ALPHA)**
    * Use requests.utils.quote or some-such to encode things properly.
* Set up error handling for query/second errors. Use time.sleep(1). **FINISHED-(ALPHA)**
* Implement paging with self.current_offset.
* Ensure Python3 compatibility w/ try: except: statement for manual header entry.
    * (Currently using `raw_input`)