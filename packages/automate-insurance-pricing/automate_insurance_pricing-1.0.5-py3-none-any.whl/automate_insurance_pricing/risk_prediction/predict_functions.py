import pandas as pd
import numpy as np

from sklearn.preprocessing import FunctionTransformer

from timeit import default_timer as timer

from automate_insurance_pricing.reports.export_functions import *


def get_glm_rating_factors(df, glm_coefs, num_features_analysis, constant_column_name='const', transformer=FunctionTransformer(), export_excel=False, glm_file_path=None):
    """
        Gets the GLM rating factor values for all features values \n \
        Arguments --> the dataframe, the coefs values found by the glm for each feature, the numerical features names, the column name for the constant (reference) obtained by the glm \n \
            the transformer object which corresponds to the link for a GLM, \n \
            a boolean indicating if it needs to export the results to excel, and the export file path \n \
        Returns --> a dict with feature as keys and tuples as values corresponding to the feature modalities and their impacts on the target variable (i.e. the rating factor applied on the feature value)
    """

    features_coefs = {}

    for feature in glm_coefs.index:

        if feature != constant_column_name and ((feature in df.columns and len(df[feature].unique()) > 2) or feature not in df.columns):
            glm_coef = glm_coefs[glm_coefs.index==feature][0]
            number_features = feature.count(':') + 1
            features = feature.split(':')
            original_values = df[features[0].replace('_scaled', '')]

            min_value, max_value = original_values.min(), original_values.max()
            discrete_values = list(range(int(min_value), int(max_value) + 1, int(max_value/100 + 1)))

            if len(features) > 1:

                for selected_feature in features[1:]:

                    if selected_feature in num_features_analysis:
                        original_values = df[selected_feature]
                        new_min_value, new_max_value = original_values.min(), original_values.max()
                        new_discrete_values = list(range(int(new_min_value), int(new_max_value) + 1, int(new_max_value/100 + 1)))

                        min_value *= new_min_value
                        max_value *= new_max_value

                        df_cartesian = (
                            pd.DataFrame(discrete_values).assign(key=1)
                            .merge(pd.DataFrame(new_discrete_values).assign(key=1), on="key")
                            .drop("key", axis=1)
                        )

                        discrete_values = list(df_cartesian.iloc[:, 0] * df_cartesian.iloc[:, 1])

            diff_from_min_scaled = (discrete_values - min_value) / (max_value - min_value)
            feature_coefs = transformer.inverse_transform(glm_coef * diff_from_min_scaled).tolist()

        else:
            discrete_values = [1]
            feature_coefs = [transformer.inverse_transform(glm_coefs[glm_coefs.index==feature][0])]

        features_coefs[feature] = list(zip(discrete_values, feature_coefs))

        if export_excel == True:
            export_glm_coefs_to_excel(features_coefs, feature, glm_file_path)

    return features_coefs



def print_model_coefs(model_name, results, features, transformer=FunctionTransformer(), sort=True):
    """ Displays the selected model and its linear predictor expression \n \
        Arguments --> the model name, its results, the features, \n \
            the transformer object which corresponds to the link for a GLM, \n \
            a boolean indicating if coefs must be sorted
    """

    print('Model {}:\n'.format(model_name))

    if 'coefs' in results.keys():
        coefs = results['coefs']

        if 'alpha' in results.keys():
            print("{0} model Best alpha: {1}\n".format(model_name, results['alpha']))

        print("{} model picked ".format(model_name) + str(sum(coefs != 0)) + " variables and eliminated the other " +  str(sum(coefs == 0)) + " variables\n")

        print("*********************\n")

        print('target variable = {}'.format(print_linear_predictor(coefs, names=features, transformer=transformer, sort=sort)))
        
        

def print_linear_predictor(coefs, names=None, transformer=FunctionTransformer(), sort=False):
    """ Displays the linear predictor expression \n \
        Arguments --> the coefficients, the features names associated to them, the link function and a boolean indicating if coefs must be sorted
        Returns --> the expression of the target as linear function of the features
    """

    if names == None:
        names = ["X%s" % x for x in range(len(coefs))]
    lst = zip(coefs, names)

    if sort == True:
        lst = sorted(lst,  key= lambda x: -transformer.inverse_transform(np.abs(x[0])))

    return " + ".join("%s * %s" % (round(coef, 5), name)
                                   for coef, name in lst)


def run_model_predictions(model_name, model, X_train, X_test, y_train, y_test, features, transformer=FunctionTransformer()):
    """ Runs a model \n \
        Arguments --> the model name, the model, the train and test independent and target variables \n \
            the transformer object which corresponds to the link for a GLM, \n \
        Returns --> the results obtained by the model
    """

    results = {}

    y_train_transformed = transformer.transform(y_train)
    results['model_fit'] = model_fit = model.fit(X_train, y_train_transformed)

    y_test_transformed = transformer.transform(y_test)
    results['score'] = score = round(model_fit.score(X_test, y_test_transformed), 5)

    results['predictions'] = transformer.inverse_transform(model_fit.predict(X_test))

    if hasattr(model_fit, 'coefs'):
        results['alpha'] = alpha = round(model_fit.alpha_, 5)

    if hasattr(model_fit, 'coefs'):
        try:
            results['coefs'] = pd.Series(model_fit.coef_[0], index = X_train[features].columns)
        except:
            results['coefs'] = pd.Series(model_fit.coef_, index = X_train[features].columns)

    return results



def run_simple_model(model, X_test, y_test):
    """Runs a simple model with default hyperparameters to quickly obtain its score \n \
        Arguments --> the model, the independant and dependent variable on the test set \n \
        Returns --> the model score
    """

    start_time = timer()
    model.fit(X_test, y_test)
    training_time = timer() - start_time

    model_score = model.score(X_test, y_test)

    print('The baseline model applied on the test set has a score of {:.4f}.'.format(model_score))
    print('The baseline model needs {:.4f} seconds'.format(training_time))

    return model_score
