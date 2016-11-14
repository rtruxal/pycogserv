
Intro
=====

This is an attempt to adapt tristantaos's [py-bing-search] (https://github.com/tristantao/py-bing-search) to Microsoft's new Cognitive Services APIs (aka Bing Search API v5) interface.
Bing has notified their customers that all APIs with 'datamarket' in their endpoint URL will be deactivated on December 15th 2016.

As of now, this tool supports only basic web-search and basic query params detailed in source.SearchWeb.constants
Contributions are welcome and needed!

Usage
=====

Remember to ser the 'api_key' as your own.

####For Web Results:
'''py
>>> from py-cog-serv import BingWebSearch
>>> search_query = "ENTER YOUR ARBITRARY SEARCH TERMS HERE'
>>> web_searcher = BingWebSearch(api_key=api_key, query=search_query, safe=False, headers=constants.HEADERS, addtnl_params=None) # see list of BASE_QUERY_PARAMS for compatible params. Must be in {param : value} format
>>> return_json = web_searcher.search(limit=50) # 50 is the maximum number results returned per query. Pagination is in the works.


Notes
=====

Massive swaths of this v5 API interface were graciously stolen from py-bing-search
you can find it here: https://github.com/tristantao/py-bing-search


I AM NOT A PROFESSIONAL PROGRAMMER AND JUST STARTING THIS.
PLEASE HELP ME MAKE THIS NOT AWFUL!


TODO:
    - parse the return JSON!...like any of it! just do something it's a mess!
    - Add image/news/video classes w/ support for API-specific querying
        --Base Endpoint URLs for these are partially built in class "constants"
    - fix query params-checking
    - parse queries into URLs better.
        --Use requests.utils.quote or some-such to encode things properly.
    - set up error handling for query/second errors. Use time.sleep(1).
    - implement paging with self.current_offset.