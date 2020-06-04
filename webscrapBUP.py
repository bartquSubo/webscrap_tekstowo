import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re
import string
from time import sleep
import random
from random import randint
import logging
from itertools import cycle
from lxml.html import fromstring


# error logging configuration
logging.basicConfig(filename='/home/subo/PycharmProjects/webscrap_tekstowo/errors.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

'''
webdriver_path = "/home/subo/PycharmProjects/IG-BOT2/chromedriver"
driver = webdriver.Chrome(webdriver_path)
driver.get("https://www.tekstowo.pl/przegladaj_teksty.html")
driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/a').click()
'''

records = []
alphabet = ['C', 'D']
# alphabet = list(string.ascii_uppercase)


# get free proxy list and randomize it:
def get_proxies():
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

    # clean_numb = re.sub(r"\d+\. ", "", clean_string)
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
        proxy = next(proxy_pool)
        proxies = {"http://": proxy, "https://": proxy}
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

    soup = BeautifulSoup(song.text, 'lxml')
    # get the specific tag: element
    found = soup.find(tag)
    song_str = str(found)
    clean_leading_text = re.sub(r"<p>Tekst piosenki:", "", song_str)
    clean_trailing_text = re.sub(r"Poznaj historię zmian tego tekstu \n\n</p>", "", clean_leading_text)
    return clean_trailing_text


proxies = get_proxies()
proxy_pool = cycle(proxies)

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

for letter in alphabet:
    general_url = 'https://www.tekstowo.pl/artysci_na,' + letter

    # number of sub-pages to scrap:
    for i in range(1, 6):
        url_page = general_url + ',strona,' + str(i) + '.html'
        artists_tag = soup_url(url_page, "div", "class", "content")
        # r = requests.get(url_page)
        # r.encoding = r.apparent_encoding
        # soup = BeautifulSoup(r.text, 'lxml')
        '''
        # get the artist list from all defined sub-pages:
        # works but super slow!
        for artist in soup.find_all("a", class_="title")[20:51]:
            print(artist.get('title'))
        # get the artist list from all defined sub-pages: super slow!
        artists = soup.find("a", href=re.compile("/piosenki_artysty,.*"))
        '''
        # get the content tag
        # artists = soup.find("div", {"class": "content"})
        '''
        soup2 = BeautifulSoup(artists.text, "lxml")
        soup_str = str(soup2).lower()
        # search only for artists in the content tag
        pattern = r"(\d+\. \w.+\n)"
        artist_data = re.findall(pattern, soup_str)
        # remove eof \n from the list items:
        artist_list = list(map(lambda it: it.strip(), artist_data))
        '''
        for x in clean_list(artists_tag):
            artist_remove_initial = re.sub(r"\d+\. ", "", x)
            artist_name = normalize_list(artist_remove_initial)
            # clean_numb = re.sub(r"\d+\. ", "", x)
            # clean_str = re.sub(r"\(\d+ utworów\)", "", clean_numb)
            # clean_str = clean_str.replace("&amp;", "__")
            # clean_punctuation = re.sub(r"[^\w\s]", "_", clean_str)
            # clean_punctuation = clean_punctuation.replace(" ", "_")
            # clean_repetitions = re.sub(r"_{3,}", "_", clean_punctuation)
            # clean_trailing_under = re.sub(r"_+$", "", clean_repetitions)
            # artist_name = clean_trailing_under

            # print(clean_trailing_under)

            # create artists urls
            artist_url = 'https://www.tekstowo.pl/piosenki_artysty,' + artist_name + '.html'
            songs_tag = soup_url(artist_url, "div", "class", "ranking-lista")
            # print(artist_name)

            for y in clean_list(songs_tag):
                song_remove_initial = re.sub(r"\d+\. \w.* - ", "", y)
                song_title = normalize_list(song_remove_initial)
                song_url = 'https://www.tekstowo.pl/piosenka,' + artist_name + ',' + song_title + '.html'
                text_tag = soup_url(song_url, "div", "class", "song-text")
                try:
                    song_text = soup_song(text_tag, "p")
                    translation_tag = soup_url(song_url, "div", "id", "translation")
                    translation_text = soup_song(translation_tag, "p")
                except (requests.exceptions.TooManyRedirects, requests.exceptions.ConnectionError, requests.TooManyRedirects, AttributeError) as attr:
                    logger.error(attr)
                    print("AttributeError:NoneType error for " + song_url)
                else:
                    # get both, translation and songtext:
                    # both = soup_url(song_url, "div", "class", "tekst")
                    records.append((song_text, translation_text, song_title, artist_name, song_url))
                    print(song_url)
                    # print(artist_name)
                    # print(song_title)
                    # print(translation_text)
                    # soup_songs = BeautifulSoup(songs.text, "lxml")
                    # songs_str = str(soup_songs).lower()
                    # songs_data = re.findall(pattern, songs_str)
                    # songs_list = list(map(lambda it: it.strip(), songs_data))

                    # print(songs_list)
                    # needed for not getting blocked on a server:
                    sleep(randint(2, 9))

df = pd.DataFrame(records, columns=['song_text', 'translation_text', 'song_title', 'artist_name', 'song_url'])
df.to_csv('tekstowo_data.csv', index=False, encoding='utf-8')

print('Data has been saved.')



# def get_urls():
#     for letter in alphabet:
#         url = 'https://www.tekstowo.pl/artysci_na,' + letter
#         for i in range(1, 201):
#             url_page = url + ',strona,' + str(i) + '.html'
#             # print(url_page)
#             return url
## get_urls()

# r = requests.get("https://www.tekstowo.pl/piosenka,action_pact,_drowning_out_the__big_jets.html")

# soup = BeautifulSoup(r.text, 'html.parser')
#
# def get_song_text():
#
#     songtext = soup.find("div", {"class":"song-text"})
#     translationtext = soup.find("div", {"id":"translation"})
#     #  get the translation and songtext:
#     both = soup.find_all("div", {"class":"tekst"})
#
#     return translationtext.text
#     # print(both.get_text())
#
# get_song_text()
