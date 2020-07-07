import matplotlib.pyplot as plt
import pandas as pd

path = "/home/subo/PycharmProjects/webscrap_tekstowo/"
df = pd.read_csv(path + "all_data_clean.csv")


def plot_languages(column):

    lang_column = pd.Series(df[column])
    lang_counts = lang_column.value_counts(normalize=True).to_dict()
    names = list(lang_counts.keys())
    values = list(lang_counts.values())
    # plot categorical variables for a passed column:
    fig, axs = plt.subplots()
    axs.bar(names, values)
    fig.suptitle("Song " + column)
    plt.show()
    return names, values


song = plot_languages("language")
translation = plot_languages("language_translation")
