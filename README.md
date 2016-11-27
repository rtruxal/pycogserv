
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
#Step 1: Customize Headers & Optional Query Params


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




##Step 2: Search For Web Results:
```py
>>> from source.SearchWeb import BingWebSearch
>>> from source.constants import user_constants, static_constants #<--Not necessary. Added for clarification

>>> search_query = "ENTER YOUR ARBITRARY SEARCH TERMS HERE"
>>> api_key = "ENTER ONE OF YOUR API KEYS HERE"
```

First things first, instantiate the seach interface object.
```py
>>> web_searcher = BingWebSearch(api_key=api_key, query=search_query, safe=False, headers=user_constants.HEADERS, addtnl_params=user_constants.INCLUDED_PARAMS) 
>>> # see source.constants.static_constants.BASE_QUERY_PARAMS for 
>>> # compatible params. Must be in {param : value} format
 ```
 
Quickly notice that the web_searcher instance will keep track of your 'offset' value every time you call the .search() method. **This will be important in Step 3: Paging Results**
```py
>>> print web_searcher.current_offset
0
>>> # 0 makes sense here. We haven't run .search() yet, and we didn't 
>>> # alter the "user_constants.INCLUDED_PARAMS['offset'] = None" option above.
```

.search() returns a list of WebResult objects. Each WebResult is `__repr__`'d with its display URL.
```py
>>> packaged_json = web_searcher.search()
'Bing says there are an "estimated" 149 results matching your query'
>>> packaged_json[0]
WebResponse Obj: www.madeupwebsite.com
```

The WebResponse objects will expose the meat & potatoes if you will. Check it out:
```PY
>>> WebResp1 = packaged_json[0]
>>> print WebResp1.about
[{some_key : some_value}]
>>> print WebResp1.snippet
'blahblah blah blah this is the site description for www.madeupwebsite.com blahblahblahblahhhhhh'
>>> print WebResp1.display_url
'www.madeupwebsite.com'
>>> print WebResp1.id
'https://api.cognitive.microsoft.com/api/v5/#WebPages.0'
>>> print WebResp1.name
'madeupwebsite.com the best site in the world ...'
>>> print WebResp1.date_crawled
2016-11-21 T20:51:00
>>> print WebResp1.json
{UNPARSED VERSION OF EVERYTHING ABOVE WILL BE HERE. GOOD FOR DEBUGGING OR HIGH-LEVEL VIEW}
>>> print WebResp1.url
'http://www.bing.com/cr?IG4537854378543873458787193244_ARRRRGHGHHHHHHFD2SA4HJ3KLJK4LSDFL<(^_^)>DFS43FJKA43730984%2fwww.madeupwebsite.com%2f&p=DevEx,9999'
```



##Step 3: Paging Results

Recall that `self.current_offset` value I referenced in step 2. The `offset` value can be used in conjunction with the `count` user_param to get a slice of the `totalEstimatedMatches` value which Bing exposes after your first query. 

Let's quickly recall what was printed when we called `.search()` for the first time.
```py
>>> packaged_json = web_searcher.search()
'Bing says there are an estimated 149 results matching your query'
```

Bing reported back that `totalEstimatedMatches` was 149 and **NOT** 150. Let's recap what values we have so far:
```py
>>> print web_searcher.total_estimated_matches
149
```

The default number of results requested is 50 (the maximum # of results Bing will return per query,) so that's the length of what we get when we call .search() 
```py
>>> len(packaged_json)
50
```

Now take a look at the current_offset value that we now have. 
```py
>>> web_searcher.current_offset
50
```
So, we've retrieved 50 out of the 149 total results that exist, and our offset value is now set to 50.


We know that running web_searcher.search() again will return 50 more results, so let's do .search() again and take a look at our numbers.
```py
>>> packaged_json_2 = web_searcher.search()
>>> len(packaged_json_2)
50
```

Now we check the web_searcher's offset value again. Remember that so far we've done 2 searches, and each one has given us 50 results.
```py
>>> web_searcher.current_offset
100
```

Has total_estimated_matches changed? Let's find out:
```py
>>> print web_searcher.total_estimated_matches
149
```
Nope. Still the same. This makes sense; the number of possible results should not change for any one query.


For good measure, we can check equivalency and make sure that `packaged_json_2` received different records than did `packaged_json`
```py
>>> packaged_json == packaged_json_2
False
```

Let's see what happens when we try to get the next 50 results. 
```py
>>> packaged_json_3 = web_searcher.search()
>>> print len(packaged_json_3)
49
>>> print web_searcher.current_offset
149
```
We didn't get 50! We got the rest of what was possible, and py-cog-serv recognized this and didn't throw an error in your face. That said, running .search() again with an offset value of 149 and a totalEstimatedResults value ALSO of 149, we will receive 0 objects from our query, and probably get some error thrown in our face.


For more advanced usage such as computational queries & compound queries, check back soon for guidance or poke at the code.

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