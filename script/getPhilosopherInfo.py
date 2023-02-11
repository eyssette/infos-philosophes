import csv, urllib.request
import json
import re

def get_philosopher_info(philosopher_name):
    query_url = "https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=info|pageimages|extracts&exintro&generator=allpages&inprop=url&gaplimit=1&gapfrom=" + urllib.parse.quote(philosopher_name)
    try: 
        wikipediaResponse = urllib.request.urlopen(query_url)
        wikipediaResponseTxt = wikipediaResponse.read().decode('utf-8')
        json_data = json.loads(wikipediaResponseTxt)
        json_list = list(json_data['query'].values())[0]
        json_list2 = list(json_list.values())[0]
        if 'thumbnail' in json_list2:
            img_link = json_list2['thumbnail']['source']
        else:
            img_link = ''
        url = json_list2['fullurl']
        extract = json_list2['extract']
        return img_link,url,extract
    except:
        return ''

url = 'https://raw.githubusercontent.com/eyssette/frise-philo/main/data/philosophers-1.csv'
response = urllib.request.urlopen(url)
lines = [l.decode('utf-8') for l in response.readlines()]
cr = csv.reader(lines)
next(cr)

for row in cr:
    philosopher_name = row[0]
    info_philosopher = get_philosopher_info(philosopher_name)
    if info_philosopher[0]=='':
        image_url =''
    else :
        image = re.sub("/50px.*",'',info_philosopher[0].replace('/thumb',''))
        image_url='<img src="'+image+'" />'
    url_wikipedia='<a href="'+info_philosopher[1]+'">Page wikipedia</a>'
    extract_info=re.sub('<!--.*?-->','',info_philosopher[2].replace("\n", " "))
    extract='<details>'+extract_info+'</details>'
    print(f'{philosopher_name}\t{row[1]}\t{row[2]}\t{row[3]}\t{image_url}\t{url_wikipedia}\t{extract}')
