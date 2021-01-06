import requests
import numpy as np
import re
from jikanpy import Jikan
jikan = Jikan()

def get_characters(data_json,anime_id):
    cast = {}
    try:
        length = np.where(len(data_json['data']['Media']['characters']['edges']) >= 5, 5,
                          len(data_json['data']['Media']['characters']['edges']))
        for i in range(length):
            chara_id = data_json['data']['Media']['characters']['edges'][i]['node']['id']
            full_name = data_json['data']['Media']['characters']['edges'][i]['node']['name']['full']
            native_name = str(data_json['data']['Media']['characters']['edges'][i]['node']['name']['native']).replace(r'[',"").replace(r']',"").replace("'","")
            alternative = str(data_json['data']['Media']['characters']['edges'][i]['node']['name']['alternative']).replace(r'[',"").replace(r']',"").replace("'","")

            image_url = data_json['data']['Media']['characters']['edges'][i]['node']['image']['large']

            description = str(data_json['data']['Media']['characters']['edges'][i]['node']['description'])
            regex = re.compile(r'[\n\r\t\\]')
            about = regex.sub('', description)

            cast[full_name] = [chara_id, image_url,native_name, alternative, about]
    except:
        print(anime_id)
        url = 'https://api.jikan.moe/v3/anime/' + str(anime_id) + '/characters_staff'
        response = requests.get(url)
        data_json = response.json()
        length = np.where(len(data_json['characters']) > 5, 5, len(data_json['characters']))
        for i in range(length):
            try:
                chara_id = data_json['characters'][i]['mal_id']
                chara_info = jikan.character(chara_id)

                image_url = chara_info['image_url']
                nicknames = ", ".join(chara_info['nicknames'])

                regex = re.compile(r'[\n\r\t\\]')
                about = regex.sub('', chara_info['about'])

                name = chara_info['name']
                cast[name] = [chara_id, image_url,"", nicknames, about]

            except:
                pass
    return cast