from copy import deepcopy

def merge_assumptions_fields(document, dict_figures=None, field_dict_index_name=None, field_dict_value_name=None, unique_figure=None, field_name_unique=None, style_format_dict='{:,.0f}', style_format_unique='{:.2%}'):

    if dict_figures is not None and field_dict_index_name is not None and field_dict_value_name is not None:
        rows = [{field_dict_index_name: str(key.year), field_dict_value_name: style_format_dict.format(dict_figures[key])} for key in dict_figures.keys()]
        document.merge_rows(field_dict_index_name, rows)

    if unique_figure is not None and field_name_unique is not None:
        rows = [{field_name_unique: style_format_unique.format(unique_figure)}]
        document.merge_rows(field_name_unique, rows)

        

def merge_analysis_features_fields(document, df, features):
    """ Merges the analysis summaries done by feature to word"""

    new_features = [features] if isinstance(features, str) == True else features

    for index, feature in enumerate(new_features):
        merge_analysis_fields(document, df, 'analysis_variable_' + str(index+1), feature=feature)

        if index == len(new_features) - 1:
            print('The merge function successfully worked. The analysis word fields have been merged with the performance analysis done for the specified features.')

            

def merge_analysis_fields(document, df, first_column_name, exposure_name='exposure', written_premium_name='asif_written_premium_excl_taxes', earned_premium_name='asif_earned_premium', feature=None):
    """
        Merges the analysis summaries to word fields
        Arguments --> the df, the word field name and the feature if it is a performance analysis by feature
    """

    if first_column_name == 'analysis_total':
        total_name = 'Total'
        rows = [
            {
                first_column_name: 'Total',
                'analysis_exposure': '{:,.0f}'.format(df.loc[total_name, exposure_name]),
                'analysis_gwp': '{0:,.0f} {1}'.format(df.loc[total_name, written_premium_name], currency),
                'analysis_gep': '{0:,.0f} {1}'.format(df.loc[total_name, earned_premium_name], currency),
                'analysis_observed_capped_loss_ratio': '{:.2%}'.format(df.loc[total_name, 'observed_capped_loss_ratio']),
                'analysis_observed_full_loss_ratio': '{:.2%}'.format(df.loc[total_name, 'observed_full_loss_ratio']),
                'analysis_projected_capped_cost': '{0:,.0f} {1}'.format(df.loc[total_name, 'projected_capped_cost'], currency),
                'analysis_projected_capped_loss_ratio': '{:.2%}'.format(df.loc[total_name, 'projected_capped_loss_ratio']),
                'analysis_projected_full_loss_ratio': '{:.2%}'.format(df.loc[total_name, 'projected_full_loss_ratio']),
                'analysis_necessary_rate_adjusment': '{:.2%}'.format(df.loc[total_name, 'necessary_rate_adjusment']),
                'analysis_frequency': '{:.2%}'.format(df.loc[total_name, 'frequency']),
                'analysis_average_cost': '{0:,.0f} {1}'.format(df.loc[total_name, 'average_cost'], currency),
                'analysis_pure_premium_excl_LL': '{0:,.0f} {1}'.format(df.loc[total_name, 'pure_premium_excl_LL'], currency),
                'analysis_pure_premium_incl_LL': '{0:,.0f} {1}'.format(df.loc[total_name, 'pure_premium_incl_LL'], currency),
                'analysis_proposed_gwp': '{0:,.0f} {1}'.format(df.loc[total_name, 'proposed_gwp_excl_taxes'], currency)
            }
        ]

        document.merge_rows(first_column_name, rows)

    else:
        new_df = deepcopy(df) if feature is None else df[feature]
        loop_values = new_df.index
        rows = [
            {
                first_column_name: str(value),
                'analysis_exposure': '{:,.0f}'.format(new_df.loc[value][exposure_name]),
                'analysis_gwp': '{0:,.0f} {1}'.format(new_df.loc[value][written_premium_name], currency),
                'analysis_gep': '{0:,.0f} {1}'.format(new_df.loc[value][earned_premium_name], currency),
                'analysis_projected_capped_loss_ratio': '{:.2%}'.format(new_df.loc[value]['projected_capped_loss_ratio']),
                'analysis_projected_full_loss_ratio': '{:.2%}'.format(new_df.loc[value]['projected_full_loss_ratio']),
                'analysis_necessary_rate_adjusment': '{:.2%}'.format(new_df.loc[value]['necessary_rate_adjusment']),
                'analysis_frequency': '{:.2%}'.format(new_df.loc[value]['frequency']),
                'analysis_average_cost': '{0:,.0f} {1}'.format(new_df.loc[value]['average_cost'], currency),
                'analysis_pure_premium_excl_LL': '{0:,.0f} {1}'.format(new_df.loc[value]['pure_premium_excl_LL'], currency),
                'analysis_proposed_gwp': '{0:,.0f} {1}'.format(new_df.loc[value]['proposed_gwp_excl_taxes'], currency)
            }

            for value in loop_values
        ]


        if feature is None:
            document.merge_rows(first_column_name, rows)

        else:
            index = list(df.keys()).index(feature)
            merge_templates = [{
                'analysis_feature_' + str(index+1): feature.replace('feature', '').replace('_', ' ').replace('bins', '').capitalize(),
                first_column_name: rows,
            }]

            document.merge_templates(merge_templates, separator='page_break')

            

def merge_portfolio_fields(document, df, features, num_features_analysis, portfolio_num_features_description=None, termination_rates=None, written_premium_column_name='asif_written_premium_excl_taxes', currency='€'):
    """ Merges the portfolio summary figures to word fields"""
    
    new_df = deepcopy(df)
    new_features = [features] if isinstance(features, str) == True else features
    rows_to_merge2 = None
    
    for index, feature in enumerate(features):

        if portfolio_num_features_description is not None and (feature in num_features_analysis or feature.replace('_bins', '') in num_features_analysis):
            
            if feature not in num_features_analysis:
                # Variables binned have interval/category pandas style. It has to be treated               
                unique_values = new_df[feature].unique().sort_values().astype(str)
                new_df[feature] = new_df[feature].astype(str)  
                
                row1 = 'variable_value_' + str(index+1)
                rows_to_merge1 = [{
                    row1: str(value),
                    'policies_number_by_variable': '{:,.0f}'.format(new_df[new_df[feature] == value].shape[0]),
                    'gwp_by_variable': '{0:,.0f} {1}'.format(new_df[new_df[feature] == value][written_premium_column_name].sum(), currency),
                    'average_gwp_by_variable': '{0:,.0f} {1}'.format(new_df[new_df[feature] == value][written_premium_column_name].mean(), currency)
                } for value in unique_values]
                
                feature = feature.replace('_bins', '')
            
            row2 = 'average_' + str(index+1)
            rows_to_merge2 = [{
                row2: '{:,.0f}'.format(portfolio_num_features_description.loc['mean', feature]),
                'median': '{:,.0f}'.format(portfolio_num_features_description.loc['50%', feature]),
                'min': '{:,.0f}'.format(portfolio_num_features_description.loc['min', feature]),
                'max': '{:,.0f}'.format(portfolio_num_features_description.loc['max', feature])
            }] 

            
        else:
            row1 = 'variable_value_' + str(index+1)                
            unique_values = new_df[feature].unique()
            
            rows_to_merge1 = [{
                row1: str(value),
                'policies_number_by_variable': '{:,.0f}'.format(new_df[new_df[feature] == value].shape[0]),
                'gwp_by_variable': '{0:,.0f} {1}'.format(new_df[new_df[feature] == value][written_premium_column_name].sum(), currency),
                'average_gwp_by_variable': '{0:,.0f} {1}'.format(new_df[new_df[feature] == value][written_premium_column_name].mean(), currency)
            } for value in unique_values]
        
        if rows_to_merge2 is None:
            merge_templates = [{
                'feature_' + str(index+1): feature.replace('feature', '').replace('_', ' ').capitalize(),
                row1: rows_to_merge1,
            }]
        else:
            merge_templates = [{
                'feature_' + str(index+1): feature.replace('feature', '').replace('_', ' ').capitalize(),
                row1: rows_to_merge1,
                row2: rows_to_merge2
            }] 
            
            rows_to_merge2 = None
        
        
        document.merge_templates(merge_templates, separator='page_break') 
    
    if termination_rates is not None:
        rows = [{'termination_rate_occurrence_year': str(key), 'termination_rate': '{:.1%}'.format(termination_rates[key])} for key in termination_rates.keys()]
        document.merge_rows('termination_rate_occurrence_year', rows)
    
    print('The merge has successfully worked. The word field names have been well merged with the portfolio composition figures.')   