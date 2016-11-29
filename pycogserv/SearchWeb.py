from socket import gethostname, gethostbyname
from time import sleep

import requests
from pycogserv.constants import user_constants, static_constants
from pycogserv.utils.dict_mod import OrderedDictWithPrepend
from pycogserv.utils.validations import QueryChecker, ResponseChecker
# import pdb

## TODO: Update README.md to reflect ref subpackage
## TODO: Add Alt-Endpoint functionality (news, images, etc...)
## TODO: Add autopaging support in BingSearch.search()

"""
Massive swaths of this v5 API interface were graciously stolen from py-bing-search
you can find it here: https://github.com/tristantao/py-bing-search

Modify query params in class 'constants.'
    - You can create your own own query-param-dict as a replacement, but use OrderedDict. 'query_plaintext' must be the first _key at runtime.
    - Dict entries of format "YourDict[_key] == None" will be ignored and can therefore be safely included.



TODO:
    - Add image/news/video classes w/ support for API-specific querying
        --Base Endpoint URLs for these are partially built in class "constants"
    - Update Readme to reflect ref subpackage.
"""


class BingSearch(object):
    """
    Base-Class to elimnate redundancy for the common functionalities that cut across APIs
    """

    def __init__(self, api_key, query, safe=False, header_dict=user_constants.HEADERS):
        self.api_key = api_key
        self.safe = safe
        self.query = query
        self.header_template = header_dict.copy()
        # Paging-support
        self.current_offset = 0
        self.total_estimated_matches = None
        self.last_url_sent = None
        # Cache last response
        self.last_response = None
        self.last_response_packaged = None
        # Flags to indicate state.
        self._instance_has_called_requests = False
        self._instance_shows_last_response_was_paged = False
        self._reuse_header_vals = False
        self._reuse_query_params = False

        # Build the header.
        self.build_header(header_dict=header_dict, api_key=api_key)

    def build_header(self, header_dict, api_key):
        # Generates or keeps existing header.
        # Handle prepend issue when user_constants.HEADERS['Ocp-Apim-Subscription-Key'] already has a value.
        if self.header and self._reuse_header_vals:
            pass
        elif header_dict is user_constants.HEADERS:
            self.header = header_dict
            if 'Ocp-Apim-Subscription-Key' in self.header.keys():
                if self.header['Ocp-Apim-Subscription-Key'] == api_key:
                    pass
                elif self.header['Ocp-Apim-Subscription-Key']:
                    print(
                    'Change in API-_key detected. Please remember that switching API keys at runtime is not advised.')
                    del self.header['Ocp-Apim-Subscription-Key']
            else:
                self.header.prepend('Ocp-Apim-Subscription-Key', api_key)
            for key in self.header.keys():
                if self.header[key] == None:
                    ## TODO: make self.header handle/ignore NoneType entries.
                    del self.header[key]
        else:
            self.header = self.manual_header_entry()

    def search(self, count_param=50, enable_auto_paging=False, **kwargs):
        """
        :param count_param: Number of JSON results you want the API to return. count_param will be lovingly referred to as 'limit' in henceforth c0de. Max value alowed by MS is 50.
        :return packaged_json(default) OR raw_html OR NoneType: 'packaged_json' is a list of WebResult objects (aka Smallz.)
                                                                Set user_constants.INCLUDED_PARAMS['textFormat'] to = 'HTML' to get raw html returned.
                                                                Request timeout returns nothing but doesn't raise any errors.
        """
        self._reuse_header_vals = True
        if enable_auto_paging:
            self._reuse_query_params = True
        return self._search(limit=50, **kwargs)

    def clear_headers(self):
        self._reuse_header_vals = False
        self.build_header(header_dict=self.header_template.copy(), api_key=self.api_key)


    def manual_header_entry(self):
        """
        Specify your own headers like a BOSS!

        (Note: spoof At your own peril. Complications abound.)
        :return: Nothing. This sets input. No type checking for max customizations.
        """
        while True:
            headr = OrderedDictWithPrepend()
            if not headr:
                api_key = eval(input('enter your api _key'))
                ua_str = eval(input('enter a valid User-Agent string'))
                ipaddr = eval(input('enter your ip address (or leave blank to autodetect)'))
                if not ipaddr:
                    ipaddr = gethostbyname(gethostname())
                headr['Ocp-Apim-Subscription-Key'] = api_key
                headr['User-Agent'] = ua_str
                headr['X-Search-ClientIP'] = ipaddr
            print(('\nYour auth-_key is {}\nYour User-Agent string is {}\nYour ip address will appear as {}\n\n\n\n'.format(
                headr['Ocp-Apim-Subscription-Key'], headr['User-Agent'], headr['X-Search-ClientIP'])))
            response1 = eval(input(
                'To change your auth-_key enter (a)\nTo change your User-Agent string enter (u)\nTo change your ip address enter (i)\n\nIf you are satisfied, press (y) to confirm, or (n) to start over.\n> :'))
            if response1.lower() == 'y':
                return headr
            elif response1.lower() == 'n':
                del headr
                continue
            elif response1.lower() == 'a':
                headr['Ocp-Apim-Subscription-Key'] = eval(input('enter your api _key'))
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
        self._BASE_URL = static_constants._WEBSEARCH_ENDPOINT
        self.param_dict = OrderedDictWithPrepend()
        if addtnl_params and type(addtnl_params) == OrderedDictWithPrepend:
            for key, value in list(addtnl_params.items()):
                if key in static_constants._BASE_QUERY_PARAMS[2:]:
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
        print(('run <instance>.search() to run query and print json returned\ncurrent URL format is:\n {}'.format(
            self.predict_url())))

    def __repr__(self):
        return "BingWebSearch objec with query-string = {}".format(self.query)

    def predict_url(self, websearch_only=True):
        param_dict_copy = self.param_dict.copy()
        if self.query:
            param_dict_copy.prepend('query_plaintext', self.query)
        else: param_dict_copy.prepend('query_plaintext', 'YOUR QUERY STRING GOES HERE')
        if websearch_only == True:
            param_dict_copy['responseFilter'] = 'Webpages'
        for key in param_dict_copy.keys():
            if param_dict_copy[key] == None:
                del param_dict_copy[key]
        return self._BASE_URL + requests.models.urlencode(param_dict_copy)



    def _search(self, limit, override=False, newquery=None):
        """
        Meat-&Potatoes of the search. Inserts search query and makes API call.
        :param limit: Number of return results. Max is 50
        :param override: Set to True if you intend to use 'newquery' to modify the query on the fly
        :param newquery: enter new query value if you so choose. Will not change query params.
        :return json_results: list of packaged JSON results returned from Microsoft.
        see WebResult class below.
        """
        #####################################################
        # Finalize websearch URL build.
        #
        # Note: If specified using both override=True and newquery='some random query str...',
        #       _search() can reinit a new query to restart paging at runtime.
        self._load_q_param_or_pass(override=override, newquery=newquery)
        self._load_websearch_specific_and_paging_params(limit=limit)

        #####################################################
        # Query the API. Receive response object.
        # Return NoneType if server-side timeout
        try:
            ##############################
            #           BEHOLD!          #
            response_object = requests.get(self._BASE_URL, params=self.param_dict, headers=self.header)
            ##############################

            self._instance_has_called_requests = True
        except requests.Timeout:
            print('requests module timed out. Returning NoneType')
            return None

        #####################################################
        # Handle error-codes and Warn about potential garbage results if query URL is too long.
        if len(response_object.url) > 1300:
            print('WARNING: URL too long at {} characters.\n Bing can silently truncate your query.\n Limit URLs to < 1,200 chars.').format(len(response_object.url))
        response_validated = ResponseChecker.validate_request_response(response_object)
        if response_validated == '429':
            response_object = self._handle_429_error(url=response_object.url)
        else:
            pass

        #####################################################
        # Return packaged JSON or Raw HTML.
        #
        # Updates: 'self.current_offset'
        #          'self.last_response'
        #          'self.last_response_packaged'
        self.last_response = response_object
        self.last_url_sent = response_object.url
        if 'textFormat' in list(self.param_dict.keys()) and self.param_dict['textFormat']:
            if self.param_dict['textFormat'].upper() == 'HTML':
                self.current_offset += min(50, limit)
                print('returning HTML w/o packaging. <instance>.last_response_packaged will remain set to None.')
                # Declaring raw_html explicitly for clarity.
                raw_html = response_object.text
                return raw_html
        else:
            packaged_json = self._parse_json(response_object.json())
            self.last_response_packaged = packaged_json
            self.current_offset += min(50, limit, len(packaged_json))
            return packaged_json

    def _load_q_param_or_pass(self, override, newquery):
        if override and newquery:
            self._reinit_query_and_paging(newquery=newquery)
        elif override and not newquery:
            raise AssertionError('query override has been activated but you have not specified a new query.')

        # Modify some variable/nonvariable params to enable paging and restrict query to webpages.
        if 'query_plaintext' in list(self.param_dict.keys()):
            if not override:
                pass
            elif override == True:
                del self.param_dict['query_plaintext']
                self.param_dict.prepend('query_plaintext', self._insert_web_search_query(override=override, newquery=newquery))
            else:
                raise TypeError('override arg is type bool.')

        else:
            self.param_dict.prepend('query_plaintext', self._insert_web_search_query())

    def _reinit_query_and_paging(self, newquery):
        self.query = newquery
        self.current_offset = 0
        self.total_estimated_matches = None

    def _insert_web_search_query(self, override=False, newquery=None):
        if override:
            return newquery
        else:
            return self.query


    def _load_websearch_specific_and_paging_params(self, limit=50):
        self.param_dict['offset'] = self.current_offset
        self.param_dict['responseFilter'] = 'Webpages'

        try:
            if self.param_dict['count'] and type(int(self.param_dict['count'])) == int:
                # Means condition already satisfied. Quietly pass by returning NoneType.
                return None
        except ValueError:
            print("'count' value specified is not convertible to type int.")
            print("'count' param will now default to 50")

        if limit > 50 or limit < 1:
            raise ValueError('limit must be positive integer b/w 1 and 50')
        else:
            self.param_dict['count'] = str(limit)

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
                raise IOError(static_constants._ERROR_CODES['429'])
        return r2

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



class WebResult(object):
    '''
    Attributes which can be called from WebResult instance(aka WebResults instance aka WRi) --

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

class Bingy(BingWebSearch):
    """
    'Legacy' support. BingWebSearch objects are now called "BingWebSearch"s. They're part of BingWebSearch/WebResult.
    Hilarious, I know.
    """
    def __init__(self, api_key, query, safe=False, header_dict=user_constants.HEADERS,
                 addtnl_params=user_constants.INCLUDED_PARAMS):
        BingWebSearch.__init__(api_key=api_key, query=query, safe=safe, header_dict=header_dict, addtnl_params=addtnl_params)

class Smallz(WebResult):
    """
    'Legacy' support. WebResult objects are now called "WebResult"s. They're part of BingWebSearch/WebResult.
    It's a knee-slapper dammit; so get ta' slappin.
    """
    def __init__(self, result):
        WebResult.__init__(self, result=result)
