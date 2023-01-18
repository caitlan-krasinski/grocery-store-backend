''' builds an keyword index for each stores product catalog for more efficient data retrieval'''

import pandas as pd
from nltk.stem import PorterStemmer
from pickle import dump
import os

ps = PorterStemmer() # stemming for better results 

stores = ['zehrs', 'no_frills', 'valu_mart', 'walmart', 'sobeys', 'freshco', 'food_basics']

# make variables 
for store in stores:
    globals()[f"{store}_index"] = {} # dynamically create variable names 

for store in stores:

    data = pd.read_csv(f'clean_data/{store}/{store}_data.csv')

    for index, row in data.iterrows():
        product_name = row['product']

        product = ps.stem(product_name).lower()

        for word in product.split(): 
            if word not in globals()[f"{store}_index"].keys():
                globals()[f"{store}_index"][word] = [index]
            else:
                globals()[f"{store}_index"][word].append(index)

    # save index 
    dump(globals()[f"{store}_index"], open(os.path.join('catalogue_index', f'{store}_index.pkl'), 'wb'))
    