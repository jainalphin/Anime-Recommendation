from python_files.characters import get_characters
from python_files.voice_staff import get_voice_characters
from python_files import declaration
import requests
def get_anime_details(anime_name):
    #request for data
    try:
        query = '''
            query ($search: String){
            Media(search:$search,type: ANIME){
             id             
                coverImage{
                        large
                        }
                   characters(sort:FAVOURITES_DESC){
                       edges{
                           node{
                           id
                               name{
                               full
                               native
                               alternative
                               }
                                image{
                                    large
                                }
                                description
                            }
                            voiceActors(language : JAPANESE){

                                name{
                                    full
                               native
                               alternative
                                    }
                                id                 
                                image{
                                large
                                }
                                 description
                                }
                       }
                   }
            }
            }
        '''
        variables = {
            'search': anime_name
        }
        url = 'https://graphql.anilist.co'
        response = requests.post(url, json={'query': query, 'variables': variables})
        data_json = response.json()
    except:
        pass

    # now lets gather all data
    anime2 = declaration.anime1[declaration.anime1['name'] == anime_name]
    title = "".join(map(str,anime2['name'].values))
    title_japanese = "".join(map(str,anime2['title_japanese'].values))
    type = "".join(map(str,anime2['type'].values))
    source = "".join(map(str,anime2['source'].values))
    studio = "".join(map(str,anime2['studio'].values))
    genre = "".join(map(str,anime2['genre'].values))
    episodes= "".join(map(str,anime2['episodes'].values))
    status = "".join(map(str,anime2['status'].values))
    duration ="".join(map(str,anime2['duration'].values))
    rating = "".join(map(str,anime2['rating'].values))
    score = "".join(map(str,anime2['score'].values))
    rank = "".join(map(str,anime2['rank'].values))
    synopsis="".join(map(str,anime2['synopsis'].values))
    timeline="".join(map(str,anime2['timeline'].values))
    image_url = ""
    anime_id = "".join(map(str, anime2['animeID'].values))

    try:
        image_url= data_json['data']['Media']['coverImage']['large']
        anime_id = data_json['data']['Media']['id']
    except:
        pass

    cast = get_characters(data_json, anime_id)
    voice_staff = get_voice_characters(data_json)

    return title, title_japanese, \
           type, source, \
           studio, \
           genre, episodes, \
           status, duration, \
           rating, score, \
           rank, synopsis, \
           timeline, image_url, anime_id, cast, voice_staff


