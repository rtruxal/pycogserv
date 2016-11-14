import requests
from fake_useragent import UserAgent as UA
from socket import gethostname, gethostbyname
from collections import OrderedDict
# from requests import utils
# import time
"""
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
"""



class constants(object):
    user_agent = UA()
    HEADERS = OrderedDict()

    HEADERS['Ocp-Apim-Subscription-Key'] = None
    HEADERS['User-Agent'] = user_agent.firefox
    HEADERS['X-Search-ClientIP'] = gethostbyname(gethostname())
    HEADERS['X-MSEdge-ClientID']= None
    # HEADERS['Accept'] = None
    # HEADERS['Accept-Language'] = None
    # HEADERS['X-Search-Location'] = None

    BASE_QUERY_PARAMS = (
        'search?q', # <-- if you change this to 'images/search?q' or 'news/search?q' it will change ze behavior much like repsonsefileter
        'category',  # <--news only
        'cc',
        'count',
        'freshness',
        'mkt',
        'offset',
        'responseFilter',
        'safeSearch',
        'setLang',
        'textDecorations', # <-- bool
        'textFormat',
    )
    SPECIALTY_APIS = {
        'images' : 'images/',
        'images_trending' : 'images/trending/', # <-- works only for en-US, en-CA, and en-AU
        'videos' : 'videos/',
        'videos_trending' : 'videos/trending/',
        'videos_details' : 'videos/details/',
        'news' : 'news/',
        'news_trending' : 'news/trendingtopics/' # <-- works only for en-US and zh-CN
    }

    BASE_ENDPOINT = 'https://api.cognitive.microsoft.com/bing/v5.0/'

    ## Commented out Endpoint URLs have special format which is not defined by .../search?q=...
    ## These are not yet supported
    WEBSEARCH_ENDPOINT = BASE_ENDPOINT + '{}='.format(BASE_QUERY_PARAMS[0])
    IMAGESEARCH_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['images'] + '{}='.format(BASE_QUERY_PARAMS[0])
    # IMAGESEARCH_TRENDING_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['images_trending'] + ?????
    VIDEOSEARCH_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['videos'] +'{}='.format(BASE_QUERY_PARAMS[0])
    # VIDEOSEARCH_TRENDING_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['videos_trending'] + ?????
    # VIDEOSEARCH_DETAILS_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['images_details'] + ?????
    NEWSSEARCH_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['news'] + '{}='.format(BASE_QUERY_PARAMS[0])
    # NEWSSEARCH_TRENDING_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['news_trending'] + ?????


class BingSearch(object):
    def __init__(self, api_key, query, safe=False, header_dict=constants.HEADERS):
        self._initial_url_built = False
        self.api_key = api_key
        self.safe = safe
        self.query = query
        self.current_offset = 0
        self.build_url()
        if header_dict is constants.HEADERS:
            self.header = header_dict
            self.header['Ocp-Apim-Subscription-Key'] = api_key
        else:
            self.header = self.manual_header_entry()

    def search(self, limit=50):
        """

        :param limit: number of results to return. max is 50.
        :return: a mess of json right now...in a list
        """
        return self._search(limit)

    def build_url(self, param_query_dict=None):
        if self._initial_url_built and param_query_dict:
            pass
        elif not self._initial_url_built:
            for param, cond in self.param_dict.items():
                newstring = '&{}={}'.format(param, cond)
                self.QUERY_URL = self.QUERY_URL + newstring
            self._initial_url_built = True
        else:
            raise EnvironmentError('SOMEFINK BROKE IN URL BUILD')

    def manual_header_entry(self):
        """
        Specify your own headers like a BOSS!

        (Note: spoof At your own peril. Complications abound.)
        :return: Nothing. This sets input. No type checking for max customizations.
        """
        while True:
            headr = OrderedDict()
            if not headr:
                api_key = raw_input('enter your api key')
                ua_str = raw_input('enter a valid User-Agent string')
                ipaddr = raw_input('enter your ip address (or leave blank to autodetect')
                if not ipaddr:
                    ipaddr = gethostbyname(gethostname())
                headr['Ocp-Apim-Subscription-Key'] = api_key
                headr['User-Agent'] = ua_str
                headr['X-Search-ClientIP'] = ipaddr
            print '\nYour auth-key is {}\nYour User-Agent string is {}\nYour ip address will appear as {}\n\n\n\n'.format(headr['Ocp-Apim-Subscription-Key'], headr['User-Agent'], headr['X-Search-ClientIP'])
            response1 = raw_input('To change your auth-key enter (a)\nTo change your User-Agent string enter (u)\nTo change your ip address enter (i)\n\nIf you are satisfied, press (y) to confirm, or (n) to start over.\n> :')
            if response1.lower() == 'y':
                return headr
            elif response1.lower() == 'n':
                del headr
                continue
            elif response1.lower() == 'a':
                headr['Ocp-Apim-Subscription-Key'] = raw_input('enter your api key')
                continue
            elif response1.lower() == 'u':
                headr['User-Agent'] = raw_input('enter a valid User-Agent string')
                continue
            elif response1.lower() == 'i':
                headr['X-Search-ClientIP'] = raw_input('enter "your" ip address')
                continue
            else:
                print '{} is not a valid option. Try again.'.format(response1)
                continue


class BingWebSearch(BingSearch):
    def __init__(self, api_key, query, safe=False, header_dict=constants.HEADERS, addtnl_params=None):

        self.QUERY_URL = constants.WEBSEARCH_ENDPOINT + '{}'
        self.param_dict = OrderedDict()

        if addtnl_params and type(addtnl_params) == dict:
            for rec in addtnl_params.keys():
                if rec in constants.BASE_QUERY_PARAMS:
                    self.param_dict[rec] = addtnl_params[rec]
        elif not addtnl_params:
            pass
        else: raise ValueError('Additional params must be in dictionary-format: {param : str}')
        # take base search endpoint and add specified addtnl params (if any)
        BingSearch.__init__(self, api_key=api_key, query=query, safe=safe, header_dict=header_dict )
        #
        print 'run <instance>.search() to run query and print json returned'


    def _search(self, limit, override=False, newquery=None):
        url = self._insert_web_search_query(override=override, newquery=newquery)
        r = requests.get(url, headers=self.header)
        json_results = r.json()
        """
        AS OF NOW I NEED TO PARSE THE JSON RESULTS.
        """
        return json_results
        # packaged_results = [WebResult(single_result_json) for single_result_json in json_results['d']['results']]
        # self.current_offset += min(50, limit, len(packaged_results))
        # return packaged_results


    def _insert_web_search_query(self, override=False, newquery=None):
        if override:
            return self.QUERY_URL.format(newquery)
        else:
            return self.QUERY_URL.format(self.query.replace(' ', '+'))



class WebResult(object):
    '''
    The class represents a SINGLE search result.
    Each result will come with the following:
    #For the actual results#
    title: title of the result
    url: the url of the result
    description: description for the result
    id: bing id for the page
    #Meta info#:
    meta.uri: the search uri for bing
    meta.type: for the most part WebResult
    '''

    class _Meta(object):
        '''
        Holds the meta info for the result.
        '''
        def __init__(self, meta):
            self.type = meta['type']
            self.uri = meta['uri']

    def __init__(self, result):
        self.url = result['Url']
        self.title = result['Title']
        self.description = result['Description']
        self.id = result['ID']

        self.meta = self._Meta(result['__metadata'])