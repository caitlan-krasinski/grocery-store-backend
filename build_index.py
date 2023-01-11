''' builds an keyword index for each stores product catalog for more efficient data retrieval'''

import pandas as pd
from nltk.stem import PorterStemmer
from pickle import dump
import os

ps = PorterStemmer() # stemming for better results 

stores = ['zehrs', 'no_frills', 'valu_mart']

# make variables 
for store in stores:
    globals()[f"{store}_regular_index"] = {} # dynamically create variable names 
    globals()[f"{store}_flyer_index"] = {}

for store in stores:

    regular_priced = pd.read_csv(f'clean_data/{store}/regular_prices.csv')
    flyer = pd.read_csv(f'clean_data/{store}/flyer_deals.csv')


    for index, row in regular_priced.iterrows():
        product_name = row['product']

        product = ps.stem(product_name).lower()

        for word in product.split(): 
            if word not in globals()[f"{store}_regular_index"].keys():
                globals()[f"{store}_regular_index"][word] = [index]
            else:
                globals()[f"{store}_regular_index"][word].append(index)

    for index, row in flyer.iterrows():
        product_name = row['product_name']
        
        try: # in case of numbers only in word 
            product = ps.stem(product_name).lower()

            for word in product.split(): 
                if word not in globals()[f"{store}_flyer_index"].keys():
                    globals()[f"{store}_flyer_index"][word] = [index]
                else:
                    globals()[f"{store}_flyer_index"][word].append(index)
        except:
            continue

    # save index 
    dump(globals()[f"{store}_flyer_index"], open(os.path.join('catalogue_index', f'{store}_flyer_index.pkl'), 'wb'))
    dump(globals()[f"{store}_regular_index"], open(os.path.join('catalogue_index', f'{store}_regular_index.pkl'), 'wb'))
    
print('done building indexes')