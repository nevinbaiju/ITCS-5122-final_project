import pandas as pd
import joblib
from ._models import *
import os

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline

from xgboost import XGBRegressor

def build_model(segment='midsize'):
    df = pd.read_csv(f'processed_data/{segment.lower()}.csv')
    X = df.iloc[:, 1:]
    y = df.iloc[:, 0]

    price_pipe.fit(X, y)
    joblib.dump(price_pipe, f'models/{segment}.pkl')


def make_prediction(pred_data, segment='midsize'):
    if not os.path.exists(f'models/{segment.lower()}.pkl'):
        build_model(segment)
    pred_data['manufacturer'] = "_"
    pred_data['state'] = "_"
    pred_data['posting_year'] = 2023
    pred_data['age'] = 2023 - pred_data['year']
    data_list = [[pred_data['year'], pred_data['manufacturer'], pred_data['model'],
                 pred_data['condition'], pred_data['odometer'], pred_data['transmission'],
                 pred_data['drive'], pred_data['paint_color'], pred_data['state'], pred_data['posting_year'],
                 pred_data['age']]]
    pred_data = pd.DataFrame(data_list)
    pred_data.columns=['year','manufacturer','model','condition',
                       'odometer','transmission','drive','paint_color',
                       'state','posting_year','age']
    model = joblib.load(f'models/{segment.lower()}.pkl')
    
    return model.predict(pred_data)

def load_data(segment):
    return pd.read_csv(f'processed_data/{segment.lower()}.csv')