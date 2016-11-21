from socket import gethostname, gethostbyname
from time import sleep
import requests
from dict_mod import OrderedDictWithPrepend
from constants import user_constants, static_constants
from validations import QueryChecker, ResponseChecker

"""
Massive swaths of this v5 API interface were graciously stolen from py-bing-search
you can find it here: https://github.com/tristantao/py-bing-search

Modify query params in class 'constants.'
    - You can create your own own query-param-dict as a replacement, but use OrderedDict. 'q' must be the first key at runtime.
    - Dict entries of format "YourDict[key] == None" will be ignored and can therefore be safely included.

PLEASE HELP ME MAKE THIS NOT AWFUL!

TODO:
    - parse the return JSON!...like any of it! just do something it's a mess!
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
        self.current_offset = 0
        self.last_url_built = None

        if header_dict is user_constants.HEADERS:
            self.header = header_dict
            self.header['Ocp-Apim-Subscription-Key'] = api_key
            for key, val in self.header.items():
                if val == None:
                    del self.header[key]
        else:
            self.header = self.manual_header_entry()

    def search(self, limit=50):
        """
        :param limit: number of results to return. max is 50.
        :return json_results: a mess of json right now...in a dictionary.
        """
        return self._search(limit)

    def manual_header_entry(self):
        """
        Specify your own headers like a BOSS!

        (Note: spoof At your own peril. Complications abound.)
        :return: Nothing. This sets input. No type checking for max customizations.
        """
        while True:
            headr = OrderedDictWithPrepend()
            if not headr:
                api_key = raw_input('enter your api key')
                ua_str = raw_input('enter a valid User-Agent string')
                ipaddr = raw_input('enter your ip address (or leave blank to autodetect)')
                if not ipaddr:
                    ipaddr = gethostbyname(gethostname())
                headr['Ocp-Apim-Subscription-Key'] = api_key
                headr['User-Agent'] = ua_str
                headr['X-Search-ClientIP'] = ipaddr
            print '\nYour auth-key is {}\nYour User-Agent string is {}\nYour ip address will appear as {}\n\n\n\n'.format(
                headr['Ocp-Apim-Subscription-Key'], headr['User-Agent'], headr['X-Search-ClientIP'])
            response1 = raw_input(
                'To change your auth-key enter (a)\nTo change your User-Agent string enter (u)\nTo change your ip address enter (i)\n\nIf you are satisfied, press (y) to confirm, or (n) to start over.\n> :')
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
    """
    Web Search Object.
    Allows for default or manual header entry.
    Mandatory fields are 'api_key' and 'query'
    Other defaults will specify you as a firefox user, add no addtnl query params, and will give you the max of 50 results returned for your query
    Currently no support for paging, but functionality is in the works.
    """

    def __init__(self, api_key, query, safe=False, header_dict=user_constants.HEADERS,
                 addtnl_params=user_constants.INCLUDED_PARAMS):
        self.QUERY_URL = static_constants.WEBSEARCH_ENDPOINT
        self.param_dict = OrderedDictWithPrepend()

        if addtnl_params and type(addtnl_params) == OrderedDictWithPrepend:
            for key, value in addtnl_params.items():
                if value == None:
                    pass
                elif key in static_constants.BASE_QUERY_PARAMS[2:]:
                    self.param_dict[key] = addtnl_params[key]
        elif not addtnl_params:
            pass
        else:
            raise TypeError('Additional params must be in dictionary-format: {param_name : param_val}')
        ## Build header inside inherited BingSearch class.
        BingSearch.__init__(self, api_key=api_key, query=query, safe=safe, header_dict=header_dict)

        ## Run query validations
        is_ok = QueryChecker.check_web_params(self.param_dict, self.header)
        if is_ok:
            print 'Query params PASSED validation.'
        else:
            raise AttributeError('query checker has a bug')
        print 'run <instance>.search() to run query and print json returned\ncurrent URL format is {}'.format(
            self.QUERY_URL)

    def _search(self, limit, override=False, newquery=None, return_response_object=False):
        """
        Meat-&Potatoes of the search. Inserts search query and makes API call.
        :param limit: Number of return results. Max is 50
        :param override: Set to True if you intend to use 'newquery' to modify the query on the fly
        :param newquery: enter new query value if you so choose. Will not change query params.
        :return json_results: JSON returned from Microsoft.
        """
        self.param_dict.prepend('q', self._insert_web_search_query(override=override, newquery=newquery))
        if limit > 50 or limit < 1:
            raise ValueError('limit must be positive integer b/w 1 and 50')
        elif limit != 50:
            self.param_dict['count'] = limit

        response_object = requests.get(self.QUERY_URL, params=self.param_dict, headers=self.header)

        if len(response_object.url) > 1500:
            raise ValueError('URL too long. Limit URLs to < 1,200 chars.')

        response_validated = ResponseChecker.validate_request_response(response_object)
        if response_validated == '429':
            response_object = self.handle_429_error(url=response_object.url)
        else:
            pass

        if 'textFormat' in self.param_dict.keys():
            if self.param_dict['textFormat'].upper() == 'HTML':
                response_data = response_object.text()
            else:
                response_data = response_object.json()
        else:
            response_data = response_object.json()

        if return_response_object:
            return response_object
        else:
            return response_data


        # return response_data
        # packaged_results = [WebResult(single_result_json) for single_result_json in json_results['d']['results']]
        # self.current_offset += min(50, limit, len(packaged_results))
        # return packaged_results

    def handle_429_error(self, url):
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
        """
        Basic encoding & insertion of search terms. Allows for override via method described in _search() above.
        :param override: Set to True if you intend to use 'newquery' to modify the query on the fly
        :param newquery: enter new query value if you so choose. Will not change query params.
        :return finalized URL: Upon completion of this function, the URL used to call the API will be complete.
        """
        if override:
            return newquery
        else:
            return self.query


class WebResult(object):
    '''

    !!!!!!COPIED DIRECTLY FROM PY-BING-SEARCH.!!!!!!!!
    !!!!!!CURRENTLY NOT HOOKED UP TO JSON RESULTS!!!!!

    The class represents a SINGLE search cc_result.
    Each cc_result will come with the following:
    #For the actual results#
    title: title of the cc_result
    url: the url of the cc_result
    description: description for the cc_result
    id: bing id for the page
    #Meta info#:
    meta.uri: the search uri for bing
    meta.type: for the most part WebResult

    !!!!!!COPIED DIRECTLY FROM PY-BING-SEARCH.!!!!!!!!
    !!!!!!CURRENTLY NOT HOOKED UP TO JSON RESULTS!!!!!

    '''

    class _Meta(object):
        '''
        Holds the meta info for the cc_result.
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