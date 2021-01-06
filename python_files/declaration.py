import pandas as pd
import os
def init():
    global anime1,anime_features
    path1 = os.path.join('files/real_anime.csv')
    path2= os.path.join('files/anime_features.csv')
    anime1 = pd.read_csv(path1)
    anime_features = pd.read_csv(path2)
