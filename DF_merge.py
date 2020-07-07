import pandas as pd

path = "/home/subo/PycharmProjects/webscrap_tekstowo/"

language_detected = pd.read_csv(path + "detected_lang_song.csv")
print(language_detected)
# songs_data = pd.read_csv(path + "songs_data.csv")
# all_data = pd.concat([songs_data, language_detected], axis=1)
# all_data.to_csv("all_data.csv")
# print(all_data[["song_text", "language"]])

# print(concatenated_df.isnull().sum())
# print(concatenated_df.info())
