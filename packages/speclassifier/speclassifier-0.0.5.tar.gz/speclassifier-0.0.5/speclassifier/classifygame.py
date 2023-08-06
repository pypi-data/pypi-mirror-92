
from sklearn import metrics  # 0.0.0
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import datasets
import pandas as pd  # 1.0.1
import pymongo  # 3.10.1
import json
import joblib  # 0.14.1
from sklearn.feature_extraction import DictVectorizer
from gcloud import storage

loaded_model = joblib.load('finalized_model.sav')

def spectator_classifier(game_list):
    vecArr = []
    v = DictVectorizer(sparse=False)

    for vals in game_list:
        participants = vals['participants']
        for participant in participants:
            del participant['teamId']

        flat_list = [item for sublist in v.fit_transform(participants[:len(participants)//2]) for item in sublist]
        vecArr.append({'participants': [int(i) for i in flat_list]})
        flat_list_final = [item for sublist in v.fit_transform(participants[len(participants)//2:]) for item in sublist]
        vecArr.append({'participants': [int(i) for i in flat_list_final]})

    data = pd.DataFrame(vecArr)
    data.head()
    z_pred = loaded_model.predict(list(data['participants']))
    return {'pred': z_pred}

