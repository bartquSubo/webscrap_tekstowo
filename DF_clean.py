import pandas as pd
from langdetect import detect

path = "/home/subo/PycharmProjects/webscrap_tekstowo/"
df = pd.read_csv(path + "all_data.csv")

# cleaning html tags, empty lines and unnecessary text
df["song_text"] = df["song_text"].str.replace(r"^(\s)*", "")
df["song_text"] = df["song_text"].str.replace(r"(\s)*Poznaj historię zmian tego tekstu((.|\n)*)", "")
df["translation_text"] = df["translation_text"].str.replace(r"<p>", "")
df["translation_text"] = df["translation_text"].str.replace(r"(\s)*Tłumaczenie:((.|\n)*)", "")
df["translation_text"] = df["translation_text"].str.replace(r"(\s)*Poznaj historię zmian tego tłumaczenia((.|\n)*)", "")

df_translation = df["translation_text"]

# detect language of translation
detected_lang = []
for text in df_translation:
    song_url = df["song_url"]
    try:
        detection = detect(text)
    except:
        detection = "no_lang"
    else:
        detected_lang.append((detection, song_url))

lang_detect = pd.DataFrame(detected_lang, columns=["language_translation", "song_url"])
print(lang_detect.tail(20))
lang_detect.to_csv("translation_text_language.csv", index=True)
print("translation_text_language.csv saved")

'''
df = df[df['song_text'].notnull() & (df['language'] == "pl")]
translation = df[df['translation_text'].notnull()]
# print(df["song_text"])
print(translation["translation_text"])
# print a specific call by index:
# print(df.iloc[18]["song_text"])
'''