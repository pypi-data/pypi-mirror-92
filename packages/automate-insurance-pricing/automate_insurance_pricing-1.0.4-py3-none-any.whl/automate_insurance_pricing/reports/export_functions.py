import pandas as pd

import openpyxl

from automate_insurance_pricing.standard_functions import *

def export_glm_coefs_to_excel(features_coefs, features, glm_file_path):
    """ Exports to excel the glm rating factors of the features (either a list or a string) \n \
        Arguments --> The features coefficients, the features, and the file path used for the export
    """

    new_features = [features] if isinstance(features, str) == True else features

    for feature in new_features:
        feature_name = remove_words(feature, feature=('feature', ''), label=('label_enc', ''), bins=('bins', ''), scaled=('scaled', ''), underscore=('_', ' '), double_points=(':', 'x'), special_character1=(']', ''))[:31]
        data = {feature_name + ' ' + 'value': [i[0] for i in features_coefs[feature]], 'coef_value': [i[1] for i in features_coefs[feature]]}
        df_rating_factor = pd.DataFrame(data)

    try:
        with pd.ExcelWriter(glm_file_path, engine="openpyxl", mode='a') as writer:
            df_rating_factor.to_excel(writer, sheet_name=feature_name)
    except:
        with pd.ExcelWriter(glm_file_path, engine="openpyxl", mode='w') as writer:
            df_rating_factor.to_excel(writer, sheet_name=feature_name) 