from socket import gethostname, gethostbyname
from time import sleep

import requests
from pycogserv.constants import user_constants, static_constants
from pycogserv.utils.dict_mod import OrderedDictWithPrepend
from pycogserv.utils.validations import QueryChecker, ResponseChecker

# import pdb

"""
Massive swaths of this v5 API interface were graciously stolen from py-bing-search
you can find it here: https://github.com/tristantao/py-bing-search

Modify query params in class 'constants.'
    - You can create your own own query-param-dict as a replacement, but use OrderedDict. 'q' must be the first key at runtime.
    - Dict entries of format "YourDict[key] == None" will be ignored and can therefore be safely included.



TODO:
    - Add image/news/video classes w/ support for API-specific querying
        --Base Endpoint URLs for these are partially built in class "constants"
    - implement paging with self.current_offset.
"""


class BingSearch(object):
    """
    Base-Class to elimnate redundancy for the common functionalities that cut across APIs
    """

    def __init__(self, api_key, query, safe=False, header_dict=user_constants.HEADERS):
        self.api_key = api_key
        self.safe = safe
        self.query = query
        # Paging-support
        self.current_offset = 0
        self.total_estimated_matches = None
        self.last_url_sent = None
        # Cache last response
        self.last_response = None
        self.last_response_packaged = None

        if header_dict is user_constants.HEADERS:
            self.header = header_dict
            self.header.prepend('Ocp-Apim-Subscription-Key', api_key)
            for key, val in list(self.header.items()):
                if val == None:
                    ## TODO: make self.header handle/ignore NoneType entries.
                    del self.header[key]
        else:
            self.header = self.manual_header_entry()

    def search(self, limit=50, **kwargs):
        """
        :param limit: number of results to return. max is 50.
        :return json_results: a mess of json right now...in a dictionary.
        """
        return self._search(limit=50, **kwargs)

    def manual_header_entry(self):
        """
        Specify your own headers like a BOSS!

        (Note: spoof At your own peril. Complications abound.)
        :return: Nothing. This sets input. No type checking for max customizations.
        """
        while True:
            headr = OrderedDictWithPrepend()
            if not headr:
                api_key = eval(input('enter your api key'))
                ua_str = eval(input('enter a valid User-Agent string'))
                ipaddr = eval(input('enter your ip address (or leave blank to autodetect)'))
                if not ipaddr:
                    ipaddr = gethostbyname(gethostname())
                headr['Ocp-Apim-Subscription-Key'] = api_key
                headr['User-Agent'] = ua_str
                headr['X-Search-ClientIP'] = ipaddr
            print(('\nYour auth-key is {}\nYour User-Agent string is {}\nYour ip address will appear as {}\n\n\n\n'.format(
                headr['Ocp-Apim-Subscription-Key'], headr['User-Agent'], headr['X-Search-ClientIP'])))
            response1 = eval(input(
                'To change your auth-key enter (a)\nTo change your User-Agent string enter (u)\nTo change your ip address enter (i)\n\nIf you are satisfied, press (y) to confirm, or (n) to start over.\n> :'))
            if response1.lower() == 'y':
                return headr
            elif response1.lower() == 'n':
                del headr
                continue
            elif response1.lower() == 'a':
                headr['Ocp-Apim-Subscription-Key'] = eval(input('enter your api key'))
                continue
            elif response1.lower() == 'u':
                headr['User-Agent'] = eval(input('enter a valid User-Agent string'))
                continue
            elif response1.lower() == 'i':
                headr['X-Search-ClientIP'] = eval(input('enter "your" ip address'))
                continue
            else:
                print(('{} is not a valid option. Try again.'.format(response1)))
                continue


class BingWebSearch(BingSearch):
    """
    Web Search Object.
    Allows for default or manual header entry.
    Mandatory fields are 'api_key' and 'query'
    Other defaults will specify you as a firefox user, add no addtnl query params, and will give you the max of 50 results returned for your query
    Currently no support for paging, but functionality is in the works.
    """

    def __init__(self, api_key, query, safe=False, header_dict=user_constants.HEADERS,
                 addtnl_params=user_constants.INCLUDED_PARAMS):
        self._BASE_URL = static_constants.WEBSEARCH_ENDPOINT
        self.param_dict = OrderedDictWithPrepend()
        if addtnl_params and type(addtnl_params) == OrderedDictWithPrepend:
            for key, value in list(addtnl_params.items()):
                if key in static_constants.BASE_QUERY_PARAMS[2:]:
                    self.param_dict[key] = addtnl_params[key]
                else: raise ValueError('One or more keys in param-dict are not valid params.')
        elif not addtnl_params:
            pass
        else:
            raise TypeError('Additional params must be in dictionary-format: {param_name : param_val}')
        ## Build header inside inherited BingSearch class.
        BingSearch.__init__(self, api_key=api_key, query=query, safe=safe, header_dict=header_dict)

        ## Run query validations
        is_ok = QueryChecker.check_web_params(self.param_dict, self.header)
        if is_ok:
            print('Query params PASSED validation.')
        else:
            raise AttributeError('query checker has a bug')
        print(('run <instance>.search() to run query and print json returned\ncurrent URL format is {}'.format(
            self._BASE_URL)))

    def _search(self, limit, override=False, newquery=None):
        """
        Meat-&Potatoes of the search. Inserts search query and makes API call.
        :param limit: Number of return results. Max is 50
        :param override: Set to True if you intend to use 'newquery' to modify the query on the fly
        :param newquery: enter new query value if you so choose. Will not change query params.
        :return json_results: list of packaged JSON results returned from Microsoft.
        see WebResult class below.
        """

        # Allow _search to initialize new query.
        if override and newquery:
            self.query = newquery
            self.current_offset = 0
            self.total_estimated_matches = None
        elif override and not newquery:
            raise AssertionError('query override has been activated but you have not specified a new query.')

        # Modify some variable/nonvariable params to enable paging and restrict query to webpages.
        if 'q' in list(self.param_dict.keys()):
            if override:
                del self.param_dict['q']
                self.param_dict.prepend('q', self._insert_web_search_query(override=override, newquery=newquery))
            else:
                print(('keeping {} as search-query value'.format(self.query)))
                pass
        else:
            self.param_dict.prepend('q', self._insert_web_search_query(override=override, newquery=newquery))
        self.param_dict['offset'] = self.current_offset
        self.param_dict['responseFilter'] = 'Webpages'
        if limit > 50 or limit < 1:
            raise ValueError('limit must be positive integer b/w 1 and 50')
        else:
            self.param_dict['count'] = str(limit)

        # Query the API. Receive response object.
        try:
            response_object = requests.get(self._BASE_URL, params=self.param_dict, headers=self.header)
        except requests.Timeout:
            print('requests module timed out. Returning NoneType')
            return None

        # Handle error-codes and Preempt garbage results if URL is too long.
        if len(response_object.url) > 1500:
            raise ValueError('URL too long. Limit URLs to < 1,200 chars.')
        response_validated = ResponseChecker.validate_request_response(response_object)
        if response_validated == '429':
            response_object = self._handle_429_error(url=response_object.url)
        else:
            pass

        # Return packaged JSON or HTML. Update 'current_offset' and 'last_response...' caches.
        self.last_response = response_object
        self.last_url_sent = response_object.url
        if 'textFormat' in list(self.param_dict.keys()) and self.param_dict['textFormat']:
            if self.param_dict['textFormat'].upper() == 'HTML':
                self.current_offset += min(50, limit)
                print('returning HTML w/o packaging. <instance>.last_response_packaged will remain set to None.')
                return response_object.text()
        else:
            packaged_json = self._parse_json(response_object.json())
            self.last_response_packaged = packaged_json
            self.current_offset += min(50, limit, len(packaged_json))
            return packaged_json


    def _parse_json(self, json_response):
        """
        Takes raw JSON response and packages them as instances of class WebResult.
        :param json_response: EX -- <requests_response_object>.json()
        :return list of WebResult objects: parsed and prettied JSON results with easy data-access.
                Returned as a LIST of WebResult objects with len == the # of links returned by Bing.
        """
        if not self.total_estimated_matches:
            print(('Bing says there are an estimated {} results matching your query'.format(json_response['webPages']['totalEstimatedMatches'])))
            self.total_estimated_matches = int(json_response['webPages']['totalEstimatedMatches'])
        packaged_json = [WebResult(single_json_entry) for single_json_entry in json_response['webPages']['value']]
        return packaged_json


        # return response_data
        # packaged_results = [WebResult(single_result_json) for single_result_json in json_results['d']['results']]
        # self.current_offset += min(50, limit, len(packaged_results))
        # return packaged_results

    def _handle_429_error(self, url):
        timeout_cnt = 0
        while True:
            if timeout_cnt < 5:
                sleep(2)
                r2 = requests.get(url, self.header)
                if ResponseChecker.validate_request_response(r2) == '429':
                    timeout_cnt += 1
                    pass
                elif r2.status_code == 200:
                    break
                else:
                    raise AssertionError('response not successful')
            else:
                raise IOError(static_constants.ERROR_CODES['429'])
        return r2

    def _insert_web_search_query(self, override=False, newquery=None):
        if override:
            return newquery
        else:
            return self.query


class WebResult(object):
    '''
    Attributes which can be called from WebResult instance(WRi) --

    WRi.json: full JSON entry.
    WRi.url: The URL sent back by Bing.
    WRi.display_url: Display URL. Not always accurate.
    WRi.name: The title of the page linked to by WRi.url.
    WRi.snippet: A snippet of text from the page linked to by WRi.url.
    WRi.id: the index value for this JSON entry. Used primarily for compound queries.
    '''

    def __init__(self, result):
        self.json = result
        self.url = result.get('url')
        self.display_url = result.get('displayUrl')
        self.name = result.get('name')
        self.snippet = result.get('snippet')
        self.id = result.get('id')
        try:
            self.date_crawled = result.get('dateLastCrawled')
            self.about = result.get('about')
        except Exception:
            self.date_crawled = None
            self.about = None
        # maintain compatibility
        self.title = result.get('name')
        self.description = result.get('snippet')

    def __repr__(self):
        return 'WebResponse Obj: {}'.format(self.display_url)