''' 
functions to identify which store(s) or combination stores results in the lowest 
per unit subtotal cost 

Works for any n combinations so long as n <= num_stores
'''

import pandas as pd 
from itertools import combinations


def item_selection(dfs):
    
    # append all dfs
    df = dfs[0]
    dfs.remove(dfs[0])
    for df_n in dfs:
        df = df.append(df_n, ignore_index=True)

    # group by list_items 
    df_grp = df.groupby('list_item')['comparable_price']

    # add col indicating min cost out of the n store dfs 
    df = df.assign(min_cost=df_grp.transform(min))

    # filter rows where the row corresponds to the min cost 
    df = df[df['comparable_price'] == df['min_cost']]

    # take subtotal 
    per_unit_subtotal = sum(df['comparable_price'])

    return df, per_unit_subtotal


def n_store_selection(n, results_dict, results = {}):

    if n >= len(results_dict):
        print(f'{n} combinations not possible for our {len(results_dict)} store selection')
        return {}

    # go through n combination stores 
    possibilities = list(combinations(results_dict.keys(), n))
    for combin in possibilities:
        
        # place all dfs in list 
        dfs = []
        for store in combin:
            df = pd.read_csv(f'search_output/{store}_results.csv')
            dfs.append(df)

        # item selection 
        optimal_selection, per_unit_subtotal = item_selection(dfs)

        # add to results dict 
        results[combin] = per_unit_subtotal

    return results