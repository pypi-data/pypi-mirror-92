import numpy as np

from sklearn.model_selection import cross_val_score, RandomizedSearchCV, KFold
from sklearn.feature_selection import RFECV, SelectFromModel

from hyperopt import fmin, hp, STATUS_OK, tpe, Trials
from hyperopt.pyll.stochastic import sample

import csv

from copy import deepcopy
import random

from timeit import default_timer as timer

from automate_insurance_pricing.risk_prediction.charts_functions import *


def hyperopt_obj_func(params, X_train=None, y_train=None, model=None, objective=None, scoring=None, file_path=None):
    """
        Objective function for the bayesian hyperparameters search with hyperopt module \n \
        Arguments --> the hyperparameters to try, the independent and dependent variables, \n \
            the algorithmn model to work on, its objective function and the scoring method to evaluate which params give the best model \n \
            If a scoring method is indicated it will overwrite the objective function \n \
            the file path where the results will be saved
        Returns --> a dict storing the hyperopt trials (loss and status) and the params
    """

    params['subsample'] = params['boosting_type'].get('subsample', 1.0)
    params['boosting_type'] = params['boosting_type']['boosting_type']

    selected_model = model(**params) if objective is None else model(**params, objective=objective)
    loss = cross_val_score(selected_model, X_train, y_train, scoring=scoring).mean()

    try:
        of_connection = open(file_path, 'a')
        writer = csv.writer(of_connection)
        writer.writerow(['bayesian_optim', loss, params])
    except:
        print('The results could not be written in the csv. Check the file path.')
        pass

    return {'loss': loss, 'params': params, 'status': STATUS_OK}


def run_random_search(X_train, y_train, model, param_grid, n_iter=10, cv=5, scoring='neg_root_mean_squared_error', random_state=42, file_path=None, **params):
    """
        Runs a Randomized hyperparameters search thanks to scikit learn method \n \
        Arguments --> the features/target variable, \n \
            the model and params to fine tune, the number of iterations and folds for cross validations \n \
            the scoring method to select the best params, the random state to reproduce the same results \n \
            the file path where the results will be saved \n \
            and the keyword arguments for the model itself \n \
        Returns --> the final params results
    """

    rscv = RandomizedSearchCV(model(**params), param_grid, n_iter=n_iter, cv=cv, scoring=scoring, refit=True, random_state=random_state)
    rscv.fit(X_train, y_train)
    
    try:
        of_connection = open(file_path, 'a')
        writer = csv.writer(of_connection)
        writer.writerow(['random_search', rscv.best_score_, rscv.best_params_])
    except:
        print('The results could not be written in the csv. Check the file path.')
        pass

    return rscv


# def get_random_results(lgb_train_set, params, iteration, metrics='mape', stratified=False, random_state=42, **kwargs):
#     """
#         Gets the model results using the hyperparameters and cross validation method
#         Arguments --> the hyperparameters chosen, the iteration index and the number of folds used for cross validation
#     """

#     start_time = timer()

#     cv_results = lgb.cv(params, lgb_train_set, metrics=metrics, stratified=stratified, seed=random_state, **kwargs)
#     end_time = timer()

#     loss = 1 - np.max(cv_results[metrics + '-mean'])
#     n_estimators = int(np.argmax(cv_results[metrics + '-mean']) + 1)

#     return [loss, params, iteration, n_estimators, end_time - start_time]



# def run_random_search(df_random_results, lgb_train_set, param_grid, max_evals, subsample_dist=None, **kwargs):
#     """
#         Perfoms a randomized search to find the best hyperparameter for a specified model

#     """

#     for i in range(max_evals):
#         random_params = {key: random.sample(value, 1)[0] for key, value in param_grid.items()}
#         random_params['subsample'] = random.sample(subsample_dist, 1)[0] if subsample_dist is not None and random_params['boosting_type'] != 'goss' else 1.0

#     random_results = get_random_results(lgb_train_set, random_params, i, **kwargs)

#     df_random_results.loc[i, :] = random_results



def run_multiple_models(X_train, y_train, models, y_transformer=None, scoring='accuracy', n_splits=5, plot_results=True, random_state=42):
    """
        Runs multiple models to compare their results \n \
        Arguments --> The features, the target variable, the models to run, \n \
            the transformer if the target variable has been transformed (e.g. a log transformation), \n \
            the scoring measure to use to compare the algorithms, \n \
            the number of folds for the cross validation, \n \
            a boolean indicating if a plot of the result will be displayed, \n \
            a random state to reproduce the same results \n \
        Returns --> the results of the models
    """
    results = []
    models_tried = [model[1] for model in models]
    names = [model[0] for model in models]

    y = deepcopy(y_train)

    if y_transformer is not None:
        y = y_transformer.transform(y)

    for name, model in models:
        kfold = KFold(n_splits=n_splits)
        cv_results = cross_val_score(model(), X_train, y, cv=kfold, scoring=scoring)
        results.append(cv_results)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())

    if plot_results == True:
        plot_models_results(results, names)

    return list(zip(names, models_tried, results))



def get_mape(y_true, y_pred):
    """ Derives the mean absolute percentage error between the actual and predicted value"""

    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.where(y_true != 0, np.abs((y_true - y_pred) / y_true) * 100, 0))



def mean_percentage_error(y_true, y_pred):
    """ Derives the mean percentage error between the actual and predicted value"""

    y_true, y_pred = np.array(y_true), np.array(y_pred)
    nil_y_error = ((y_true - y_pred) / y_true)[y_true!=0]

    return round(np.mean(nil_y_error) * 100, 2)