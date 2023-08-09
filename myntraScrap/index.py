from bs4 import BeautifulSoup
import requests
from itertools import cycle

# Get a list of proxies
def get_proxies():
    url = "https://sslproxies.org/"
    response = requests.get(url)
    parser = BeautifulSoup(response.text, 'html.parser')
    proxies = set()
    for i in parser.table.tbody.find_all('tr'):
        proxies.add(i.find_all('td')[0].string + ':' + i.find_all('td')[1].string)
    return proxies

# Make the request over a proxy
def proxy_request(request_type, url, **kwargs):
    while 1:
        try:
            proxy = next(proxy_pool)
            print("Using proxy: {}".format(proxy))
            response = requests.request(request_type, url, proxies={"http": proxy, "https": proxy}, **kwargs)
            break
        except (Error) :
            print("Skipping. Connnection error")
    return response

proxies = get_proxies()
proxy_pool = cycle(proxies)

url = 'https://www.myntra.com'  # replace with the URL you want to scrape
response = proxy_request('get', url)

soup = BeautifulSoup(response.text, 'html.parser')
# do something with the soup...
