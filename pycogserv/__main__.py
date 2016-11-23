"""Command line parsing""""
from pycogserv import SearchWeb
import sys


if len(sys.argv)==1:
     print("--help for more options")
elif sys.argv[1] == '--help':
    ''' TODO: ENTER OTHER OPTIONS HERE AND WITH ELSE STATEMENT'''
    print ('enter api_key, query to start search')
else:
    search = SearchWeb.BingWebSearch(sys.argv[1],sys.argv[2]).search()
    print(search)
