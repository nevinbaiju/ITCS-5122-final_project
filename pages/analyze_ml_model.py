from ._models import price_pipe
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def report_metrics(X, y, model):
    y_pred = model.predict(X)
    mape = str(int(mean_absolute_percentage_error(y, y_pred)*100)) + '%'
    mae = str(int(mean_absolute_error(y, y_pred))) + '$'
    
    return y-y_pred, mape, mae

def plot_hist(dat):
    fig = plt.figure(figsize=(8, 4))
    sns.histplot(dat)
    plt.xlim(-5000, 5000)
    plt.title('Prediction errors from the ML model')
    plt.xlabel('Error')
    return fig

def analyze_ml_model(segment):
    df = pd.read_csv(f'processed_data/{segment.lower()}.csv')
    X = df.iloc[:, 1:].dropna()
    y = df.iloc[X.index, 0]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    model = joblib.load(f'models/{segment.lower()}.pkl')

    y_train_errors, train_mape, train_mae = report_metrics(X_train, y_train, model)
    y_test_errors, test_mape, test_mae = report_metrics(X_test, y_test, model)

    st.header('Train metrics')
    train_col1, train_col2, train_col3 = st.columns(3)

    with train_col1:
        train_col1.metric("MAE", train_mae, "")
    with train_col2:
        train_col2.metric("MAPE", train_mape, "")
    with train_col3:
        st.write(plot_hist(y_train_errors))

    st.header('Test metrics')
    test_col1, test_col2, test_col3 = st.columns(3)
    
    with test_col1:
        test_col1.metric("MAE", test_mae, "")
    with test_col2:
        test_col2.metric("MAPE", test_mape, "")
    with test_col3:
        st.write(plot_hist(y_test_errors))