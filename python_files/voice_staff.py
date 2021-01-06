import numpy as np
import re
from jikanpy import Jikan
jikan = Jikan()

def get_voice_characters(data_json):
    cast = {}
    try:
        length = np.where(len(data_json['data']['Media']['characters']['edges']) >= 5, 5,
                          len(data_json['data']['Media']['characters']['edges']))
        for i in range(length):
            if len(data_json['data']['Media']['characters']['edges'][i]['voiceActors']) == 0:
                pass
            else:
                chara_id = data_json['data']['Media']['characters']['edges'][i]['voiceActors'][0]['id']

                full_name = data_json['data']['Media']['characters']['edges'][i]['voiceActors'][0]['name']['full']
                native_name = str(data_json['data']['Media']['characters']['edges'][i]['voiceActors'][0]['name']['native']).replace(r'[',"").replace(r']',"").replace("'","")
                alternative = str(data_json['data']['Media']['characters']['edges'][i]['voiceActors'][0]['name']['alternative']).replace(r'[',"").replace(r']',"").replace("'","")

                image_url = data_json['data']['Media']['characters']['edges'][i]['voiceActors'][0]['image']['large']

                description = str(data_json['data']['Media']['characters']['edges'][i]['voiceActors'][0]['description'])
                regex = re.compile(r'[\n\r\t\\_]')
                about = regex.sub('<br>', description)
                if full_name in cast:
                    full_name = str(full_name) + '(2)'

                cast[full_name] = [chara_id, image_url,native_name, alternative, about]
    except:
        pass

    return cast