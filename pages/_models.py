from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline

from xgboost import XGBRegressor
import pandas as pd
import numpy as np

cat_cols = ['model', 'condition', 'transmission', 'drive']

class CategoricalImputer(BaseEstimator, TransformerMixin):
    """Categorical data missing value imputer."""

    def __init__(self, variables=None) -> None:
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables
        self.imputer_dict = {}

    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> "CategoricalImputer":
        """Fit statement to accomodate the sklearn pipeline."""
        for variable in self.variables:
            self.imputer_dict[variable] = X[variable].value_counts().index[0]
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply the transforms to the dataframe."""

        X = X.copy()
        for feature in self.variables:
            X[feature] = X[feature].fillna(self.imputer_dict[feature])

        return X

class FilterColumns(BaseEstimator, TransformerMixin):
    """Categorical data missing value imputer."""

    def __init__(self, variables=None) -> None:
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> "CategoricalImputer":
        """Fit statement to accomodate the sklearn pipeline."""
        
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply the transforms to the dataframe."""
        X = X.copy()
        X.drop(self.variables, axis=1, inplace=True)

        return X

class OHEncoder(BaseEstimator, TransformerMixin):
    """Categorical data missing value imputer."""
    def __init__(self, variables=None) -> None:
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables
    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> "CategoricalImputer":
        """Fit statement to accomodate the sklearn pipeline."""
        self.encoder = OneHotEncoder(categories='auto', handle_unknown='infrequent_if_exist', drop='first')
        self.encoder.fit(X[self.variables])
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply the transforms to the dataframe."""
        X = X.copy()
        X1 = self.encoder.transform(X[self.variables]).toarray()
        other_vars = [col for col in X.columns if col not in self.variables+['price']]
        X = np.concatenate([X[other_vars].values, X1], axis=1)

        return X

price_pipe = Pipeline(
    [
        (
            "categorical_imputer",
            CategoricalImputer(variables=cat_cols),
        ),
        (
            "filter_columns",
            FilterColumns(variables=['year', 'manufacturer', 'paint_color', 'state', 'posting_year']),
        ),
        (
            "temporal_variable",
            OHEncoder(variables=cat_cols),
        ),
        ("scaler", MinMaxScaler()),
        ("XGB", XGBRegressor(n_estimators=1000, max_depth=7, eta=0.1, subsample=0.7, colsample_bytree=0.8)),
    ]
)