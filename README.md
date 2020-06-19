# webscrap_tekstowo
A project to create an automatic song lyrics generator.

Training data obtained from www.tekstowo.pl (webscrapping)

Contains:
  - webscrap.py - a script for webscrapping song data from a website www.tekstowo.pl that converts the data into a Pandas DataFramework.
  Used libs: BeautifulSoup, requests, pandas.
  
  - detect_song_lang.py - a script to initially clean the data frame and to detect the language of each song.
  Used libs: pandas, langdetect
  
  - DF_clean.py -  a script for further (and better) cleaning of the data frame and to detect the language of each song translation.
  Used libs: pandas, langdetect
