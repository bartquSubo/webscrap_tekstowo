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

# add ids for each row
df["ids"] = range(1, len(df) + 1)

# get only rows with translation text with their ids from the general DF:
# df_notnumll_translations = df[df['translation_text'].notnull()]
# df_translation = (df_notnumll_translations[["translation_text", "ids"]])

# need to save df_translation and change manually 2 cells as they were still empty:
# df_translation.to_csv("temp_translation.csv")
df_translation = pd.read_csv(path + "temp_translation.csv")

# detect language of translation
detected_lang = []
for text in df_translation["translation_text"]:
    try:
        if None:
            detection = "no_lang"
        else:
            detection = detect(text)
    except:
        print("no lang detected for :\n{}".format(text))
    else:
        detected_lang.append(detection)

lang_detect = pd.DataFrame(detected_lang, columns=["language_translation"])
concatenated = pd.concat([df_translation, lang_detect], axis=1, sort=False)
# print(concatenated.info())
# print(concatenated.tail(20))

# lang_detect.to_csv("translation_text_language.csv", index=True)
# print("translation_text_language.csv saved")

merged_df = pd.merge(df, concatenated["language_translation"], on='ids')
print(merged_df.info())
print(merged_df.tail(50))

'''
df = df[df['song_text'].notnull() & (df['language'] == "pl")]
# print a specific call by index:
# print(df.iloc[18]["song_text"])
'''