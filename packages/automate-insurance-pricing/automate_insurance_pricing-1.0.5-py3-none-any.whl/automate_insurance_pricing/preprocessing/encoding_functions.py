import pandas as pd
import numpy as np

from copy import deepcopy
from datetime import date, timedelta, datetime



def min_max_scale(df, features, min_max_scaler):
    """
        Makes a min-max scaling method on the features \n \
        Arguments --> The dataframe, the list of features to rescale and the scaler \n \
        Returns --> a new df, copy of the original df but with the features scaled
    """

    new_df = deepcopy(df)

    for feature in features:
        new_df[feature + '_scaled'] = min_max_scaler.fit_transform(new_df[feature].to_frame())

    return new_df, min_max_scaler


def hot_encode(df, features, features_hot_encoded, encoder):
    """
        Hot encodes the features \n \
        Arguments --> the dataframe, the features to encode, the names to give to the new features encoded and the encoder \n \
        Returns --> A new df with features hot encoded
    """

    data_encoded = pd.DataFrame(encoder.fit_transform(df[features].astype('str')), columns=features_hot_encoded)

    new_df = pd.concat([df, data_encoded], axis=1, join='inner').reindex()

    for feature in features:
        value = new_df[feature].unique()[0]
        col_to_remove = feature + '_' + str(value)
        # Drops the original feature as not needed anymore
        # Drops the first value of the encoded feature as it can be directly infered from the other values
        new_df.drop(columns=[feature, col_to_remove], inplace=True)

    return new_df, encoder


def label_encode(df, features, encoder, sort_features=None):
    """
        Label encodes the features \n \
        Arguments --> the dataframe, the features to encode, the encoder \n \
            a boolean specifyin if the column values need to be sorted before being encoded (ordinal feature)
        Returns --> A new df, copy of the original df but with features label encoded
    """

    if features is None or len(features) == 0:
        print("No features to encode have been specified in the 'features' argument")
        return df, encoder

    new_df = deepcopy(df)

    list_features = features if isinstance(features, list) else [features]
    list_sort_features = sort_features if sort_features is None or isinstance(features, list)  == True else [features]

    for index, feature in enumerate(list_features):
        new_feature = feature + '_label_enc'

        if list_sort_features is None or list_sort_features[index] == True:
            data = new_df[feature]
            encoder.fit(data.sort_values().values.astype('str'))
            new_df[new_feature] = encoder.transform(data.values.astype('str'))

        else:
            new_df[new_feature] = encoder.fit_transform(new_df[feature].astype('str'))

    return new_df, encoder