from constants import static_constants


class QueryChecker():
    """
    Isolated human-error-checker class.
    All methods are static and do not modify state.
    if/else mess below forgoes optimization in favor of clarity.
    """
    @staticmethod
    def check_web_params(query_dict, header_dict):
        responseFilters = ('Computation', 'Images', 'News', 'RelatedSearches', 'SpellSuggestions', 'TimeZone', 'Videos', 'Webpages')

        if 'cc' in query_dict.keys():
            if query_dict['cc'] and not header_dict['Accept-Language']:
                raise AssertionError('Attempt to use cc_country-cc_code without specifying language.')
            if query_dict['mkt']:
                raise ReferenceError('cc and mkt cannot be specified simultaneously')
        if 'count' in query_dict.keys():
            if int(query_dict['count']) >= 51 or int(query_dict['count']) < 0:
                raise ValueError('Count specified out of range. 50 max objects returned.')
        if 'freshness' in query_dict.keys():
            if query_dict['freshness'] not in ('Day', 'Week', 'Month'):
                raise ValueError('Freshness must be == Day, Week, or Month. Assume Case-Sensitive.')
        if 'offset' in query_dict.keys():
            if int(query_dict['offset']) < 0:
                raise ValueError('Offset cannot be negative.')
        if 'responseFilter' in query_dict.keys():
            if query_dict['responseFilter'] not in responseFilters:
                raise ValueError('Improper response filter.')
        if 'safeSearch' in query_dict.keys():
            if query_dict['safeSearch'] not in ('Off', 'Moderate', 'Strict'):
                raise ValueError('safeSearch setting must be Off, Moderate, or Strict. Assume Case-Sensitive.')
            if 'X-Search-ClientIP' in query_dict.keys():
                raw_input('You have specified both an X-Search-ClientIP header and safesearch setting\nplease note: header takes precedence')
        if 'setLang' in query_dict.keys():
            if header_dict['Accept-Language']:
                raise AssertionError('Attempt to use both language header and query param.')
        if 'textDecorations' in query_dict.keys():
            if query_dict['textDecorations'].lower() not in ('true', 'false'):
                raise TypeError('textDecorations is type bool')
        if 'textFormat' in query_dict.keys():
            if query_dict['textFormat'] not in ('Raw', 'HTML'):
                raise ValueError('textFormat must be == Raw or HTML. Assume Case-Sensitive.')
        return True

class ResponseChecker():
    """
    Meant to examine returned objects and check/handle errors.
    """
    @staticmethod
    def validate_request_response(response):
        """
        Return nothing if valid response object returned.
        Otherwise handle or throw exceptions
        :param response: requests.response object.
        :return: func will pass or raise exception. That's all.
        """
        if not response.status_code == 200:
            if response.status_code == 429:
                print 'queries/second quota exceeded. this func will make 5 attempts to resend.'
                return '429'
            elif str(response.status_code) in static_constants.ERROR_CODES.keys():
                raise AssertionError(static_constants.ERROR_CODES[str(response.status_code)])
            else:
                raise ReferenceError('unknown status code returned: {}\nurl string is: {}'.format(response.status_code, response.url))
        else: return True

