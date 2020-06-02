import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import string

records = []
# alphabet = ['B']
alphabet = list(string.ascii_uppercase)


def get_general_urls():
    for letter in alphabet:
        general_url = 'https://www.tekstowo.pl/artysci_na,' + letter
        # number of sub-pages to scrap:
        for i in range(1, 10):
            url_page = general_url + ',strona,' + str(i) + '.html'
            # print(url_page)
            return url_page


def get_specific_url(imported_tag, regex_pattern):
    for x in clean_list(imported_tag):
        remove_leading = re.sub(regex_pattern, "", x)
        text = normalize_list(remove_leading)
        return text


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
    :param div_tag: str
    :param class_tag: str
    :param element_tag: str
    :return: str; tags
    """
    r = requests.get(request_url)
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

################################################################
'''
for letter in alphabet:
    general_url = 'https://www.tekstowo.pl/artysci_na,' + letter
    # number of sub-pages to scrap:
    for i in range(1, 2):
        url_page = general_url + ',strona,' + str(i) + '.html'
        '''

# get artist URLs
artists_tag = soup_url(get_general_urls(), "div", "class", "content")
artist_name = get_specific_url(artists_tag, r"\d+\. ")
artist_url = 'https://www.tekstowo.pl/piosenki_artysty,' + artist_name + '.html'

# get song URLs
songs_tag = soup_url(artist_url, "div", "class", "ranking-lista")
song_title = get_specific_url(songs_tag, r"\d+\. \w.* - ")
song_url = 'https://www.tekstowo.pl/piosenka,' + artist_name + ',' + song_title + '.html'

# def text_translation():

# get song text and translation
song_tag = soup_url(song_url, "div", "class", "song-text")
song_text = soup_song(song_tag, "p")

translation_tag = soup_url(song_url, "div", "id", "translation")
translation_text = soup_song(translation_tag, "p")
print(song_url)
################################################################
'''
for x in clean_list(artists_tag):
    artist_remove_initial = re.sub(r"\d+\. ", "", x)
    artist_name = normalize_list(artist_remove_initial)
    # create artists urls
    '''

'''
for y in clean_list(songs_tag):
    song_remove_initial = re.sub(r"\d+\. \w.* - ", "", y)
    song_title = normalize_list(song_remove_initial)

    song_url = 'https://www.tekstowo.pl/piosenka,' + artist_name + ',' + song_title + '.html'
    
text_tag = soup_url(song_url, "div", "class", "song-text")
song_text = soup_song(text_tag, "p")
translation_tag = soup_url(song_url, "div", "id", "translation")
translation_text = soup_song(translation_tag, "p")
'''
# get both, translation and songtext:
# both = soup_url(song_url, "div", "class", "tekst")

# append collected data
# records.append((song_text, translation_text, song_title, artist_name, song_url))
# print(song_url)
# print(artist_name)
# print(song_title)
# print(translation_text)
# print(song_text)

# needed for scrap pace:
sleep(randint(2, 10))

################################################################

# create a data frame
# df = pd.DataFrame(records, columns=['song_text', 'translation_text', 'song_title', 'artist_name', 'song_url'])
# df.to_csv('tekstowo_data.csv', index=False, encoding='utf-8')

# print('Data has been saved.')


# def get_urls():
#     for letter in alphabet:
#         url = 'https://www.tekstowo.pl/artysci_na,' + letter
#         for i in range(1, 201):
#             url_page = url + ',strona,' + str(i) + '.html'
#             # print(url_page)
#             return url
# get_urls()

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
