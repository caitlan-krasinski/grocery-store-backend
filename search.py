import pandas as pd
from nltk.stem import PorterStemmer
import time
from pickle import load

# packages for alt sim scoring 
# import spacy
# from sentence_similarity import sentence_similarity
# from math import sqrt

def jaccard_similarity(x,y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)


start_time = time.time()

ps = PorterStemmer() # stemming for better results 

grocery_list = ['2% milk', 'Cheddar Cheese', 'white sliced bread', 'ground beef', 
                'clementines', 'chicken breast', 'potatoes']


def search(grocery_list, ps):
    stores = ['zehrs', 'no_frills', 'valu_mart']

    # make variables 
    for store in stores:
        globals()[f"{store}_results"] = pd.DataFrame() # dynamically create variable names 

        
    for store in stores:
        
        # load data
        regular_priced = pd.read_csv(f'clean_data/{store}/regular_prices.csv')
        flyer = pd.read_csv(f'clean_data/{store}/flyer_deals.csv')

        # load index
        globals()[f"{store}_regular_index"] = load(open(f"catalogue_index/{store}_regular_index.pkl",'rb'))
        globals()[f"{store}_flyer_index"] = load(open(f"catalogue_index/{store}_flyer_index.pkl",'rb'))
        
        final_selection = pd.DataFrame(columns = ['list_item', 'store', 'product_name', 'price', 'per_unit_price', 'source'])
        
        for item in grocery_list:
            item_selection = pd.DataFrame(columns = ['list_item', 'store', 'product_name', 'price', 'per_unit_price', 'source'])

            stem_item = ps.stem(item).lower()
            reg_idxs = []
            flyer_idxs = []

            for word in stem_item.split():
                try: # list item word not in index
                    word_idxs = globals()[f"{store}_regular_index"][word]
                    reg_idxs.extend(word_idxs)
                except: continue

            if not reg_idxs: # no indicies returned
                reg_df = pd.DataFrame() # no results: return empty df
            else:
                reg_df = regular_priced.iloc[reg_idxs]
            
            
            for word in stem_item.split():
                try: # list item word not in index
                    word_idxs = globals()[f"{store}_flyer_index"][word]
                    flyer_idxs.extend(word_idxs)
                except: continue

            if not flyer_idxs: # no indicies returned
                flyer_df = pd.DataFrame() # no results: return empty df
            else:
                flyer_df = regular_priced.iloc[flyer_idxs]


            for index, row in reg_df.iterrows():
                product_name = row['product'].split(',')[0]
                per_unit_price = row['per_unit_price2']
                price = row['price2']

                similarity = jaccard_similarity(stem_item.split(' '), ps.stem(product_name).lower().split(' '))
        
                if similarity >= 0.5: # can tweak threshold but this is a good one for now  
                    data = { 'list_item':item, 'store':store, 'product_name':product_name, 'price':price, 'per_unit_price':per_unit_price, 'similarity':similarity, 'source': 'reg' }
                    item_selection = item_selection.append(data, ignore_index=True)
                    
                    
            ##### search flyer data #####
            for index, row in flyer_df.iterrows():

                try: 
                    product_name = row['product_name'].replace(',', '')
                    price = row['price2']
                    per_unit_price = row.per_unit_price2

                    # find items  
                    similarity = jaccard_similarity(stem_item.split(' '), ps.stem(product_name).lower().split(' '))

                    if similarity >= 0.5: # can tweak threshold but this is a good one for now  
                        data = { 'list_item':item, 'store':store, 'product_name':product_name, 'price':price, 'per_unit_price': per_unit_price, 'similarity':similarity, 'source': 'flyer' }
                        item_selection = item_selection.append(data, ignore_index=True)
                
                except: continue

            try:
                # find lowest price from top similarities
                
                # ************** need to decide between per unit pricing and total price difference
                # ************** maybe some units need per unit some dont 
                cheapest_item = item_selection.sort_values(by=['per_unit_price', 'similarity'], ascending = [True, False])

                final_selection = final_selection.append(dict(cheapest_item.iloc[0]), ignore_index=True)
            except: continue
                
        globals()[f"{store}_results"] = final_selection
    
        # dump results to csv 
        globals()[f"{store}_results"].to_csv(f'search_output/{store}_results.csv')
    
    # return [zehrs_results, no_frills_results, valu_mart_results] 

search(grocery_list, ps)
    
print(time.time() - start_time, 'seconds')