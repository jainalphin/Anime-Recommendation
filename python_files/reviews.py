import requests
import re
from jikanpy import Jikan
jikan = Jikan()

def get_reviews(anime_id):
    reviews_dict = {}
    try:
        url = 'https://api.jikan.moe/v3/anime/' + str(anime_id) + '/reviews'
        response = requests.get(url)
        data_json = response.json()
        for i in range(5):
            try:
                regex = re.compile(r'[\n\r\t\\]')
                about = regex.sub('',data_json['reviews'][i]['content'])
                scores = data_json['reviews'][i]['reviewer']['scores']
                scores = str(scores)
                reviews_dict[about] =scores.split('{')[1].replace("}","").replace("'","").replace(",","\n")
            except:
                try:
                    query = '''
                        query ($id: Int){
                        Media(id:$id){
                         reviews(limit:3){
                               edges{
                                       node{
                                       rating
                                        body
                                       }
                               }
                            }
                        }
                    }
                    '''
                    variables = {
                        'id': 1
                    }
                    url = 'https://graphql.anilist.co'
                    response = requests.post(url, json={'query': query, 'variables': variables})
                    data_json = response.json()
                    regex = re.compile(r'[\n\r\t\\#~_.\']')
                    about = regex.sub('', data_json['data']['Media']['reviews']['edges'][1]['node']['body'])
                    reviews_dict[about] = data_json['data']['Media']['reviews']['edges'][1]['node']['score']
                except:
                    pass
    except:
        pass
    return reviews_dict