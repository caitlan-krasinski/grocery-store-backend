'''
Script to generate synthetic data for stores who do not have their item catolog publically available 

PLease reference emperical study plan in the team Notion for more details 

This uses Zehrs data as a baseline and generates a random scaling factor based on the range identified in the 
emperical study 
'''

import pandas as pd 
import random 
import warnings
warnings.filterwarnings("ignore")


stores = {'freshco' : {'produce': [0.51, 00.86]
                    , 'bakery': [0.79, 0.93]
                    , 'dairy_and_eggs': [0.74, 1.07]
                    , 'meat': [0.59, 1.30]
                    , 'seafood': [0.59, 1.30]}
        , 'walmart' : {'produce': [0.0, 0.0]
                    , 'bakery': [0.0, 0.0]
                    , 'dairy_and_eggs': [0.0, 0.0]
                    , 'meat': [0.0, 0.0]
                    , 'seafood': [0.0, 0.0]}
        , 'sobeys' : {'produce': [0.57, 1.33]
                    , 'bakery': [1.0, 1.23]
                    , 'dairy_and_eggs': [0.82, 1.15]
                    , 'meat': [0.84, 1.45]
                    , 'seafood': [0.84, 1.45]}
        , 'food_basics' : {'produce': [0.0, 0.0]
                    , 'bakery': [0.0, 0.0]
                    , 'dairy_and_eggs': [0.0, 0.0]
                    , 'meat': [0.0, 0.0]
                    , 'seafood': [0.0, 0.0]}
    }

baseline = pd.read_csv('clean_data/zehrs/zehrs_data.csv')

for store in stores.keys():
    globals()[f"{store}_synthetic_data"] = pd.DataFrame()
    for category in stores[store].keys():
        category_data = baseline[baseline['category'] == category]

        scaling_factor_range = stores[store][category]

        # can iterate to do random scaling factor for each item but for now keep const across 
        # same cateegory items 
        scaling_factor = random.uniform(scaling_factor_range[0], scaling_factor_range[1])

        category_data.loc[:, 'price'] *= scaling_factor
        category_data.loc[:, 'per_unit_price'] *= scaling_factor
        category_data.loc[:, 'sale_price'] = None
        category_data.loc[:, 'sale_per_unit_price'] = None
        category_data['store'] = store
        category_data['is_sale'] = False

        globals()[f"{store}_synthetic_data"] = globals()[f"{store}_synthetic_data"].append(category_data, ignore_index=True)
    
    globals()[f"{store}_synthetic_data"].pop(globals()[f"{store}_synthetic_data"].columns[0])
    globals()[f"{store}_synthetic_data"].to_csv(f'clean_data/{store}/synthetic_data.csv', index=False)
