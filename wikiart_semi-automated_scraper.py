""""

A semi-automated scraper to retrieve paintings from a particular
web-page reffering to an artist from wikiart.org 

We notice that this scraper does not provide access to all the paintings of a painter listed in wikiart.org

This programm was formed exclusively for academical needs. This

If used, a proper citation must be given to the authors of this work.

Deep Learning applied in artworks: Sentiment analysis, Art Genre Classification, Art Dataset, 2022. 
A. Gavros, S. Demetriadis, A. Tefas.

"""

# importing libraries

import pandas as pd
import numpy as np
import requests
import os


# setting the necessary filepaths and opening the files that contain the name of the paintings to be retrieved

name_artist = "Artist Name"
path = str(os.getcwd()) + "/"

data_1 = pd.read_excel(path + "excel_file.xlsx", engine="openpyxl")

# some text manipulation in order to get a working url

data_1["Name"] = data_1["Name"].replace([" - "], " ", regex=True)
data_1["Name"] = data_1["Name"].replace(["à "], "", regex=True)
data_1["Name"] = data_1["Name"].replace(["à"], "", regex=True)
data_1["Name"] = data_1["Name"].replace(["è"], "-", regex=True)
data_1["Name"] = data_1["Name"].replace(["é"], "-", regex=True)
data_1["Name"] = data_1["Name"].replace([" "], "-", regex=True)
data_1["Name"] = data_1["Name"].replace(["'"], "", regex=True)
data_1["Name"] = data_1["Name"].replace(r'["]', "", regex=True)
data_1["Name"] = data_1["Name"].replace(r"[()]", "", regex=True)
data_1["Name"] = data_1["Name"].str.lower()

# editing the filenames in a form to be passed to the scraper

for i in range(0, len(data_1["Name"])):
    if (data_1["Name"][i][-3:]).isdigit():
        data_1["Name"][i] = data_1["Name"][i].replace(",", "")
    #        print(data_1['Name'][i])
    elif data_1["Name"][i][-1:] == "?":
        data_1["Name"][i] = data_1["Name"][i].replace(",", "")
        data_1["Name"][i] = data_1["Name"][i].replace("-?", "")
    #        print(data_1['Name'][i])
    else:
        continue

# passing the edited filenames to a list

df_duplicated = data_1[data_1["Name"].duplicated() == True]
df_duplicated.reset_index(drop=True, inplace=True)
df_droped = df_duplicated.drop_duplicates()
duplicate_list = df_droped["Name"].tolist()

# handling duplicate values

df_changed = pd.DataFrame(columns=["Name"])

for k in range(0, len(duplicate_list)):
    df_temp = df_duplicated.loc[df_duplicated["Name"] == str(duplicate_list[k])]
    df_temp.reset_index(drop=True, inplace=True)
    for z in range(0, len(df_temp["Name"])):
        number = z + 1
        df_temp["Name"][z] = str(df_temp["Name"][z]) + "-" + str(number)
    df_changed = df_changed.append(df_temp)

df_changed.reset_index(drop=True, inplace=True)

data_1.drop_duplicates(subset="Name", keep="first", inplace=True)

data_1 = data_1.append(df_changed)
data_1.reset_index(drop=True, inplace=True)

# opening of the formed urls #
# checking if the url exists #
# downloading the painting to our filepath #

starting_url = "https://uploads8.wikiart.org/images/"
name_artist = name_artist.lower()
name_artist = name_artist.replace(" ", "-")
starting_url = starting_url + name_artist + "/"

for i in range(0, len(data_1["Name"])):
    string_first = str(data_1["Name"][i])
    image_url = starting_url + string_first + ".jpg"
    response = requests.get(image_url)
    if response.status_code == 200:
        continue
    else:
        image_url = image_url.replace(".jpg", "")
        image_url = image_url[: (len(image_url) - 5)]
        image_url = image_url + ".jpg!Large.jpg"
        print(image_url)
    img_data = requests.get(image_url).content
    with open(path + str(data_1["Name"][i]) + ".jpg", "wb") as handler:
        handler.write(img_data)

# end of program #

