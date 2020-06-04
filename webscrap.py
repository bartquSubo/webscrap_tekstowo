import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from time import sleep
import random
from random import randint
import logging
from itertools import cycle
from lxml.html import fromstring
# for entire alphabet:
import string


# error logging configuration
logging.basicConfig(filename='/home/subo/PycharmProjects/webscrap_tekstowo/errors.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

# records = crawled and appended data
records = []
alphabet = ['G', 'H']
# alphabet = list(string.ascii_uppercase)


def get_proxies():
    """
    get a free proxy list and randomize it
    :return: lst of proxy addresses
    """

    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def clean_list(clean_soup):
    """
    Get a tag tree and convert it to a soup object.
    Get a list of artists/titles and remove initial digits (1., 2., etc.)
    Clean EOL \n.
    Remove
    :param clean_soup:
    :return:
    """

    # treat the parsed tag as html
    soup_clean = BeautifulSoup(clean_soup.text, "lxml")
    # convert the content tag to lowercase str
    str_clean = str(soup_clean).lower()
    # search only for items that start with digits followed by a dot and text till \n:
    pattern = r"(\d+\. \w.+\n)"
    data_clean = re.findall(pattern, str_clean)
    # remove eof \n from the list items:
    list_clean = list(map(lambda it: it.strip(), data_clean))
    return list_clean


def normalize_list(clean_string):
    """
    Function to normalize scraped text (artists and song titles) so that it can be used as input for web address.
    :param clean_string: str
    :return: str; clean_trailing_under
    """

    clean_str = re.sub(r"\(\d+ utworów\)", "", clean_string)
    clean_str = clean_str.replace("&amp;", "__")
    clean_punctuation = re.sub(r"[^\w\s]", "_", clean_str)
    clean_punctuation = clean_punctuation.replace(" ", "_")
    clean_repetitions = re.sub(r"_{3,}", "_", clean_punctuation)
    clean_trailing_under = re.sub(r"_+$", "", clean_repetitions)
    return clean_trailing_under


def soup_url(request_url, tag, tag_class, tag_element):
    """
    Function to request.get a URL and convert it to a BeautifulSoup object.
    :param request_url: str
    :param tag: str
    :param tag_class: str
    :param tag_element: str
    :return: str; tags
    """

    for user_agent in range(1, 10):
        # use proxy addresses:
        proxy = next(proxy_pool)
        proxies = {"http://": proxy, "https://": proxy}
        # use various user_Agent headers
        user_agent = random.choice(user_agent_list)
        s = requests.Session()
        s.max_redirects = 60
        s.headers['User-Agent'] = user_agent
        # headers = {"User-Agent": user_agent}
        r = s.get(request_url, proxies=proxies, headers=s.headers, allow_redirects=3)
        # to get Polish diacritics correctly written:
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'lxml')
        # get the specific tag: element
        found = soup.find(tag, {tag_class: tag_element})
        return found


def soup_song(song, tag):
    """
    needed for song page. create a BS4 object and perform action on it
    :param song:
    :param tag:
    :return:
    """

    soup = BeautifulSoup(song.text, 'lxml')
    # get the specific tag: element
    found = soup.find(tag)
    song_str = str(found)
    clean_leading_text = re.sub(r"<p>Tekst piosenki:", "", song_str)
    clean_trailing_text = re.sub(r"Poznaj historię zmian tego tekstu \n\n</p>", "", clean_leading_text)
    return clean_trailing_text


# proxy list + random address selection:
proxies = get_proxies()
proxy_pool = cycle(proxies)

# headers for user_agent in "def soup_url":
user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

# loop through alphabet list
for letter in alphabet:
    general_url = 'https://www.tekstowo.pl/artysci_na,' + letter

    # loop through number of sub-pages to scrap:
    for i in range(1, 6):
        url_page = general_url + ',strona,' + str(i) + '.html'
        artists_tag = soup_url(url_page, "div", "class", "content")
        # loop through artist pages
        for x in clean_list(artists_tag):
            artist_remove_initial = re.sub(r"\d+\. ", "", x)
            artist_name = normalize_list(artist_remove_initial)

            # create artists urls
            artist_url = 'https://www.tekstowo.pl/piosenki_artysty,' + artist_name + '.html'
            songs_tag = soup_url(artist_url, "div", "class", "ranking-lista")

            # loop through songs pages:
            for y in clean_list(songs_tag):
                song_remove_initial = re.sub(r"\d+\. \w.* - ", "", y)
                song_title = normalize_list(song_remove_initial)
                song_url = 'https://www.tekstowo.pl/piosenka,' + artist_name + ',' + song_title + '.html'
                text_tag = soup_url(song_url, "div", "class", "song-text")
                # handle errors:
                try:
                    song_text = soup_song(text_tag, "p")
                    translation_tag = soup_url(song_url, "div", "id", "translation")
                    translation_text = soup_song(translation_tag, "p")
                except AttributeError as err:
                    # log all errors:
                    logger.error(err)
                    print("AttributeError:NoneType error for " + song_url)
                else:
                    # append all data
                    records.append((song_text, translation_text, song_title, artist_name, song_url))
                    print(song_url)
                    # set scrapping pace:
                    sleep(randint(2, 9))

######################
# save the crawled data to a DataFrame:
df = pd.DataFrame(records, columns=['song_text', 'translation_text', 'song_title', 'artist_name', 'song_url'])
df.to_csv('tekstowo_dataGH1-5.csv', index=False, encoding='utf-8')

print('Data has been saved.')
