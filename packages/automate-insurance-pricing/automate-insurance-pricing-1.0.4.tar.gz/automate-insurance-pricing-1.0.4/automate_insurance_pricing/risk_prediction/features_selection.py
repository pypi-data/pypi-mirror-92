import numpy as np

from sklearn.feature_selection import RFECV, SelectFromModel
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

import seaborn as sns
import matplotlib.pyplot as plt

from copy import deepcopy

from automate_insurance_pricing.risk_prediction.charts_functions import *
from automate_insurance_pricing.preprocessing.charts_functions import *


def display_scree_plot(pca, save=False, prefix_name_fig=None, folder='Charts'):
    """ Plots a scree plot \n \
        Arguments --> the pca, a boolean to indicate if the plot has to be saved or not, the prefix name for the saved file and the folder where to save the chart \n \
    """

    scree = pca.explained_variance_ratio_*100
    plt.bar(np.arange(len(scree))+1, scree)
    plt.plot(np.arange(len(scree))+1, scree.cumsum(), c="red", marker='o')
    plt.xlabel("Inertia axis rank")
    plt.ylabel("Inertia percentage")
    plt.title("Eigen values")

    if save == True:
        prefix_name_fig = prefix_name_fig + '_' if prefix_name_fig is not None else ''
        plt.savefig(folder + '/' + prefix_name_fig + '.png')

def display_circles(pca, n_comp, axis_ranks, labels=None, label_rotation=0, lims=None, figsize=(14,5), save=True, prefix_name_fig=None, folder='Charts'):
    """ Plots the correlation circles from the pca results \n \
        Arguments --> the pca, the number of composantes, the composante axis (a list of tuples representing the composante number), the features names associated to these composantes \n \
            a rotation factor for the labels texts, the chart limits to enforce for the axes \n \
            the figure size, a boolean to indicate if the plot has to be saved or not, the prefix name for the saved file and the folder where to save the chart
    """

    pcs = pca.components_

    for d1, d2 in axis_ranks:

        if d2 < n_comp:

            fig, ax = plt.subplots(figsize=figsize)

            if lims is not None :
                xmin, xmax, ymin, ymax = lims
            elif pcs.shape[1] < 30 :
                xmin, xmax, ymin, ymax = -1, 1, -1, 1
            else :
                xmin, xmax, ymin, ymax = min(pcs[d1,:]), max(pcs[d1,:]), min(pcs[d2,:]), max(pcs[d2,:])

            if pcs.shape[1] < 30 :
                plt.quiver(np.zeros(pcs.shape[1]), np.zeros(pcs.shape[1]),
                   pcs[d1,:], pcs[d2,:],
                   angles='xy', scale_units='xy', scale=1, color="grey")
            else:
                lines = [[[0,0],[x,y]] for x,y in pcs[[d1,d2]].T]
                ax.add_collection(LineCollection(lines, axes=ax, alpha=.1, color='black'))

            if labels is not None:
                for i, (x, y) in enumerate(pcs[[d1,d2]].T):
                    if x >= xmin and x <= xmax and y >= ymin and y <= ymax :
                        plt.text(x, y, labels[i], fontsize='14', ha='center', va='center', rotation=label_rotation, color="blue", alpha=0.5)

            circle = plt.Circle((0,0), 1, facecolor='none', edgecolor='b')
            plt.gca().add_artist(circle)

            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)

            plt.plot([-1, 1], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-1, 1], color='grey', ls='--')

            plt.xlabel('F{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)))
            plt.ylabel('F{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)))

            plt.title("Correlations circle (F{} et F{})".format(d1+1, d2+1))

            if save == True:
                prefix_name_fig = prefix_name_fig + '_' if prefix_name_fig is not None else ''
                plt.savefig(folder + '/' + prefix_name_fig + 'F' + str(d1+1) + 'F' + str(d2+1) + '.png')

def display_factorial_planes(pca, n_comp, axis_ranks, labels=None, alpha=1, hue=None, figsize=(14,5), save=True, prefix_name_fig=None, folder='Charts'):
    """ Plots the factorial plans from the pca results \n \
        Arguments --> the pca, the number of composantes, the composante axis (a list of tuples representing the composante number), the features names associated to these composantes \n \
            an opacity alpha factor, the variable to split the data with (for example if the variable has two modalities, then there will be two different color points) \n \
            the figure size, a boolean to indicate if the plot has to be saved or not, the prefix name for the saved file and the folder where to save the chart
    """

    X_projected = pca.features_projected

    for d1,d2 in axis_ranks:

        if d2 < n_comp:

            fig = plt.figure(figsize=figsize)

            if hue is None:
                plt.scatter(X_projected[:, d1], X_projected[:, d2], alpha=alpha)
            else:
                hue = np.array(hue)
                for value in np.unique(hue):
                    selected = np.where(hue == value)
                    plt.scatter(X_projected[selected, d1], X_projected[selected, d2], alpha=alpha, label=value)
                plt.legend()

            if labels is not None:
                for i,(x,y) in enumerate(X_projected[:,[d1,d2]]):
                    plt.text(x, y, labels[i],
                              fontsize='14', ha='center',va='center')

            boundary = np.max(np.abs(X_projected[:, [d1,d2]])) * 1.1
            plt.xlim([-boundary,boundary])
            plt.ylim([-boundary,boundary])

            plt.plot([-100, 100], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-100, 100], color='grey', ls='--')

            plt.xlabel('F{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)))
            plt.ylabel('F{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)))

            plt.title("Observation projections on F{} and F{}".format(d1+1, d2+1))

            if save == True:
                prefix_name_fig = prefix_name_fig + '_' if prefix_name_fig is not None else ''
                plt.savefig(folder + '/' + prefix_name_fig + 'F' + str(d1+1) + 'F' + str(d2+1) + '.png')            
            

def run_pca(df, features, scalerMethod, n_components=6):
    """ Runs the pca analysis \n \
        Arguments --> the dataframe, the features to reduce, the scaler and the number of components we want to reduce the features to \n \
        Returns --> the pca object
    """
    features_scaled = scalerMethod().fit_transform(df[features].values)

    pca = PCA(n_components=n_components)
    pca.fit(features_scaled)
    pca.features_projected = pca.transform(features_scaled)

    print('Selected components explain {:.2%} of the total variance'.format(pca.explained_variance_ratio_.sum()))

    return pca



def run_select_from_model(X, y, model, **params):
    """
        Runs the algorithmn SelectFromModel (based on feature importance) and finds the most relevant features \n \
        Arguments --> the features, the dependent variable, the model, \n \
            and the params for the selectFromModel method like the number max of features to select \n \
        Returns --> the selector along with the retained features
    """

    selector = SelectFromModel(model, **params)
    selector.fit(X, y)

    # Gets the features that have been selected
    new_X = X.drop(columns=X.columns[np.where(selector.get_support() == False)[0]])
    relevant_features = new_X.columns.tolist()

    print('The threshold for selection is {0} and the features that seem to be the most important are: {1}'.format(selector.threshold_, relevant_features))

    return selector, relevant_features



def run_rfe(X, y, model, with_plot_scoring_curve=True, fig_size_scoring=(16, 9), with_plot_features_importance=True, fig_size_importance=(16, 9), **params):

    """
        Performs a recursive feature elimination to select the most important features \n \
        Arguments --> the features, the target variable, \n \
            a boolean indicating if it needs to plot the score curve depending on the number of features kept, its figure size, \n \
            a boolean indicating if it plots the selected feature importance and the figure size, \n \
            the kwargs are the arguments for the model like the number of folds to use for cross validation, the scoring method ('accuracy', 'explained variance' etc.) \n \
        Returns --> the rfe along with the retained features
    """

    rfecv = RFECV(estimator=model, **params)
    rfecv.fit(X, y)

    # Gets the features that have been selected
    new_X = X.drop(columns=X.columns[np.where(rfecv.get_support() == False)[0]])
    relevant_features = new_X.columns.tolist()

    if with_plot_scoring_curve == True:
        plot_scoring_curve(rfecv, figsize=fig_size_scoring)

    print('The optimal number of features is {0} and the features that seem to be the most important are: {1}'.format(rfecv.n_features_, relevant_features))

    if with_plot_features_importance == True:
        plot_features_importance(new_X, rfecv, figsize=fig_size_importance)

    return rfecv, relevant_features



def correlation_from_model(df, features_corr_matrice, model, draws=5, additional_outputs=None, target_column=None, corr_threshold=0.5, figsize=(10,10)):
    """
        Gets the features correlation coeffient for a specific type of relation determined by the model chosen in arguments \n \
        Arguments --> The full data, the corr matrice (used to get the features pairs), the chosen model (e.g. LinearRegression, RandomForest, etc.), \n \
            the number of draws (equivalent to a cross validation with different data split), \n \
            the dict specifying the other actions to perform by the function. Each value of the dict must be a function or a boolean (e.g. plotting a chart), \n \
            the dependent variable, the correlation threshold, the figure size, \n \
            the kwargs is used for the model params (e.g. the alpha argument for a Lasso Regression) \n \
        Returns --> a new correlation matrice with the coefficients corresponding to the correlation between the predicted feature value thanks to another feature and with the model specified in the arguments
    """

    corr_matrice = deepcopy(features_corr_matrice)
    dict_output = {}

    # Takes the first feature that we will be used to predict the other features
    # Will do it for each of the features
    for feature1 in corr_matrice.index:
        xi = df[feature1].to_frame()

        # Takes another feature. This feature is the one that will be predicted thanks to the first feature
        # Each feature will be predicted thanks to the selected model and the first feature from the parent loop
        for feature2 in corr_matrice.columns:
            xj = df[feature2].to_frame()
            corr_coefs_list = []

            # Performs several random splits to reduce bias and variance
            for k in range(0, draws):
                xi_train, xi_test, xj_train, xj_test = train_test_split(xi, xj, test_size=0.5)

                # instanciates the model with the params specified in the keyword arguments
                model.fit(xi_train, xj_train.values.ravel())
                # Predicts the feature2 value
                mod_predict = model.predict(xi_test)

                # Gets the correlation coef value
                corr_coef = np.corrcoef(xj_test, mod_predict, rowvar=False)[0, 1]
                corr_coefs_list.append(corr_coef)

            # The random splits have been done, the average of the feature predicted values is taken
            corr_matrice.loc[feature1, feature2] = sum(corr_coefs_list) / len(corr_coefs_list)

    dict_output['corr_matrice'] = corr_matrice

    # Runs extra actions like plotting charts
    for key in additional_outputs:

        if key == 'corr_matrice_plot':
            if additional_outputs[key]['display'] == True:
                plt.subplots(figsize=additional_outputs[key]['figsize'])
                sns.heatmap(corr_matrice, annot=True)

        else:
            if additional_outputs[key] == '' or additional_outputs[key] is None:
                continue
            dict_output[key] = additional_outputs[key](df=df, features_corr_matrice=corr_matrice, model=model, figsize=figsize, target_column=target_column, corr_threshold=corr_threshold)

    return dict_output



def get_correlated_features(features_corr_matrice, target_column, corr_threshold=None):
    """Gets the features that have a correlations between each other higher than the threshold specified in the arguments \n \
        Arguments --> the corr matrice (used to get the features pairs), the dependent variable, the correlation threshold \n \
        Returns --> the features that have been considered as correlated
    """

    corr_matrice = deepcopy(features_corr_matrice)
    corr_threshold = corr_threshold if corr_threshold is not None else 0.5

    corr_list = []
    features = [column for column in corr_matrice.columns if column != target_column]
    corr_matrice_index = [column for column in corr_matrice.index if column != target_column]

    for feature1 in corr_matrice_index:

        features.remove(feature1)

        for feature2 in features:
            corr_value = corr_matrice.loc[feature1, feature2]

            if corr_value > corr_threshold or corr_value < -corr_threshold:
                corr_list.append((feature1, feature2, corr_value))

    corr_list = sorted(corr_list, key=lambda x: -abs(x[2]))

    return corr_list



def get_relevant_features(features_corr_matrice, target_column, corr_threshold=None):
    """Gets the potential relevant features for the target variable prediction based on a correlation threshold specified in the arguments \n \
        Arguments --> the corr matrice (used to get the features pairs), the dependent variable, the correlation threshold \n \
        Returns --> the features that have considered correlated to the target variable
    """

    corr_matrice = deepcopy(features_corr_matrice)
    corr_threshold = corr_threshold if corr_threshold is not None else 0.5

    corr_with_target = abs(features_corr_matrice[target_column])
    relevant_features = corr_with_target[corr_with_target>corr_threshold].drop(labels=target_column).index

    return relevant_features



def get_corr_matrice(df, columns, plot_matrice=True, figsize=(16, 9), save=True, prefix_name_fig=None, folder='Charts'):
    """Produces the corr matrice between the columns specified in the arguments, and plots it \n \
        Arguments --> the dataframe, the features, a boolean indicating if we plot a heat map or not, \n \
            the figure size, a boolean to indicate if the plot has to be saved or not, the prefix name for the saved file and the folder where to save the chart \n \
        Returns --> the correlation matrice displaying all the features pairs
    """

    features_corr_matrice = df[columns].corr()

    if plot_matrice == True:
        plt.subplots(figsize=figsize)
        sns.heatmap(features_corr_matrice, annot=True)

    if save == True:
        prefix_name_fig = prefix_name_fig + '_' if prefix_name_fig is not None else ''
        plt.savefig(folder + '/' + prefix_name_fig + '.png')

    return features_corr_matrice