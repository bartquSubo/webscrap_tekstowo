import pandas as pd

path = "/home/subo/PycharmProjects/webscrap_tekstowo/"
df = pd.read_csv(path + "all_data.csv")

# cleaning html tags, empty lines and unnecessary text
df["song_text"] = df["song_text"].str.replace(r"^(\s)*", "")
df["song_text"] = df["song_text"].str.replace(r"(\s)*Poznaj historię zmian tego tekstu((.|\n)*)", "")
df["translation_text"] = df["translation_text"].str.replace(r"<p>", "")
df["translation_text"] = df["translation_text"].str.replace(r"(\s)*Tłumaczenie:((.|\n)*)", "")
df["translation_text"] = df["translation_text"].str.replace(r"(\s)*Poznaj historię zmian tego tłumaczenia((.|\n)*)", "")

# print(df["translation_text"].head(20))
# print a specific call by index:
print(df.iloc[18]["song_text"])
