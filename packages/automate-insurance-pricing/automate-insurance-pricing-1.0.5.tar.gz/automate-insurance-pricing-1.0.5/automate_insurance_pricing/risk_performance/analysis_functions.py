import numpy as np

import pandas as pd
import math

from copy import deepcopy

from automate_insurance_pricing.risk_prediction.charts_functions import *
from automate_insurance_pricing.preprocessing.charts_functions import *
    
def compare_to_mean_by_feature(df_analysis, target_column, mean_target, features, rebase_on='exposure', rebase_to_value=100, plot_chart=True, figsize=(12, 8), save=False, prefix_name_fig=None, folder='Charts', title=None):
    """
        Compare the dependent mean value for each feature modality to the mean on the whole dataset \n \
        Arguments --> the df, the target column, its mean on the whole df, the features on which to perform the analysis, \n \
            the column name that must be used to derive the target variable mean on a subset matching the feature modality, e.g. if we need to derive frequencies then we need first to derive the total exposure concerned by the modality, \n \
            (this column can be set to False, in that case, we just get the mean thanks to a group by) \n \
            the value to rebase the figures, by default it is in base 100, \n \
            the figure size, a boolean to indicate if the plot has to be saved or not, the prefix name for the saved file, the chart title and the folder where to save the chart \n \
        Returns --> a dictionnary where the keys are the features names and the values the comparison tables
    """
    
    df_compare = {}
    df_compare_styled = {}

    for feature in features:
        if rebase_on == False:
            df_compare[feature] = pd.DataFrame(df_analysis.groupby(feature)[target_column].mean() / mean_target) * rebase_to_value
        else:
            df_compare[feature] = pd.DataFrame((df_analysis.groupby(feature)[target_column].sum() / df_analysis.groupby(feature)[rebase_on].sum()) / mean_target) * rebase_to_value
            df_compare[feature] = df_compare[feature].rename(columns={0: target_column})

        df_compare_styled[feature] = df_compare[feature].style.format('{:.2f}')

    print(df_compare.keys())

    if plot_chart == True:
        plot_bar_charts2(df_compare, target_column, columns=features, n_cols=1, figsize=figsize, save=save, prefix_name_fig=prefix_name_fig, folder=folder, title=title)  
        
    return df_compare


def get_interquartile_lower_upper(df, target_column):   
    """ Gets the quantiles a variable and returns the interquartile range"""
    
    quantile_25 = df[target_column].quantile(0.25)
    median = df[target_column].quantile(0.5)
    quantile_75 = df[target_column].quantile(0.75)

    interquartile_range = [quantile_25, quantile_75]
    interquartile = quantile_75 - quantile_25
    lower_bound = quantile_25 - 1.5 * interquartile
    upper_bound = quantile_75 + 1.5 * interquartile   
    
    return interquartile_range, lower_bound, upper_bound



def style_df(df, currency='€'):
    """ Makes the df look prettier """

    new_df = deepcopy(df)

    percentage_columns = [col for col in new_df.columns if any(name in col for name in ['ratio', 'frequency', 'rate'])]
    formats = {'n': '{:.0f}'.format, 'm': '{:,.0f}'.format, 'c': ('{:,.0f}' + ' ' + currency).format, 'p': '{:.2%}'.format}
    formatters = {col: formats['c'] if any(name in col for name in ['cost', 'premium', 'gep', 'gwp']) else formats['p'] if col in percentage_columns else formats['m'] for col in new_df.select_dtypes(include=['float64', 'int64', 'int32']).columns}

    return new_df.style.format(formatters)


def run_multi_analysis_by_feature(df_portfolio, df_claims, portfolio_kpis, claims_kpis, claims_limit, LL_loading, current_comm, new_comm, target_LR_new_comm, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name='policy_id', unknown_rows_name='UNKNOWN', row_per_each_contract_year=True, exposure_column_name='exposure', written_premium_column_name='asif_written_premium_excl_taxes', earned_premium_column_name='asif_earned_premium', occurrence_date_column_name='occurrence_date', claims_column_name='asif_total_capped_cost', full_claims_column_name='asif_total_cost', capped_claims_column_name='asif_total_capped_cost', claim_count_column_name='count_claim', guarantees=None, guarantee_column_name='guarantee_impacted', analysis_year_level=None, features=None, parent_features=None, triangle_costs=None, triangle_counts=None, style_format=False, currency='€'):
    """
        Generates the summary tables that displays the portfolio performance by feature \n \
        Arguments --> portfolio and claims df to work on, the portfolio and claims kpis (exposure, premiums, costs, etc.), \n \
            the capped claims threshold, the LL loading, \n \
            the current and new commission rates and the entailed new target loss ratio \n \
            the start and end years of the study, \n \
            the contract start and policy columns names \n \
            the name given to rows identified as potentially wrong with missing information \n \
            a boolean indicating if the data is aggregated at policy level or if each yearly contract is represented by a new row \n \
            the exposure, written premium, earned premium, claims occurrence dates, full claims, capped claims and the claims number columns names \n \
            the list of guarantees we want to look at the performance and the column name indicating the type of guarantee involved, \n \
            the type of year analysis (by occurrence/inception/effective year) \n \
            the segmentation, i.e. on which features the analysis will be performed, and features for a higher level of segmentation (typically the formula as most analysis will be relevant only for a specific formula and not overall) \n \
            the claims amounts and counts triangles that will be used, \n \
            the style format (produces a prettier table if set to true ) and currency used (only if style format set to true) \n \
        Returns --> a dictionnary with the features names as keys and the performance summary tables as values
    """

    df_multiple_analysis = {}
    new_df_claims = deepcopy(df_claims)
    parent_features = [] if parent_features is None else [parent_features] if isinstance(parent_features, str) == True else parent_features
    features = [parent_features + [feature] if len(parent_features) > 0 and feature not in parent_features else feature for feature in features]

    if guarantees is not None:
        guarantees = [guarantees] if isinstance(guarantees, str) == True else guarantees
        new_df_claims = df_claims[df_claims[guarantee_column_name].isin(guarantees)]

    for feature in features:
        df_analysis_feature = build_table(df_portfolio, new_df_claims, portfolio_kpis, claims_kpis, claims_limit, LL_loading, current_comm, new_comm, target_LR_new_comm, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name, unknown_rows_name, row_per_each_contract_year, exposure_column_name, written_premium_column_name, earned_premium_column_name, occurrence_date_column_name, full_claims_column_name, capped_claims_column_name, claim_count_column_name, table_for_prediction=False, analysis_year_level=analysis_year_level, portfolio_group_by_columns=feature, triangle_costs=triangle_costs, triangle_counts=triangle_counts, style_format=style_format, currency=currency)
                                            
        if isinstance(feature, list) == True:
            feature = tuple(feature)

        df_multiple_analysis[feature] = df_analysis_feature

    return df_multiple_analysis


# In[144]:
                            
def run_all_analysis_by_year(df_portfolio, df_claims, portfolio_kpis, claims_kpis, claims_limit, LL_loading, current_comm, new_comm, target_LR_new_comm, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name='policy_id', unknown_rows_name='UNKNOWN', row_per_each_contract_year=True, exposure_column_name='exposure', written_premium_column_name='asif_written_premium_excl_taxes', earned_premium_column_name='asif_earned_premium', occurrence_date_column_name='occurrence_date', claims_column_name='asif_total_capped_cost', full_claims_column_name='asif_total_cost', capped_claims_column_name='asif_total_capped_cost', claim_count_column_name='count_claim', guarantees=None, guarantee_column_name='guarantee_impacted', triangle_costs=None, triangle_counts=None, style_format=False, currency='€', **kwargs):
    """
        Generates the summary tables that displays the portfolio performance by occurrence year / inception / effective year
        Arguments --> portfolio and claims df to work on, the portfolio and claims kpis (exposure, premiums, costs, etc.), \n \
            the capped claims threshold, the LL loading, \n \
            the current and new commission rates and the entailed new target loss ratio \n \
            the start and end years of the study, \n \
            the contract start and policy columns names \n \
            the name given to rows identified as potentially wrong with missing information \n \
            a boolean indicating if the data is aggregated at policy level or if each yearly contract is represented by a new row \n \
            the exposure, written premium, earned premium, claims occurrence dates, full claims, capped claims and the claims number columns names \n \
            the list of guarantees we want to look at the performance and the column name indicating the type of guarantee involved, \n \
            the segmentation, i.e. on which features the analysis will be performed \n \
            the claims amounts and counts triangles that will be used, \n \
            the style format (produces a prettier table if set to true ) and currency used (only if style format set to true) \n \
        Returns --> three summary tables for each analysis by year
    """

    new_df_claims = deepcopy(df_claims)
    
    if guarantees is not None:
        guarantees = [guarantees] if isinstance(guarantees, str) == True else guarantees
        new_df_claims = df_claims[df_claims[guarantee_column_name].isin(guarantees)]

    # Create analysis per occurrence / inception / effective year
    df_analysis_occurrence_year = build_table(df_portfolio, new_df_claims, portfolio_kpis, claims_kpis, claims_limit, LL_loading, current_comm, new_comm, target_LR_new_comm, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name, unknown_rows_name, row_per_each_contract_year, exposure_column_name, written_premium_column_name, earned_premium_column_name, occurrence_date_column_name, claims_column_name, full_claims_column_name, capped_claims_column_name, claim_count_column_name, table_for_prediction=False, analysis_year_level='occurrence', triangle_costs=triangle_costs, triangle_counts=triangle_counts, style_format=style_format, currency='€', **kwargs)
    df_analysis_inception_year = df_analysis_effective_year = build_table(df_portfolio, new_df_claims, portfolio_kpis, claims_kpis, claims_limit, LL_loading, current_comm, new_comm, target_LR_new_comm, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name, unknown_rows_name, row_per_each_contract_year, exposure_column_name, written_premium_column_name, earned_premium_column_name, occurrence_date_column_name, claims_column_name, full_claims_column_name, capped_claims_column_name, claim_count_column_name, table_for_prediction=False, analysis_year_level='inception', triangle_costs=triangle_costs, triangle_counts=triangle_counts, style_format=style_format, currency='€', **kwargs)
                                                                        
    if row_per_each_contract_year == True:
        df_analysis_effective_year = build_table(df_portfolio, new_df_claims, portfolio_kpis, claims_kpis, claims_limit, LL_loading, current_comm, new_comm, target_LR_new_comm, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name, unknown_rows_name, row_per_each_contract_year, exposure_column_name, written_premium_column_name, earned_premium_column_name, occurrence_date_column_name, claims_column_name, full_claims_column_name, capped_claims_column_name, claim_count_column_name, table_for_prediction=False, analysis_year_level='effective', triangle_costs=triangle_costs, triangle_counts=triangle_counts, style_format=style_format, currency='€', **kwargs)
                                               
    return df_analysis_occurrence_year, df_analysis_inception_year, df_analysis_effective_year

                
def build_table(df_portfolio, df_claims, portfolio_kpis, claims_kpis, claims_limit, LL_loading, current_comm, new_comm, target_LR_new_comm, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name='policy_id', unknown_rows_name='UNKNOWN', row_per_each_contract_year=True, exposure_column_name='exposure', written_premium_column_name='asif_written_premium_excl_taxes', earned_premium_column_name='asif_earned_premium', occurrence_date_column_name='occurrence_date', full_claims_column_name='asif_total_cost', capped_claims_column_name='asif_total_capped_cost', claim_count_column_name='count_claim', table_for_prediction=True, kpis_list=None, analysis_year_level=None, portfolio_group_by_columns=None, claims_group_by_columns=None, triangle_costs=None, triangle_counts=None, rate_increase_params=None, style_format=False, currency='€', **kwargs):
    """
        Creates a summary profitability table or builds the data set ready for risk modelling  \n \
        Arguments --> portfolio and claims dataframes to work on, the portfolio and claims kpis (exposure, premiums, costs, etc.), \n \
            the capped claims threshold, the LL loading, \n \
            the current and new commission rates and the entailed new target loss ratio \n \
            the start and end years of the study, \n \
            the contract start and policy columns names \n \
            the name given to rows identified as potentially wrong with missing information \n \
            a boolean indicating if the data is aggregated at policy level or if each yearly contract is represented by a new row \n \
            the exposure, written premium, earned premium, claims occurrence dates, full claims, capped claims and the claims number columns names \n \
            a boolean indicating if it must produce a summary profitability table or if we are building the database for risk prediction, \n \
            the kpis names, this argument will be used only when creating the dataset for modelling and to perform a sense check ensuring no data has been lost. Must be left as None for profitability analysis. \n \
            the type of year analysis (by occurrence/inception/effective year) \n \
            the segmentation, i.e. on which features the analysis will be performed, and features for a higher level of segmentation (typically the formula as most analysis will be relevant only for a specific formula and not overall) \n \
            the claims amounts and counts triangles that will be used, \n \
            the rates adjustments to apply to the premiums, it must be a dictionnary with features modalities as keys and adjustments as values \n \
            example: rates_increases = {'[25-35)': 0.2, 'London’: 0.1}, this will increase all insured age between 25 et 35 by 20% and all insured located in London by 10% \n \
            the style format (produces a prettier table if set to true ) and currency used (only if style format set to true) \n \
        Returns --> either a summary profitability table or the full dataset ready for risk prediction works 
    """

    new_df_portfolio, new_df_claims = deepcopy(df_portfolio), deepcopy(df_claims)
    new_df_claims = new_df_claims[new_df_claims[policy_id_column_name].isin(new_df_portfolio[policy_id_column_name])]

    new_portfolio_group_by = [] if portfolio_group_by_columns is None else [portfolio_group_by_columns] if isinstance(portfolio_group_by_columns, str) == True else deepcopy(portfolio_group_by_columns)
    new_claims_group_by = [] if claims_group_by_columns is None else [claims_group_by_columns] if isinstance(claims_group_by_columns, str) == True else deepcopy(claims_group_by_columns)
    year_group_by = []


    # Category type not yet well supported by numpy. Potential issues when merging etc. better having it converted to string
    # portfolio_categorical_columns = new_df_portfolio.select_dtypes('category').columns
    # if len([col for col in new_portfolio_group_by if col in portfolio_categorical_columns]) > 0:
    #     new_df_portfolio[portfolio_categorical_columns] = new_df_portfolio[portfolio_categorical_columns].astype('object')

    # claims_categorical_columns = new_df_claims.select_dtypes('category').columns
    # if len([col for col in new_claims_group_by if col in claims_categorical_columns]) > 0:
    #     new_df_claims[claims_categorical_columns] = new_df_claims[claims_categorical_columns].astype('object')

    if rate_increase_params is not None:
        # It is easier to have all columns that will get rate adjustments converted to string
        # adjust_columns = [value[0] for value in rate_increase_params.values() if value[0] not in portfolio_categorical_columns]
        # adjust_columns = adjust_columns if len(adjust_columns) > 1 else adjust_columns[0]

        # new_df_portfolio[adjust_columns] = new_df_portfolio[adjust_columns].astype(str)
        # new_df_claims[adjust_columns] = new_df_claims[adjust_columns].astype(str)

        new_df_portfolio = adjust_rates(new_df_portfolio, start_business_year, extraction_year, written_premium_column_name, earned_premium_column_name, rate_increase_params)

    # If by occurrence a special treatment is required as in the portfolio there is no occurrence date
    # The only analysis possible by occurrence year is to work on the columns named like this 'in_{year}'
    if analysis_year_level == 'occurrence':

        if table_for_prediction == True:
                print('When occurrence year level is selected, only a summary table by occurrence year can be produced. \n\
Change the analysis_year_level argument to either None, effective or inception if you want to build you table for prediction job. \n\
Change the argument to table_for_prediction False if you want to build a risk analysis summary table.')
                return

        year_group_by = ['occurrence_year']
        df_policy_claims = prep_data_summary_occurrence_year(new_df_portfolio, new_df_claims, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name, unknown_rows_name, row_per_each_contract_year, written_premium_column_name, occurrence_date_column_name, year_group_by, new_portfolio_group_by, new_claims_group_by, claims_kpis)
                                          
    else:

        # Will produce either the full table that will most likely serve for prediction job or a summary table depending on effective/inception year + other variables
        if table_for_prediction == True or analysis_year_level is not None :
            df_policy_claims, year_group_by = other_prepare_data(new_df_portfolio, new_df_claims, policy_id_column_name, main_column_contract_date, row_per_each_contract_year, table_for_prediction, analysis_year_level, new_portfolio_group_by, new_claims_group_by, portfolio_kpis, claims_kpis)
                                                                    
        # The summary table will be on figures depending on portfolio features and claims attributes but not on a yearly basis
        else:
            if len(new_portfolio_group_by + new_claims_group_by) == 0:
                print('Indicate at least one variable on which performing the analysis. Either setting the porfolio_group_by or the claims_group_by argument')
                return
                                            
            df_policy_claims = sum_merge_tables(new_df_portfolio, new_df_claims, policy_id_column_name, new_portfolio_group_by, new_claims_group_by, portfolio_kpis, claims_kpis)
            df_policy_claims = df_policy_claims.reset_index().set_index(new_portfolio_group_by+new_claims_group_by).drop(columns='Total', errors='ignore')

    # Derives the mains kpis such as frequency, average cost and loss ratio
    df_analysis = produce_df_for_analysis(df_policy_claims, analysis_year_level, portfolio_kpis, claims_limit, LL_loading, current_comm, new_comm, target_LR_new_comm, exposure_column_name, earned_premium_column_name, full_claims_column_name, capped_claims_column_name, claim_count_column_name, table_for_prediction=table_for_prediction, triangle_costs=triangle_costs, triangle_counts=triangle_counts, portfolio_group_by=new_portfolio_group_by, claims_group_by=new_claims_group_by)
                                            
    if table_for_prediction == True:
        # Will check the total premiums and claims to see if everything went ok and keep only features + kpis (frequency, average cost, etc.)
        category_columns = df_analysis.select_dtypes('category').columns
        columns_to_fillna = [col for col in df_analysis.columns if col not in category_columns]
        df_analysis[columns_to_fillna] = df_analysis[columns_to_fillna].fillna(0)
        df_analysis = check_finish_table(df_analysis, df_portfolio, df_claims, kpis_list, exposure_column_name, earned_premium_column_name, capped_claims_column_name)

    df_analysis = df_analysis.drop(columns=claims_kpis, errors='ignore')

    # This will do some style formatting to the final df. Only available for summary table as we don't perform any calculations on them
    if table_for_prediction == False and style_format == True:
        df_analysis = style_df(df_analysis, currency)

    return df_analysis

                    
def adjust_rates(df, start_business_year, extraction_year, written_premium_column_name, earned_premium_column_name, rate_increase_params):
    """
        Increase the rates for specific segments such as customer age, chosen formula etc. \n \
        Arguments --> the portfolio df, the start and extraction dates, \n \
            the written and earned premiums columns names \n \
            the rates adjustments to apply to the premiums, it must be a dictionnary with features modalities as keys and adjustments as values \n \
            example: rates_increases = {'[25-35)': 0.2, 'London’: 0.1}, this will increase all insured age between 25 et 35 by 20% and all insured located in London by 10% \n \
        Returns --> a new df with the updated rates
    
    """
    
    new_df = deepcopy(df)
            
    rate_increase_params_values = rate_increase_params.values()
    
    for value in rate_increase_params_values:

        mask = new_df[value[0]] == value[1]
        new_df[written_premium_column_name] = np.where(mask, new_df[written_premium_column_name] * (1 + value[2]), new_df[written_premium_column_name])          
        new_df[earned_premium_column_name] = np.where(mask, new_df[earned_premium_column_name] * (1 + value[2]), new_df[earned_premium_column_name])  

        if True in ['written_premium_in_' in col for col in df.columns]:
            for year in range(start_business_year, extraction_year + 1):
                new_df['asif_written_premium_in_{}'.format(year)] = np.where(mask, new_df['asif_written_premium_in_{}'.format(year)] * (1 + value[2]), new_df['asif_written_premium_in_{}'.format(year)])  
                new_df['asif_earned_premium_in_{}'.format(year)] = np.where(mask, new_df['asif_earned_premium_in_{}'.format(year)] * (1 + value[2]), new_df['asif_earned_premium_in_{}'.format(year)]) 
        else:
            for year in range(start_business_year, extraction_year + 1):
                new_df['asif_earned_premium_in_{}'.format(year)] = np.where(mask, new_df['asif_earned_premium_in_{}'.format(year)] * (1 + value[2]), new_df['asif_earned_premium_in_{}'.format(year)])             
            
    return new_df

                                    
def prep_data_summary_occurrence_year(df_portfolio, df_claims, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name, unknown_rows_name, row_per_each_contract_year, written_premium_column_name, occurrence_date_column_name, year_group_by, portfolio_group_by, claims_group_by, claims_kpis):
    """
        Prepares the porfolio and claims dataframes so that they can then be used for a summary risk analysis by occurrence year \n \
        Arguments --> portfolio and claims dataframes, the business start and data extraction years \n \
            the contract start and policy columns names \n \
            the name given to rows identified as potentially wrong with missing information \n \
            a boolean indicating if the data is aggregated at policy level or if each yearly contract is represented by a new row \n \
            the written premium and the claims occurrence dates columns names \n \
            the name of the column associated to the occurrence year \n \
            the segmentation, i.e. on which features the analysis will be performed \n \
            the claims attributes if the profitability results must be done on specific claims characteristics \n \
            the claims kpis, e.g. capped costs, inflated amounts, etc. \n \
        Returns --> a merged policies-claims df
    """

    df_claim_sum = deepcopy(df_claims)
    df_portfolio_sum = pd.DataFrame()
    year_column_name = year_group_by[0]
    merge_on = year_group_by + portfolio_group_by

    # Selects the columns associated for each year (e.g. 'premium_in_{year}') and derive their totals
    df_portfolio_sum = derive_per_occurrence_year(df_portfolio, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name, unknown_rows_name, row_per_each_contract_year, written_premium_column_name, df_portfolio.columns, year_column_name, portfolio_group_by)
                                                    
    # Aggregates the claims data by the occurrence year and the other variables specified in the arguments
    df_claim_sum[year_column_name] = df_claim_sum[occurrence_date_column_name].dt.year
    df_claim_sum = df_claim_sum.groupby(year_group_by+portfolio_group_by+claims_group_by)[claims_kpis].sum().reset_index()

    # Merges portfolio and claims data based on occurrence year and the variables that served to aggregate portfolio and claims
    df_policies_claims = df_portfolio_sum.merge(df_claim_sum, how='left', on=merge_on).set_index(keys=year_group_by+portfolio_group_by+claims_group_by)

    return df_policies_claims

                            
def derive_per_occurrence_year(df, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name='policy_id', unknown_rows_name='UNKNOWN', row_per_each_contract_year=True, written_premium_column_name='asif_written_premium_excl_taxes', columns_to_sum=None, year_column_name=None, df_group_by=None, style_format=False, currency='€'):
    """
        This function derives the figures by occurrence year and generates a summary table \n \
        Arguments --> the df, the columns to sum, the business start and extraction years, the contract start date and claim occurrence columns name, \n \
            the contract start and policy columns names \n \
            the name given to rows identified as potentially wrong with missing information \n \
            a boolean indicating if the data is aggregated at policy level or if each yearly contract is represented by a new row \n \
            the written premium column name and the list of columns to sum per occurrence year (e.g. earned premium, exposure) \n \
            the column name to get the year and the segmentation used, i.e. on which features the analysis will be performed \n \
            the style format (produces a prettier table if set to true ) and currency used (only if style format set to true) \n \            
        Returns --> a summary table that will display the totals per occurrence year
    """

    def build_aggregation(df, year, df_group_by, year_column_name, columns_to_sum):
        #This function perform the columns summation for a specific occurrence year

        # Retrieves all the columns that must be summed by year, and detected thanks to the suffixe 'in_' + year
        columns_to_sum =  [column for column in columns_to_sum if 'in_' + str(year) in column]
        # Renames the columns so that they will be the same during the concatenations
        column_names={col: col.replace('_in_' + str(year), '') for col in columns_to_sum}
        new_df = df[df_group_by+columns_to_sum]

        # Needs to build the aggegate shape manually because the groupby built-in function cannot be used without variables to group by
        if len(df_group_by) == 0:
            # Sums the rows in each column and transpose the output so that the year is the index and the column remains as a column
            df_sum = new_df[columns_to_sum].sum().to_frame().transpose().rename(index={0: year}, columns=column_names)

        else:
            new_df[year_column_name] = year
            # Reset index to get the variables we've grouped by as columns then we set index to have results depending on the year, i.e. year as an index
            # setting the year as index is needed because we are building the table iteratively by year. otherwise the index will be 0 or 1 and next year result will keep overwriting previous year ones
            df_sum = new_df.groupby(year_group_by+df_group_by)[columns_to_sum].sum().rename(columns=column_names).reset_index().set_index(year_column_name)

        return df_sum

    df_sum = pd.DataFrame()
    columns_to_sum = df.columns if columns_to_sum is None else [columns_to_sum] if isinstance(columns_to_sum, str) == True else deepcopy(columns_to_sum)
    df_group_by = [] if df_group_by is None else deepcopy(df_group_by) if isinstance(df_group_by, list) == True else [df_group_by]

    if year_column_name is None:
        year_group_by = ['occurrence_year']
        year_column_name = 'occurrence_year'
    else:
        year_group_by = [year_column_name]

    years = range(start_business_year, extraction_year + 1)

    if len(columns_to_sum) == 1 and columns_to_sum[0] == written_premium_column_name and row_per_each_contract_year == True:
        df_sum = get_written_premium_occurrence_year(df, main_column_contract_date, policy_id_column_name, unknown_rows_name, row_per_each_contract_year, written_premium_column_name, years=years, year_column_name=year_column_name, df_group_by=df_group_by, alone=False, style_format=style_format, currency=currency)
                                                   
    else:

        for year in years:
            df_intermed_sum = build_aggregation(df, year, df_group_by, year_column_name, columns_to_sum)
            # Concatenates along the rows ; each year line will be added at the bottom of the df
            df_sum = pd.concat([df_sum, df_intermed_sum])

        df_sum = df_sum.reset_index()

        # Adds the written premium to the df
        if written_premium_column_name in columns_to_sum and row_per_each_contract_year == True:
            df_written_premium_sum = get_written_premium_occurrence_year(df, main_column_contract_date, policy_id_column_name, unknown_rows_name, row_per_each_contract_year, written_premium_column_name, years=years, year_column_name=year_column_name, df_group_by=df_group_by, alone=False, style_format=style_format, currency=currency)                               
            df_sum = pd.concat([df_sum, df_written_premium_sum], axis=1)

        df_sum = df_sum.rename(columns={'index': year_column_name})

    # This will do some style formatting to the final df
    if style_format == True:
        formats = {'n': '{:.0f}'.format, 'm': '{:,.0f}'.format, 'c': ('{:,.0f}' + ' ' + currency).format, 'p': '{:,.2f}%'.format}
        formatters = {col: formats['c'] if any(name in col for name in ['premium']) else formats['m'] if col in columns_to_sum else formats['n'] for col in df_sum.select_dtypes(include=['float64', 'int64', 'int32'])}

        return df_sum.fillna(0).style.format(formatters)

    return df_sum

                                        
def get_written_premium_occurrence_year(df, main_column_contract_date, policy_id_column_name='policy_id', unknown_rows_name='UNKNOWN', row_per_each_contract_year=True, written_premium_column_name="asif_written_premium_excl_taxes", start_business_year=None, extraction_year=None, years=None, year_column_name=None, df_group_by=None, alone=None, style_format=False, currency='€'):
    """
        This function derives the right written premium per occurrence year depending on the df format \n \
        Arguments --> the df, the columns names for the policy id, the written premium the contract date and the claim occurrence year, \n \
            the contract start and policy columns names \n \
            the name given to rows identified as potentially wrong with missing information \n \
            a boolean indicating if the data is aggregated at policy level or if each yearly contract is represented by a new row \n \
            the written premium column name and the list of columns to sum per occurrence year (e.g. earned premium, exposure) \n \
            the business starting year and the extraction year, \n \
            the list of years (alternative to specifying start and extraction year), \n \
            the column name to get the year and the segmentation used, i.e. on which features the analysis will be performed \n \
            if alone set to True, means only written premium will be derived, i.e. the function has been used as stand-alone (instead of being called from a parent function doing other jobs), \n \
            the style format (produces a prettier table if set to true ) and currency used (only if style format set to true) \n \                    
        Returns --> a summary table of the written premium per year. The shape of the df will be different if it used within a parent function and needs to be coupled to another summary table
    """

    new_df = deepcopy(df)
    df_group_by = [] if df_group_by is None else deepcopy(df_group_by) if isinstance(df_group_by, list) == True else [df_group_by]

    if year_column_name is None:
        year_group_by = ['occurrence_year']
        year_column_name = 'occurrence_year'
    else:
        year_group_by = [year_column_name]

    # Effective year for portfolio is equivalent to occurrence year for claims when dealing about written premium
    if row_per_each_contract_year == True:
        new_df[year_column_name] = new_df[main_column_contract_date].dt.year
        df_unknown_policies = new_df[new_df[written_premium_column_name]==unknown_rows_name]

        if df_unknown_policies.shape[0] > 0:

            new_df.loc[df_unknown_policies.index, written_premium_column_name] = 0

            if years is None:
                if start_business_year is None or extraction_year is None:
                    print('You need to indicate the years, either by setting the year the data has been extracted and the year the business started \n \
                    or by directly giving to the function the list of years.')
                    return
                else:
                    years = range(start_business_year, extraction_year + 1)

            year_of_unknown_policies = new_df[main_column_contract_date].dt.year[0]

            for year in years:
                if year != year_of_unknown_policies:
                    new_row_df = new_df.loc[new_df.shape[0]-1]
                    new_df.loc[new_df.shape[0]] = new_row_df
                    new_df.loc[new_df.shape[0]-1, year_column_name] = year

        if alone == True:
            df_written_premium_sum = new_df.groupby(year_group_by+df_group_by)[written_premium_column_name].sum().to_frame()
        else:
            df_written_premium_sum = new_df.groupby(year_group_by+df_group_by)[written_premium_column_name].sum().to_frame().reset_index().drop(columns=year_group_by+df_group_by)

    # There is no effective date column, so the database is at policy level
    else:
        df_written_premium_sum = derive_per_occurrence_year(df, start_business_year, extraction_year, main_column_contract_date, policy_id_column_name, unknown_rows_name, row_per_each_contract_year, written_premium_column_name, df_group_by= df_group_by)
                                                            
    # This will do some style formatting to the final df
    if style_format == True:
        return df_written_premium_sum.fillna(0).applymap('{:,.0f}' + ' ' + currency.format)

    return df_written_premium_sum


def other_prepare_data(df_portfolio, df_claims, policy_id_column_name, main_column_contract_date, row_per_each_contract_year, table_for_prediction, analysis_year_level, portfolio_group_by, claims_group_by, portfolio_kpis, claims_kpis):
    """
        Prepares the porfolio and claims df so that they can then be used to create either a profitability table or the data set for risk modelling \n \
        Arguments --> portfolio and claims df, the policy id, and contract date columns names \n \
            a flag indicating if the portfolio has a unique row for the full policy contract or a row per yearly amendment \n \
            a boolean indicating if the result from this function will be used to produce a summary profitability table or if we are building the database for risk prediction, \n \
            the lists of the variables used to make the aggregations: year, portfolio features, claims attributes \n \
            the list of the kpis used in the sommations: portfolio figures like earned premiums, claims figures like costs \n \
        Returns --> a merged policies-claims df
    """

    year_group_by = []
    policy_group_by = []
    df_portfolio_nodupl_policy = None

    # A summary table will be built for risk analysis instead of a full table for risk prediction
    # Only main kpis will be displayed
    if table_for_prediction == False:
        year_group_by = [analysis_year_level + '_year']

        # The analysis will be on inception year but data has rows per yearly contract, not per full contrat length
        if analysis_year_level == 'inception' and row_per_each_contract_year == True:
            analysis_year_level = 'effective'

            # Firsly, sorts by the effective date in order to retrieve the latest contract amendment date by removing the other previous duplicates
            df_portfolio = df_portfolio.sort_values(main_column_contract_date)
            df_portfolio_nodupl_policy = df_portfolio.drop_duplicates(subset=policy_id_column_name, keep='first').drop(columns=portfolio_kpis)

            # Secondly, aggregates per policy and derive the totals. Now the df will be at policy level, i.e. a unique line per policy. But effective dates have been lost due to the sum
            df_portfolio_sum = df_portfolio.groupby([policy_id_column_name])[portfolio_kpis].sum().reset_index()

            # Thirdly Link back the effective dates to the policies
            df_portfolio = df_portfolio_nodupl_policy.merge(df_portfolio_sum, how='left', on=policy_id_column_name)

            # Finally we link the same latest effective date for policies that claimed. Because in the claims data, the contract effective date associated to them is not necessarily the latest one
            df_claims = df_claims.drop(columns=main_column_contract_date).merge(df_portfolio_nodupl_policy[[policy_id_column_name, main_column_contract_date]], how='left', on=policy_id_column_name)

            df_portfolio_nodupl_policy = None

    # The table for prediction is a table that keeps all the policies features and will be displayed differently than if a summary table is requested
    else:
        # To merge policies and claims, policy id will be necessary
        policy_group_by = [policy_id_column_name]
        portfolio_group_by = []
        claims_group_by = []

        # If working at effective date level, each amendment is considered as a true new contract with its own associated features. The effective year will be another variable necessary to merge policy and claims
        # If at inception level, it is equivalent to policy level (one unique line per policy), grouping by policy only is enough
        analysis_year_level = 'effective' if analysis_year_level is None and row_per_each_contract_year == True else analysis_year_level
        year_group_by = ['effective_year'] if analysis_year_level == 'effective' else []

        # As we will sum on the data, features will be lost (or summed as well, which is not consistent neither). We retrieve the features by creating a new df and keeping only the latest policy features
        sorting_column = main_column_contract_date
        df_portfolio_nodupl_policy = df_portfolio.sort_values(sorting_column).drop_duplicates(subset=policy_id_column_name, keep='last').drop(columns=portfolio_kpis)

    # Either this is a summary table per inception or effective year, or it is a table for risk prediction keeping each policy with its amendment contract
    if len(year_group_by) > 0:
        year_column_name = year_group_by[0]
        df_portfolio[year_column_name] = df_portfolio[main_column_contract_date].dt.year
        df_claims[year_column_name] = df_claims[main_column_contract_date].dt.year

    portfolio_group_by = policy_group_by + year_group_by + portfolio_group_by

    # Makes the portolio-claims merge and derives the total figures
    df_policies_claims = sum_merge_tables(df_portfolio, df_claims, policy_id_column_name, portfolio_group_by, claims_group_by, portfolio_kpis, claims_kpis, df_portfolio_nodupl_policy)

    return df_policies_claims, year_group_by


def sum_merge_tables(df1, df2, policy_id_column_name, df1_group_by, df2_group_by, df1_kpis, df2_kpis, df_no_dupl=None):
    """
        Sums separately two dataframes and merge them \n \
        Arguments --> the two 2 dataframes to sum and merge, the policy id column name \n \
            the variables to aggregate on in the two dfs, the kpis to derive in the two dfs \n \
            a df that contains the portfolio features and no policy duplicates. This df will be used when it is the full data for risk prediction that must be obtained \n \
        Returns --> A merged df with the kpis summed adequatly
    """
    
    # Figures must be calculated on portfolio and claims separately, then merging them on the same intersection variables (i.e. the portfolio features) used for the aggregation
    # Here, the analysis is not done by features but only by claims attributes. The portfolio kpis like exposure, premium are the same, they don't vary depending on claims attributes.
    if df1_group_by is None or len(df1_group_by) == 0:
        df1_group_by = ['Total']
        df1_sum = df1[df1_kpis].sum()

        # Converts the pandas series, and tranposes it so that the column Total serves for the merge with claims df
        df1_sum = df1_sum.to_frame().T
        df1_sum['Total'] = 'Total'
        df2_sum = df2.groupby(df2_group_by)[df2_kpis].sum().reset_index()
        df2_sum['Total'] = 'Total'

    else:

        df1_sum = df1.groupby(df1_group_by)[df1_kpis].sum().reset_index()
        df2_sum = df2.groupby(df1_group_by+df2_group_by)[df2_kpis].sum().reset_index()

    # Merges portfolio and claims data based on the variables that served to aggregate both two df
    df_merged = df1_sum.merge(df2_sum, how='left', on=df1_group_by).set_index(keys=df1_group_by+df2_group_by)

    #- The steps above have removed the features, we get them back thanks to the df specified in the argument that corresponds to the portfolio data with features and no duplicates
    if df_no_dupl is not None:
        df_merged = df_no_dupl.merge(df_merged, how='left', on=policy_id_column_name).reset_index(drop=True)

    return df_merged

                        
def check_finish_table(df_analysis, df_portfolio, df_claims, kpis_list, exposure_column_name, earned_premium_column_name, claims_column_name):
    """ Check if the final table produced is consistent by looking at the totals premiums and claims and defines the final kpis to display \n \
        Arguments --> the dataframe on which we perform the checks, the two dataframes portfolio and claims used to check the initial totals \n \
            the list of kpis to check the totals, the exposure, earned premium and claims columns names \n \
        Returns --> the initial table but with only the necessary kpis 
    """
    
    initial_premium_sum, initial_cost_sum = df_portfolio[earned_premium_column_name].sum(), df_claims[claims_column_name].sum()

    new_premium_sum, new_cost_sum = df_analysis[earned_premium_column_name].sum(), df_analysis[claims_column_name].sum()
    diff_premium, diff_claims = new_premium_sum - initial_premium_sum, new_cost_sum - initial_cost_sum
    
    if math.floor(abs(diff_premium)) == 0 and math.floor(abs(diff_claims)) == 0:
        print('A sense check has been made on premiums and claims. Everything looks fine. \
Both the original data and the newly created have: \nEarned Premiums: {0} \nTotal cost: {1}'.format(initial_premium_sum, initial_cost_sum))
    
    else:
        diff_premium, diff_claims = new_premium_sum - initial_premium_sum, new_cost_sum - initial_cost_sum
        print('The table has been built. However it seems there was a problem building the table because total number do not match. \n\
The original data has {0} earned premium whereas we now have {1}, i.e. {2} premium difference. \nAnd there were \
{3} claims originally agains {4} now, i.e. {5} claims difference. \nYou should dig a bit to find out where it comes from.'.format(initial_premium_sum, new_premium_sum, diff_premium, initial_cost_sum, new_cost_sum, diff_claims))
    
    features_analysis = [col for col in df_analysis.columns if 'feature' in col]
    
    if kpis_list is None:
        kpis_list = [exposure_column_name, 'projected_capped_cost', 'claim_occurred', 'number_claims', 'frequency', 'average_cost', 'pure_premium_capped_claims', 'pure_premium_full_claims', 'projected_capped_loss_ratio', 'projected_full_loss_ratio']
        
    columns_to_keep = features_analysis + [col for col in df_analysis.columns if col in kpis_list]   
    df_analysis = df_analysis[columns_to_keep]
    
    return df_analysis

    
def produce_df_for_analysis(df, analysis_year_level, portfolio_kpis, claims_limit, LL_loading, current_comm, new_comm, target_LR_new_comm, exposure_column_name, earned_premium_column_name, full_claims_column_name, capped_claims_column_name, claim_count_column_name, table_for_prediction, triangle_costs, triangle_counts, portfolio_group_by, claims_group_by):
    """
        Derives the main kpis (e.g. the ones that will be displayed in the profitability table or that will be modelled)
        Arguments --> the dataframe with policies and claims merged \n \
            the type of year analysis (by occurrence/inception/effective year) \n \
            the portfolio and claims kpis columns names (exposure, earned premium, inflated claims amounts etc.)
            the capped claims threshold, the LL loading, \n \
            the current and new commission rates and the entailed new target loss ratio \n \
            the exposure, earned premium, full claims, capped claims and the claims number columns names \n \
            a boolean indicating if it must produce a summary profitability table or if we are building the database for risk prediction, \n \
            the claims amounts and counts triangles that will be used, \n \
            the segmentation, i.e. on which features the analysis will be performed \n \
            the claims attributes (only if the parent function must create a profitability result) if the profitability results must be done on specific claims characteristics \n \
        Returns --> a df with the KPIs (frequency, projected loss ratios, etc.) derived 
    """   
    
    projected_capped_cost = df[capped_claims_column_name]
    count_claims = df[claim_count_column_name]

    try:
        cost_ibnr = triangle_costs.iloc[:, -1]
        count_ibnr = triangle_counts.iloc[:, -1]
        cost_ibnr_loading,  count_ibnr_loading= 0, 0

        if analysis_year_level == 'occurrence' and len(portfolio_group_by) == 0 and len(claims_group_by) == 0:

            length_diff = df.shape[0] - len(cost_ibnr)

            # This can happen for example in an analysis by occurrence year where the first claim occurrs the year after the business started
            if length_diff > 0:
                cost_ibnr, count_ibnr = list(cost_ibnr), list(count_ibnr)
                [cost_ibnr.insert(0, 0) for i in range(0, length_diff)]
                [count_ibnr.insert(0, 0) for i in range(0, length_diff)]     

        else:
            cost_ibnr_loading = cost_ibnr.sum() / df[capped_claims_column_name].sum()
            count_ibnr_loading = count_ibnr.sum() / df[df[capped_claims_column_name] > 0].count()                

    except:
        cost_ibnr, count_ibnr, cost_ibnr_loading,  count_ibnr_loading= 0, 0, 0, 0

    # Creates the dependant variables that we will try to predict       
    
    projected_capped_cost = projected_capped_cost + (cost_ibnr_loading * projected_capped_cost if cost_ibnr_loading > 0 else cost_ibnr)
    count_claims = count_claims + (count_ibnr_loading * projected_capped_cost if count_ibnr_loading > 0 else count_ibnr)
    df[capped_claims_column_name] = projected_capped_cost
    df[claim_count_column_name] = count_claims 

    # It creates a summary table with more kpis to display
    if table_for_prediction == False:
        
        # If aggregated by both portfolio features and claims attributes, no total is displayed as it does not make sense (exposure, premiums are the same all along the rows and will be summed multiple times). Only costs can be summed by claims attributes such as the guarantee impacted.
        if (len(portfolio_group_by) > 0 and len(claims_group_by) == 0) or (len(portfolio_group_by) == 0 and len(claims_group_by) == 1) or (df.index.name is not None and 'year' in df.index.name):
            df = derive_totals_analysis(df, portfolio_kpis, portfolio_group_by, claims_group_by)
            projected_capped_cost, count_claims = df[capped_claims_column_name], df[claim_count_column_name]

            if isinstance(cost_ibnr, list) == True:
                cost_ibnr.insert(len(cost_ibnr), sum(cost_ibnr))
                count_ibnr.insert(len(count_ibnr), sum(count_ibnr))

        df['observed_full_loss_ratio'] = df[full_claims_column_name] / df[earned_premium_column_name]
        df['observed_capped_loss_ratio'] = df[capped_claims_column_name] / df[earned_premium_column_name]
    
    else:        
        df['claim_occurred'] = np.where(count_claims > 0, 1, 0)
        df['number_claims'] = count_claims

    df['projected_capped_cost'] = projected_capped_cost
    df['projected_capped_loss_ratio'] = projected_capped_cost / df[earned_premium_column_name]
    df['projected_full_loss_ratio'] = df['projected_capped_loss_ratio'] * (1 + LL_loading) 
    
    loss_ratio_adjusted_for_comm = df['projected_full_loss_ratio'] * (1 - new_comm) / (1 - current_comm)                
    df['necessary_rate_adjusment'] = loss_ratio_adjusted_for_comm / target_LR_new_comm -1

    df['frequency'] = count_claims / df[exposure_column_name] 
    df['average_cost'] = projected_capped_cost / count_claims
    df['pure_premium_capped_claims'] = projected_capped_cost / df[exposure_column_name]
    df['pure_premium_full_claims'] = df['pure_premium_capped_claims'] * (1 + LL_loading)    
    df['proposed_gwp_excl_taxes'] = df['pure_premium_full_claims'] / target_LR_new_comm     
    
    return df


def derive_totals_analysis(df, portfolio_kpis, portfolio_group_by, claims_group_by):
    """ Derives the totals amounts from a summary table \n \
        Arguments --> the dataframe, the kpis on which the total sums must be derived \n \
            the segmentation, i.e. on which features the analysis will be performed \n \
            the claims attributes if the profitability results must be done on specific claims characteristics \n \
        Returns --> the modified df with an additional row corresponding to the totals
    """

    # These lines create the last line of the table that is the total sum
    df_reset_index = df.reset_index()
    group_by_length = df_reset_index.shape[1] - df.shape[1]

    # Analysis done only on portfolio features or by either occurrence/inception/effective year
    if (portfolio_group_by is not None and len(portfolio_group_by) > 0) or (group_by_length == 1 and 'year' in df.index.name):
        # Figures are derived depending on only one portfolio feature
        if group_by_length == 1:
            df.loc['Total'] = df.sum()

        # The summary table is aggregated on multiple variables
        else:
            columns = df_reset_index.select_dtypes(include=['category', 'interval']).columns
            df_reset_index[columns] = df_reset_index[columns].astype(str)

            # Takes only the columns corresponding to the variables that served to aggregate
            columns = df_reset_index.columns[:group_by_length]
            # Set the value Total at the bottom of each of these columns
            for column_name in columns:
                df_reset_index.loc[df.shape[0], column_name] = 'Total'

            # Derives the total sum over the rows and affect it to the columns of the summary table except the ones that initially served for aggregation
            df_reset_index.loc[df.shape[0], group_by_length:] = df.sum()

            # We put back on index the variables that segment out analysis
            df = df_reset_index.set_index(list(columns))

    # Analysis done on just one claim attribute. (Code will be improved later to sum the porfolio kpis through many claims attributes)
    else:
        # Gets only portfolio kpis (exposure, gwp and gep)
        df_portfolio_kpis_sum = df.loc[df.index[df.shape[0]-1]][portfolio_kpis]
        # Sums the claims kpis (reserves, costs)
        claims_sum = df.iloc[:, len(df_portfolio_kpis_sum):].sum()
        # Concatenate both totals of porfolio and claims kpis
        concat = pd.concat((df_portfolio_kpis_sum, claims_sum)).values

        # Resets the index so that we can create a new row as Total
        df_reset_index = df.reset_index()
        df_reset_index.loc[df_reset_index.shape[0], claims_group_by] = 'Total'
        # Sets back the index, otherwise the concat created above will not have the same length
        df_reset_index = df_reset_index.set_index(claims_group_by)
        # Affects to the row the concat values, i.e. premiums, costs totals
        df_reset_index.loc[df_reset_index.index[df_reset_index.shape[0]-1]] = concat
        df = df_reset_index

    return df

# %%
