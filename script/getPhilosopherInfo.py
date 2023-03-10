import csv
import json
import re
import urllib.request


def get_philosopher_info(philosopher_name):
    query_url = f"https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=info|pageimages|extracts&exintro&generator=allpages&inprop=url&gaplimit=1&gapfrom={urllib.parse.quote(philosopher_name)}"
    try:
        wikipedia_response = urllib.request.urlopen(query_url)
        wikipedia_response_txt = wikipedia_response.read().decode("utf-8")
        json_data = json.loads(wikipedia_response_txt)
        json_list = list(json_data["query"].values())[0]
        json_list2 = list(json_list.values())[0]
        if "thumbnail" in json_list2:
            img_link = re.sub(
                "/50px.*",
                "",
                json_list2["thumbnail"]["source"]
                .replace("/thumb", "")
            )
        else:
            img_link = ""
        url = json_list2["fullurl"]
        extract = re.sub(
            ' class=".*?"',
            "",
            re.sub(
                "\s\s+",
                " ",
                re.sub(
                    "<!--.*?-->",
                    "",
                    json_list2["extract"]
                    .replace("\n", " ")
                    .replace("\t", " ")
                    .replace("<dfn>", "")
                    .replace("</dfn>", ""),
                ),
            ),
        )
        return img_link, url, extract
    except:
        return "", "", ""


file_id = "1"

url = (
    "https://raw.githubusercontent.com/eyssette/frise-philo/main/data/philosophers-"
    + file_id
    + ".csv"
)
response = urllib.request.urlopen(url)
lines = [l.decode("utf-8") for l in response.readlines()]
cr = csv.reader(lines)
next(cr)

with open("philosophes-" + file_id + ".tsv", "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")

    writer.writerow(
        [
            "Philosophe",
            "Naissance",
            "Mort",
            "Catégorie",
            "Image",
            "Page Wikipedia",
            "Extrait Wikipédia",
        ]
    )

    for row in cr:
        if file_id == "4":
            philosopher_name, birth, death, category = row
        else:
            philosopher_name, birth, death, category, curriculum = row
        img_link, url, extract = get_philosopher_info(philosopher_name)
        writer.writerow(
            [philosopher_name, birth, death, category, img_link, url, extract]
        )