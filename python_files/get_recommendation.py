import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import requests
from python_files import declaration
from jikanpy import Jikan
jikan = Jikan()

declaration.init()
anime_feat_scaler = MinMaxScaler()
anime_features3 = anime_feat_scaler.fit_transform(declaration.anime_features)
knn2 = NearestNeighbors(n_neighbors=10,algorithm='brute',metric='cosine').fit(anime_features3)
all_anime_names = list(declaration.anime1.name.str.lower())

def get_recommendation(anime_name):
    similar_anime =[]
    anime_name = anime_name.lower()
    if anime_name not in all_anime_names:
        return None
    else:
        query_index =all_anime_names.index(anime_name)
        distances1, indices1 = knn2.kneighbors(anime_features3[query_index].reshape(1, -1), n_neighbors = 11)
        for i in range(1, len(distances1.flatten())):
                similar_anime.append(declaration.anime1['name'][indices1.flatten()[i]])
        return  similar_anime

def recommended_anime_detail(anime_names):
    recommended_animes ={}
    query = '''
               query ($search: String){
               Media(search:$search,type: ANIME){
                   id 
                   title {
                   romaji
                     english
                       }            
               coverImage{
                       large
                       }
                   }
               }
           '''
    for i in anime_names:
        variables = {
            'search': str(i)
        }
        url = 'https://graphql.anilist.co'
        response = requests.post(url, json={'query': query, 'variables': variables})
        data_json = response.json()
        try:
            if 'errors' in data_json:
                data_json = jikan.search('anime', str(i), page=1)
                recommended_animes[data_json['results'][0]['title']] = data_json['results'][0]['image_url']
            else:
                recommended_animes[str(i).capitalized()] = data_json['data']['Media']['coverImage']['large']

        except:

            data_json2 = jikan.search('anime', str(i), page=1)
            recommended_animes[data_json2['results'][0]['title']] = data_json2['results'][0]['image_url']

    return recommended_animes


def get_suggestions():
    return list(declaration.anime1['name'])
