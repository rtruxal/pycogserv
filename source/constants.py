from _socket import gethostbyname, gethostname
from collections import OrderedDict

from fake_useragent import UserAgent as UA


class user_constants():
    """
    This class gives access to the default headers and query-modifiers used when a
    BingWebSearch object is instantiated.

    Change the 'None' values to fit your use-case.
    Any value maked 'None' will be ignored. ANY & ALL other values will not be ignored.

    Also, DON'T CHANGE THE DICTIONARY KEYS!!!!!! They're defined by Microsoft.

    These values can also all be accessed and changed on the fly from the REPL.
    """
    ###############################################
    ##              DON'T TOUCH                  ##
    ###############################################
    user_agent = UA()
    HEADERS = OrderedDict()
    INCLUDED_PARAMS = OrderedDict()

    ###############################################
    ## Enter default-header customizations here. ##
    ###############################################
    HEADERS['Ocp-Apim-Subscription-Key'] = None
    HEADERS['User-Agent'] = user_agent.firefox
    HEADERS['X-Search-ClientIP'] = gethostbyname(gethostname())
    HEADERS['X-MSEdge-ClientID'] = None
    HEADERS['Accept'] = None
    HEADERS['Accept-Language'] = None
    HEADERS['X-Search-Location'] = None

    ###############################################
    ##     Enter query customizations here.      ##
    ###############################################
    ## Web Params:
    INCLUDED_PARAMS['cc'] = None               # <--(See constants.COUNTRY_CODES below for available options)
    INCLUDED_PARAMS['count'] = None            # <--(Enter a number from 0-50. Must by type==str. EX: count of 5 should be "5")
    INCLUDED_PARAMS['freshness'] = None        # <--(Poss values are 'Day', 'Week', or 'Month')
    INCLUDED_PARAMS['mkt'] = None              # <--(See constants.MARKET_CODES below for available options)
    INCLUDED_PARAMS['offset'] = None           # <--(Use this in conjunction with totalEstimatedMatches and count to page. Same format as 'count')
    INCLUDED_PARAMS['responseFilter'] = None   # <--(Poss values are 'Computation', 'Images', 'News', 'RelatedSearches', SpellSuggestions', 'TimeZone', 'Videos', or 'Webpages')
    INCLUDED_PARAMS['safeSearch'] = None       # <--(Poss values are 'Off', 'Moderate', and 'Strict.')
    INCLUDED_PARAMS['setLang'] = None          # <--(See ISO 639-1, 2-letter language codes here: https://www.loc.gov/standards/iso639-2/php/code_list.php)
    INCLUDED_PARAMS['textDecorations'] = None  # <--(Case-insensitive boolean. '(t|T)rue', or '(f|F)alse')
    INCLUDED_PARAMS['textFormat'] = None       # <--(Poss values are 'Raw', and 'HTML.' Default is 'Raw' if left blank.)


class static_constants():
    """
    These are both for reference and are used extensively in _methods()

    So don't modify them!!!!! Just lookie-lookie.
    """
    ####################################################
    ## ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !##
    ##    DO NOT modify ANY of the constants below    ##
    ## ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !##
    ####################################################

    ####################################################
    ##    BASE_QUERY_PARAMS[0] & [1] are special!     ##
    ####################################################
    BASE_QUERY_PARAMS = (
        'search?q',  # <-- if you change this to 'images/search?q' or 'news/search?q' it will change ze behavior much like repsonsefileter
        'category',  # <--news only
        'cc',
        'count',
        'freshness',
        'mkt',
        'offset',
        'responseFilter',
        'safeSearch',
        'setLang',
        'textDecorations',  # <-- bool
        'textFormat',
    )

    ####################################################
    ##    Use these in conjunction w/ the cc param    ##
    ####################################################
    COUNTRY_CODES = {
        'Australia': 'AR',
        'Austria': 'AU',
        'Belgium': 'AT',
        'Brazil': 'BE',
        'Canada': 'BR',
        'Chile': 'CA',
        'Denmark': 'CL',
        'Finland': 'DK',
        'France': 'FI',
        'Germany': 'FR',
        'Hong Kong SAR': 'DE',
        'India': 'HK',
        'Indonesia': 'IN',
        'Ireland': 'ID',
        'Italy': 'IE',
        'Japan': 'IT',
        'Korea': 'JP',
        'Malaysia': 'KR',
        'Mexico': 'MY',
        'NO': 'CN',
        'Netherlands': 'MX',
        'New Zealand': 'NL',
        'Norway': 'NZ',
        'Poland': 'PL',
        'Portugal': 'PT',
        'Republic of the Philippines': 'PH',
        'Russia': 'RU',
        'Saudi Arabia': 'SA',
        'South Africa': 'ZA',
        'Spain': 'ES',
        'Sweden': 'SE',
        'Switzerland': 'CH',
        'Taiwan': 'TW',
        'Turkey': 'TR',
        'United Kingdom': 'GB',
        'United States': 'US'
    }

    ####################################################
    ##    Use these in conjunction w/ the mkt param   ##
    ####################################################
    MARKET_CODES = {
        'Argentina-Spanish': 'es-AR',
        'Australia-English': 'en-AU',
        'Austria-German': 'de-AT',
        'Belgium-Dutch': 'nl-BE',
        'Belgium-French': 'fr-BE',
        'Brazil-Portuguese': 'pt-BR',
        'Canada-English': 'en-CA',
        'Canada-French': 'fr-CA',
        'Chile-Spanish': 'es-CL',
        'Denmark-Danish': 'da-DK',
        'Finland-Finnish': 'fi-FI',
        'France-French': 'fr-FR',
        'Germany-German': 'de-DE',
        'Hong Kong SAR-Traditional Chinese': 'zh-HK',
        'India-English': 'en-IN',
        'Indonesia-English': 'en-ID',
        'Ireland-English': 'en-IE',
        'Italy-Italian': 'it-IT',
        'Japan-Japanese': 'ja-JP',
        'Korea-Korean': 'ko-KR',
        'Malaysia-English': 'en-MY',
        'Mexico-Spanish': 'es-MX',
        'Netherlands-Dutch': 'nl-NL',
        'New Zealand-English': 'en-NZ',
        'Norway-Norwegian': 'no-NO',
        "People's republic of China-Chinese": 'zh-CN',
        'Poland-Polish': 'pl-PL',
        'Portugal-Portuguese': 'pt-PT',
        'Republic of the Philippines-English': 'en-PH',
        'Russia-Russian': 'ru-RU',
        'Saudi Arabia-Arabic': 'ar-SA',
        'South Africa-English': 'en-ZA',
        'Spain-Spanish': 'es-ES',
        'Sweden-Swedish': 'sv-SE',
        'Switzerland-French': 'fr-CH',
        'Switzerland-German': 'de-CH',
        'Taiwan-Traditional Chinese': 'zh-TW',
        'Turkey-Turkish': 'tr-TR',
        'United Kingdom-English': 'en-GB',
        'United States-English': 'en-US',
        'United States-Spanish': 'es-US'
    }

    SPECIALTY_APIS = {
        'images': 'images/',
        'images_trending': 'images/trending/',  # <-- works only for mkt= en-US, en-CA, and en-AU
        'videos': 'videos/',
        'videos_trending': 'videos/trending/',
        'videos_details': 'videos/details/',
        'news': 'news/',
        'news_trending': 'news/trendingtopics/'  # <-- works only for en-US and zh-CN
    }

    ## This is the basis for all endpoint permutations available for Bing Search APIs through Azure Cognitive Services
    BASE_ENDPOINT = 'https://api.cognitive.microsoft.com/bing/v5.0/'

    ## Commented out Endpoint URLs have special format which is not defined by .../search?q=...
    ## These are not yet supported.
    WEBSEARCH_ENDPOINT = BASE_ENDPOINT + '{}='.format(BASE_QUERY_PARAMS[0])
    IMAGESEARCH_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['images'] + '{}='.format(BASE_QUERY_PARAMS[0])
    # IMAGESEARCH_TRENDING_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['images_trending'] + ?????
    VIDEOSEARCH_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['videos'] + '{}='.format(BASE_QUERY_PARAMS[0])
    # VIDEOSEARCH_TRENDING_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['videos_trending'] + ?????
    # VIDEOSEARCH_DETAILS_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['images_details'] + ?????
    NEWSSEARCH_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['news'] + '{}='.format(BASE_QUERY_PARAMS[0])
    # NEWSSEARCH_TRENDING_ENDPOINT = BASE_ENDPOINT + SPECIALTY_APIS['news_trending'] + ?????



