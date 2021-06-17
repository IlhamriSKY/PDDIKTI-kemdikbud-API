from pprint import pprint as p
from src.api import api
from src.helper import helper

h = helper()
a = api()

#p (h.withversion())

p (a.search_all('Soegijapranata'))
