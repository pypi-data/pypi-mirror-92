
import pandas as pd  # 1.0.1
import json
import joblib  # 0.14.1
from sklearn.feature_extraction import DictVectorizer
import time

loaded_model = joblib.load('finalized_model.sav')

def spectator_classifier(game_list):
    t1 = time.time()
    vecArr = []
    v = DictVectorizer(sparse=False)

    for vals in game_list:
        participants = vals['participants']

        flat_list = [item for sublist in v.fit_transform(participants[:len(participants)//2]) for item in sublist]
        vecArr.append({'participants': [int(i) for i in flat_list]})

        flat_list_final = [item for sublist in v.fit_transform(participants[len(participants)//2:]) for item in sublist]
        vecArr.append({'participants': [int(i) for i in flat_list_final]})

    data = pd.DataFrame(vecArr)

    z_pred = loaded_model.predict(list(data['participants']))
    t2 = time.time()
    print(t2-t1)

    return z_pred


