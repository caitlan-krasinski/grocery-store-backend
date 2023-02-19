import pandas as pd
from scipy import stats
import random

stores = ['freshco', 'sobeys', 'food_basics', 'walmart']

def generate_scaling_factors(study_data):
    '''geometric mean of % diff values to be our _scaling_factor_'''

    departments = study_data.department.unique()

    factors = pd.DataFrame()

    for department in departments:
        df = study_data[study_data['department'] == department]

        for store in stores: 

            geo_mean = stats.gmean(df[f'{store} % difference'], axis=0, dtype=None)

            if department == 'meat + seafood':
                factors = factors.append({'store':store, 'department':'meat', 'geo_mean':geo_mean}, ignore_index=True)
                factors = factors.append({'store':store, 'department':'seafood', 'geo_mean':geo_mean}, ignore_index=True)
            elif department == 'home goods':
                factors = factors.append({'store':store, 'department':'household_items', 'geo_mean':geo_mean}, ignore_index=True)
            elif department == 'dairy':
                factors = factors.append({'store':store, 'department':'dairy_and_eggs', 'geo_mean':geo_mean}, ignore_index=True)
            elif department == 'dry goods':
                factors = factors.append({'store':store, 'department':'pantry', 'geo_mean':geo_mean}, ignore_index=True)
                factors = factors.append({'store':store, 'department':'snacks', 'geo_mean':geo_mean}, ignore_index=True)
                factors = factors.append({'store':store, 'department':'drinks', 'geo_mean':geo_mean}, ignore_index=True)
                factors = factors.append({'store':store, 'department':'frozen', 'geo_mean':geo_mean}, ignore_index=True)
            else:
                factors = factors.append({'store':store, 'department':department, 'geo_mean':geo_mean}, ignore_index=True)

    return factors 


study = pd.read_csv('empirical study.csv')
baseline = pd.read_csv('clean_data/zehrs/zehrs_data.csv')

factors = generate_scaling_factors(study)


for store in stores:
    globals()[f"{store}_synthetic_data"] = pd.DataFrame()

    for category in factors.department.unique():
        category_data = baseline[baseline['category'] == category]

        columns = category_data.columns

        geo_mean = list(factors.loc[ (factors['store']==store) & (factors['department'] == category) ].geo_mean)[0]
        noise = random.uniform(0, 0.05)
        scaling_factor = geo_mean+noise
        print(store, noise, geo_mean, scaling_factor)
        
        # print(scaling_factor)
        # print(category_data['price'])/
        print(category_data['price'], category_data['price']*scaling_factor)

        category_data['price'] = category_data['price']*scaling_factor
        category_data['per_unit_price'] = category_data['per_unit_price']*scaling_factor
        category_data['sale_price'] = [None]*len(category_data)
        category_data['sale_per_unit_price'] = [None]*len(category_data)
        category_data['store'] = [store]*len(category_data)
        category_data['is_sale'] = [False]*len(category_data)

        category_data = category_data[columns]

        globals()[f"{store}_synthetic_data"] = globals()[f"{store}_synthetic_data"].append(category_data, ignore_index=True)
    
    globals()[f"{store}_synthetic_data"].pop(globals()[f"{store}_synthetic_data"].columns[0])
    globals()[f"{store}_synthetic_data"].to_csv(f'clean_data/{store}/synthetic_data.csv', index=False)



