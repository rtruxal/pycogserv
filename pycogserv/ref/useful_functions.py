

class avoid_import_conflicts():
    import requests
    # from requests import utils
    # from pycogserv.utils.validations import QueryChecker as qc

    urlencode = {'descr' : requests.models.urlencode.__doc__ + "\n\nEx: {'query_plaintext' : 'arbitrary search query', 'responseFilter' : 'Webpages'\n--Turns into--\n'query_plaintext=arbitrary+search+query&responseFilter=Webpages'",
                 'func' : requests.models.urlencode}







# values in 'func_descriptions' are strings.
func_descriptions = {
    'urlencode' : avoid_import_conflicts.urlencode['descr']
}

# values in 'funcs' are actual functions. They can be called by appending () when making a call to the dictionary.

encode_param_dict_2_url = avoid_import_conflicts.urlencode['func']
