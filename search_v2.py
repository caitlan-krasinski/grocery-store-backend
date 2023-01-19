'''
Script to search each stores catologe of data for a users specified grocery list 

Format to run:
python search_v2.py <grocery_list>

EX: python search_v2.py "['2% milk', 'Cheddar Cheese', 'white sliced bread']"

'''

# general data 
import pandas as pd

# nltk 
from nltk.stem import PorterStemmer
from nltk.metrics.distance import jaccard_distance

# timing
import time

# reading in cmd arguments
import sys
import ast

# saving data
from pickle import load
import json 

start_time = time.time()

ps = PorterStemmer() # stemming for better results 


# take grocery list from terminal 
grocery_list = ast.literal_eval(sys.argv[1])
n_stores = ast.literal_eval(sys.argv[2])

def search(grocery_list, ps):
    stores = ['zehrs', 'no_frills', 'valu_mart', 'sobeys', 'freshco'] #, 'walmart', 'food_basics']

    # make variables 
    for store in stores:
        globals()[f"{store}_results"] = pd.DataFrame() # dynamically create variable names 

        
    for store in stores: # retrieval for each store 
        
        # load data
        store_data = pd.read_csv(f'clean_data/{store}/{store}_data.csv')

        # load index
        globals()[f"{store}_index"] = load(open(f"catalogue_index/{store}_index.pkl",'rb'))
        
        final_selection = pd.DataFrame(columns = ['list_item', 'store', 'product_name', 'price', 'per_unit_price', 'is_sale'])
        
        for item in grocery_list:
            item_selection = pd.DataFrame(columns = ['list_item', 'store', 'product_name', 'price', 'per_unit_price', 'is_sale'])

            stem_item = ps.stem(item).lower()
            idxs = []

            for word in stem_item.split():
                try: # list item word not in index
                    word_idxs = globals()[f"{store}_index"][word]
                    idxs.extend(word_idxs)
                except: continue

            if not idxs: # no indicies returned
                store_df = pd.DataFrame() # no results: return empty df
            else:
                store_df = store_data.iloc[idxs]


            ##### search items #####
            for index, row in store_df.iterrows():
                
                product_name = row['product']
                is_sale = row.is_sale

                if is_sale:
                    price = row.sale_price
                    per_unit_price = row.sale_per_unit_price
                else:
                    price = row.price
                    per_unit_price = row.per_unit_price

                # similarity = jaccard_similarity(stem_item.split(' '), ps.stem(product_name).lower().split(' '))
                similarity = jaccard_distance(set(stem_item.lower().split(' ')), set(ps.stem(product_name).lower().split(' ')))
        
                if similarity >= 0.5: # can tweak threshold but this is a good one for now  
                    data = { 'list_item':item, 'store':store, 'product_name':product_name, 'price':price, 'per_unit_price':per_unit_price, 'similarity':similarity, 'is_sale': is_sale}
                    item_selection = item_selection.append(data, ignore_index=True)    
           
            try:
                # find lowest price from top similarities
                cheapest_item = item_selection.sort_values(by=['per_unit_price', 'similarity'], ascending = [True, False])

                final_selection = final_selection.append(dict(cheapest_item.iloc[0]), ignore_index=True)
            except: continue
                
        globals()[f"{store}_results"] = final_selection
    
        # dump results to csv 
        globals()[f"{store}_results"].to_csv(f'search_output/{store}_results.csv')
    
    return {'zehrs': zehrs_results
        , 'no_frills': no_frills_results
        , 'valu_mart': valu_mart_results
        , 'walmart': walmart_results
        , 'sobeys': sobeys_results
        , 'freshco': freshco_results
        , 'food_basics': food_basics_results}


def find_n_cheapest_stores(n, results):
    per_unit_subtotals = {}
    subtotals = {}
    cheapest_stores = {}

    for store in results.keys():
        result = results[store]
        per_unit_subtotal = round(result.per_unit_price.sum(),3)
        subtotal = round(result.price.sum(),3)

        per_unit_subtotals[store] = per_unit_subtotal
        subtotals[store] = subtotal

    for i in range(n):
        min_store = min(per_unit_subtotals, key=per_unit_subtotals.get)
        
        cost = subtotals[min_store]

        cheapest_stores[i+1] = {'store':store
                            , 'file_name': f'{store}_results.csv'
                            , 'subtotal': cost}

        per_unit_subtotals.pop(min_store)
    
    return cheapest_stores


def generate_metadata_file(metadata):
    with open("search_output/metadata.json", "w") as write_file:
        json.dump(metadata, write_file, indent=4)


results_dict = search(grocery_list, ps)

metadata = find_n_cheapest_stores(3, results_dict)

generate_metadata_file(metadata)
    
print(f'completed in {time.time() - start_time} seconds')
print('results in csv results and metadata file in search_output folder')