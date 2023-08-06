import requests
from lxml import html

def findxpath(x,y):
    page = requests.get(x)
    root = html.fromstring(page.text)
    tree = root.getroottree()
    result = root.xpath('//*[. = "{}"]'.format(y))
    L = []
    for r in result:
        L.append(tree.getpath(r))
    if len(L) == 1:
        return(L[0])
    if len(L) == 0:
        return("")
    if len(L) > 1:
        return(L)