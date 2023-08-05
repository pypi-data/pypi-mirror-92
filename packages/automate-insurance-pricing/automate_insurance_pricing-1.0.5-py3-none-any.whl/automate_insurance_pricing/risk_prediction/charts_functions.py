import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from scipy import stats
from statsmodels import graphics
import statsmodels.api as sm
from statsmodels.graphics.api import abline_plot

import seaborn as sns
import matplotlib.pyplot as plt

from copy import deepcopy


def display_error_by_param(cv_results, name_score, param, figsize=(15, 10), save=False, prefix_name_fig=None, folder='Charts'):

    param = 'param_' + param
    sns.lineplot(cv_results[param].data, cv_results[name_score])
    fig = plt.gcf()
    fig.set_size_inches(figsize[1], figsize[2])

    if save == True:
        prefix_name_fig = prefix_name_fig + '_' if prefix_name_fig is not None else ''
        plt.savefig(folder + '/' + prefix_name_fig + param + '.png')
    
    

def plot_observed_predicted(y_data, y_predict, ols_line=False, model_fit=None, figsize=(15, 10), save=False, end_name_fig='', folder='Charts'):
    """
        Plots the predicted vs the observed values \n \
        Arguments --> the test target variable values, the predictions, \n \
            a boolean indicating if predictions are from a ols model, \n \ 
            and the glm fitted model to make tests on pearson / deviance residuals \n \
            the figure size, a boolean to indicate if the plot has to be saved or not, the prefix name for the saved file, the chart title and the folder where to save the chart
    """    

    end_name_fig = end_name_fig + '_' if end_name_fig is not None else ''

    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(y_data, y_predict)
    
    if ols_line == False:
        ax.plot([y_data.min(), y_data.max()], [y_data.min(), y_data.max()], 'k--', lw=4)

    else:
        line_fit = sm.OLS(y_data, sm.add_constant(y_predict, prepend=True)).fit()
        abline_plot(model_results=line_fit, ax=ax)

    ax.set_title('Predicted vs Observed')
    ax.set_ylabel('Observed values')
    ax.set_xlabel('Predicted values')

    if save == True:
        plt.savefig(folder + '/predict_observed_' + end_name_fig + '.png')

    if model_fit is not None:
        
        fig, ax = plt.subplots(figsize=figsize)
        ax.scatter(y_predict, model_fit.resid_pearson)
        ax.hlines(0, 0, 1)
        ax.set_xlim(0, 1)
        ax.set_title('Residual Dependence Plot')
        ax.set_ylabel('Pearson Residuals')
        ax.set_xlabel('Fitted values') 

        if save == True:
            plt.savefig(folder + '/pearson_residuals_' + end_name_fig + '.png')


        fig, ax = plt.subplots(figsize=figsize)
        res_dev_residuals = model_fit.resid_deviance.copy()
        res_dev_residuals_std = stats.zscore(res_dev_residuals)
        ax.hist(res_dev_residuals_std, bins=25)
        ax.set_title('Histogram of standardized deviance residuals')

        if save == True:
            plt.savefig(folder + '/standard_deviance_residuals_' + end_name_fig + '.png')

        graphics.gofplots.qqplot(res_dev_residuals, line='r')

        if save == True:
            plt.savefig(folder + '/gofplot_' + end_name_fig + '.png')        
        

def display_linear_model_features(model_name, coefs, save=False, prefix_name_fig=None, folder='Charts'):
    """ Plots a feature importance \n \
        Arguments --> the model name, the coefs obtained, a boolean to indicate if the plot has to be saved or not, the prefix name for the saved file and the folder where to save the chart
    """

    imp_coefs = coefs.sort_values()
    imp_coefs.plot(kind = "barh")
    plt.title("Feature importance using {} Model".format(model_name))
    
    if save == True:
        prefix_name_fig = prefix_name_fig + '_' if prefix_name_fig is not None else ''
        plt.savefig(folder + '/' + prefix_name_fig + '.png')    
    

def plot_models_results(results, names, figsize=(16, 14), save=False, prefix_name_fig=None, folder='Charts'):
    """Compare the models plotting their results in a boxplot \n \
        Arguments --> the model results, their names, the figure size, a boolean to indicate if the plot has to be saved or not, the prefix name for the saved file and the folder where to save the chart
    """

    fig = plt.figure(figsize=figsize)
    fig.suptitle('Algorithm Comparison')
    ax = fig.add_subplot(111)
    plt.boxplot(results)
    ax.set_xticklabels(names)
    
    if save == True:
        prefix_name_fig = prefix_name_fig + '_' if prefix_name_fig is not None else ''
        plt.savefig(folder + '/' + prefix_name_fig + '.png')     
    

def plot_features_importance(X, rfecv, figsize=(16, 14), save=False, prefix_name_fig=None, folder='Charts'):
    """ Plots the importance features selected by a RFE method \n \
        Arguments --> the features, the rfe model, the figure size, a boolean to indicate if the plot has to be saved or not, the prefix name for the saved file and the folder where to save the chart
    """

    new_df = pd.DataFrame()
    new_X = deepcopy(X)

    if len(rfecv.estimator_.feature_importances_) != X.shape[1]:
        new_X = X.drop(columns=X.columns[np.where(rfecv.support_ == False)[0]])

    new_df['attr'] = new_X.columns

    new_df['importance'] = rfecv.estimator_.feature_importances_

    new_df = new_df.sort_values(by='importance', ascending=False)

    plt.figure(figsize=figsize)
    plt.barh(y=new_df['attr'], width=new_df['importance'], color='#1976D2')
    plt.title('RFECV - Feature Importances', fontsize=20, fontweight='bold', pad=20)
    plt.xlabel('Importance', fontsize=14, labelpad=20)

    if save == True:
        prefix_name_fig = prefix_name_fig + '_' if prefix_name_fig is not None else ''
        plt.savefig(folder + '/' + prefix_name_fig + '.png')  

    

def plot_scoring_curve(rfecv, figsize=(16, 9), save=False, prefix_name_fig=None, folder='Charts'):
    """ Plots the scoring curve obtained from a RFE method and shows what is the optimal number of features to keep
        Arguments --> the rfe model, the figure size, a boolean to indicate if the plot has to be saved or not, the prefix name for the saved file and the folder where to save the chart 
    """

    plt.figure(figsize=figsize)
    plt.title('Recursive Feature Elimination with Cross-Validation', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Number of features selected', fontsize=14, labelpad=20)
    plt.ylabel('% Correct Classification', fontsize=14, labelpad=20)
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_, color='#303F9F', linewidth=3)

    if save == True:
        prefix_name_fig = prefix_name_fig + '_' if prefix_name_fig is not None else ''
        plt.savefig(folder + '/' + prefix_name_fig + '.png')  
    
    

def pairplot_cross_val(df=None, features_corr_matrice=None, model=None, figsize=(10,10), save=False, prefix_name_fig=None, folder='Charts', **kwargs):
    """
        Plots a scatter plot for all pair of features
        Arguments --> the dataframe, the corr matrice (used to get the features pairs), the model,
            the figure size, a boolean to indicate if the plot has to be saved or not, the prefix name for the saved file and the folder where to save the chart \n \
            and kwargs which shoud mainly correspond to the model params
    """

    corr_matrice = deepcopy(features_corr_matrice)
    features_number = len(corr_matrice.columns) 

    fig, ax = plt.subplots(features_number, features_number, figsize=figsize)

    if model is None:
        model = LinearRegression

    # Takes the first feature that we will be used to predict the other features
    # Will do it for each of the features
    for index1, feature1 in enumerate(corr_matrice.index):
        xi = df[feature1].to_frame()

        # Takes another feature. This feature is the one that will be predicted thanks to the first feature
        # Each feature will be predicted thanks to the selected model and the first feature from the parent loop
        for index2, feature2 in enumerate(corr_matrice.columns):
            xj = df[feature2].to_frame()
            corr_coefs_list = []

            xi_train, xi_test, xj_train, xj_test = train_test_split(xi, xj, test_size=0.5)

            # xj test will be predicted from xi and the model trained on the train set
            model.fit(xi_train, xj_train.values.ravel())
            mod_predict_test = model.predict(xi_test)

            # xj train will be predicted from xi and the model trained on the test set
            model.fit(xi_test, xj_test.values.ravel())
            mod_predict_train = model.predict(xi_train)

            # Plots in the same graph the xj prediction against true xj from the test set, and from the train set
            ax[index1, index2].plot(xj_test, mod_predict_test, ".")
            ax[index1, index2].plot(xj_train, mod_predict_train, ".")

            if index2 == 0:
                ax[index1, index2].set_ylabel(feature1)

            if index1 == features_number-1:
                ax[index1, index2].set_xlabel(feature2)

            # Plots the affine curve y=x starting, and set the x-axis from the min value to the max value of the features values
            mi = min(min(xj_test.values), min(mod_predict_test), min(xj_train.values), min(mod_predict_train))
            ma = max(max(xj_test.values), max(mod_predict_test), max(xj_train.values), max(mod_predict_train))
            ax[index1, index2].plot([mi, ma], [mi, ma], "--")

            if save == True:
                prefix_name_fig = prefix_name_fig + '_' if prefix_name_fig is not None else ''
                plt.savefig(folder + '/' + prefix_name_fig + '.png')
                
    return ax