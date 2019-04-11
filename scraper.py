from  bs4 import BeautifulSoup
import html.parser
import requests
import re
#for url validation
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

#master list of urls
linklist = dict()

def soupify (page):
    """function takes in webpage returns all links"""
    soup = BeautifulSoup(page, 'html.parser')
    links=[]
    for a in soup.find_all('a', href=True):
        print(a['href'])
        if re.match(regex, a['href']):
            links.append(a['href'])
    return links

def pagegetter (url):
    """takes in url returns webpage""" 
    response= requests.get(url)
    print(response)
    return response.text

def linkmanager (arr):
    """takes in an array of links and adds to master link list"""
    for link in arr:
        if linklist.get(link)==None:
            linklist[link]={'visited':False}
    
#gets espn.com
current_page=pagegetter("http://espn.com")
#gets all validated links from espn.com
returned_links = soupify(current_page)
#adds links to master list
linkmanager (returned_links)
#visits each link from main page
for link in (returned_links):
    page = pagegetter (link)
    returned_links =soupify(page)
    linkmanager (returned_links)

print ("Done")