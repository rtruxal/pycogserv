"""
These are for Reference! Changing them won't do anything 'cept confuse you.
"""




BASE_QUERY_PARAMS = (
    'query_plaintext',
    # <-- if you change this to 'images/search?query_plaintext' or 'news/search?query_plaintext' it will change ze behavior much like repsonsefileter
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
## For use with 'cc'
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

## For use with 'mkt'
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

## What it sounds like.
ERROR_CODES = {
        '200' : 'The call succeeded',
        '400' : 'One of the query parameters is missing or not valid',
        '401' : 'The subscription _key is missing or not valid',
        '403' : "The user is authenticated but doesn't have permission to the requested resource. Bing may also return this status if the caller exceeded their queries per month quota",
        '404' : 'Page not found: Bing should not be throwing this error. There is likely a fundamental problem with the structure of your query URL.',
        '410' : 'The request was made using HTTP. Only HTTPS is supported.(_BASE_ENDPOINT USES HTTPS. EITHER YOU CHANGED THAT OR YOU ARE NOT AT FAULT)',
        '429' : 'The user exceeded their queries per second quota',
    }
## All query URLs begin with this.
BASE_ENDPOINT = 'https://api.cognitive.microsoft.com/bing/v5.0/'

WEBSEARCH_ENDPOINT = BASE_ENDPOINT + 'search?'

## Complete list of possible endpoint URLs.
SPECIALTY_API_ENDPOINTS = {
        'images': 'https://api.cognitive.microsoft.com/bing/v5.0/images/search?',
        'images_trending': 'https://api.cognitive.microsoft.com/bing/v5.0/images/trending/search?',  # <-- works only for mkt= en-US, en-CA, and en-AU
        'videos': 'https://api.cognitive.microsoft.com/bing/v5.0/videos/search?',
        'videos_trending': 'https://api.cognitive.microsoft.com/bing/v5.0/videos/trending/search?',
        'videos_details': 'https://api.cognitive.microsoft.com/bing/v5.0/videos/details/search?',
        'news': 'https://api.cognitive.microsoft.com/bing/v5.0/news/search?',
        'news_trending': 'https://api.cognitive.microsoft.com/bing/v5.0/news/trendingtopics/search?'  # <-- works only for en-US and zh-CN
    }

