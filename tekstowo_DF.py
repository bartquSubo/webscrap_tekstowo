import pandas as pd
import glob, os
from langdetect import detect

# available columns:
# ['song_text', 'translation_text', 'song_title', 'artist_name', 'song_url']

path = "/home/subo/PycharmProjects/webscrap_tekstowo/raw_data"
all_csv = glob.glob(os.path.join(path, "*.csv"))

# converting html tags "<p> \n</p>" to NaN:
missing_values = ["<p> \n</p>"]
concatenated_df = pd.concat((pd.read_csv(f, na_values=missing_values) for f in all_csv), ignore_index=True)

# convert to another DF, not Series (mind the difference between [] and [[]]):
song_text = concatenated_df["song_text"]\
    .str.findall("\w.*")

# NEEDED TO DETECT LANGUAGE OF EACH SONG. ONCE USED = COMMENTED
detected_lang = []
for text in song_text:
    # removing Poznaj historię zmian tego tekstu </p> from each cell
    # & create back full text of a song:
    joined = " ".join(text[0:][:-2])

    # detect language for each song:
    try:
        detection = detect(joined)
    except:
        print("No language detected!")
    else:
        detected_lang.append((detection, joined))

# create a dataFrame of each song
lang_detect = pd.DataFrame(detected_lang, columns=["language", "song_text"])
print(lang_detect.head(20))
lang_detect.to_csv("detected_lang1.csv", index=True)
print("song_text_language.csv saved")






