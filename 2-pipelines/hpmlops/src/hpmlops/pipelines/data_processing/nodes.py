import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm, skew
import statsmodels.api as sm

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder, RobustScaler, OneHotEncoder, PowerTransformer
from sklearn.impute import SimpleImputer


def remove_outliers(train, parameters):
    train = train.copy()
    train = train.drop(train[(train['GrLivArea']>parameters['outliers']['GrLivArea']) & 
                             (train['SalePrice']<parameters['outliers']['SalePrice'])]
                       .index)
    return train

def create_target(train):
    y_train = np.log1p(train["SalePrice"])
    return y_train

def drop_cols(train, parameters):
    return train.drop(parameters['cols_to_drop'],axis=1)

def fill_na(train, parameters):
    train = train.copy()
    train[parameters['none_cols']] = train[parameters['none_cols']].fillna("None")
    train[parameters['zero_cols']] = train[parameters['zero_cols']].fillna(0)
    
    train["LotFrontage"] = train.groupby("Neighborhood")["LotFrontage"].transform(
                                        lambda x: x.fillna(x.median()))
    
    impute_int = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    impute_str = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    
    int_cols = train.select_dtypes(include='number').columns
    str_cols = train.select_dtypes(exclude='number').columns
    
    train[int_cols] = impute_int.fit_transform(train[int_cols])
    train[str_cols] = impute_str.fit_transform(train[str_cols])
    
    return train

def total_sf(train):
    train = train.copy()
    train['TotalSF'] = train['TotalBsmtSF'] + train['1stFlrSF'] + train['2ndFlrSF']
    return train