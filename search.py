import pandas as pd
import time 
from nltk.stem import PorterStemmer

ps = PorterStemmer() # stemming for better results 


def jaccard_similarity(x,y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)



start_time = time.time()


stores = ['zehrs', 'no_frills', 'valu_mart']

zehrs_results = pd.DataFrame()
no_frills_results = pd.DataFrame()
valu_mart_results = pd.DataFrame()

grocery_list = ['2% milk', 'Cheddar Cheese', 'white sliced bread', 'ground beef', 
                'clementines', 'chicken breast', 'potato', 'shredded cheese', 'ribs']

for store in stores:
    regular_priced = pd.read_csv(f'clean_data/{store}/regular_prices.csv')
    flyer = pd.read_csv(f'clean_data/{store}/flyer_deals.csv')
    
    final_selection = pd.DataFrame(columns = ['list_item', 'store', 'product_name', 'price', 'per_unit_price', 'source'])
    
    for item in grocery_list: 
        item_selection = pd.DataFrame(columns = ['list_item', 'store', 'product_name', 'price', 'per_unit_price', 'source'])
        
        ##### search regular price data #####
        for index, row in regular_priced.iterrows():
            product_name = row['product']
            per_unit_price = row['per_unit_price2']
            price = row['price2']

            # find items  
            similarity = jaccard_similarity(ps.stem(item).lower().split(' '), ps.stem(product_name).lower().split(' '))

            if similarity >= 0.5: # can tweak threshold but this is a good one for now  
                data = { 'list_item':item, 'store':store, 'product_name':product_name, 'price':price, 'per_unit_price':per_unit_price, 'similarity':similarity, 'source': 'reg' }
                item_selection = item_selection.append(data, ignore_index=True)
    
            elif ps.stem(item).lower() in ps.stem(product_name).lower(): # when the similarity fails
                data = { 'list_item':item, 'store':store, 'product_name':product_name, 'price':price, 'per_unit_price':per_unit_price, 'similarity':0.5, 'source': 'reg' }
                item_selection = item_selection.append(data, ignore_index=True)
       
        ##### search flyer data #####
        for index, row in flyer.iterrows():

            try: 
                product_name = row['product_name'].replace(',', '')
                price = row['price2']
                per_unit_price = row.per_unit_price2

                # find items  
                similarity = jaccard_similarity(ps.stem(item).lower().split(' '), pas.stem(product_name).lower().split(' '))
                
                if similarity >= 0.2: # can tweak threshold but this is a good one for now  
                    data = { 'list_item':item, 'store':store, 'product_name':product_name, 'price':price, 'per_unit_price': per_unit_price, 'similarity':similarity, 'source': 'flyer' }
                    item_selection = item_selection.append(data, ignore_index=True)
               
                elif ps.stem(item).lower() in ps.stem(product_name).lower(): # when the similarity fails
                    data = { 'list_item':item, 'store':store, 'product_name':product_name, 'price':price, 'per_unit_price':per_unit_price, 'similarity':0.5, 'source': 'flyer' }
                    item_selection = item_selection.append(data, ignore_index=True)
            except: continue


        try:
            # find lowest price from top similarities
            # ************** need to decide between per unit pricing and total price difference maybe have it be user input / selection
            cheapest_item = item_selection.sort_values(by=['per_unit_price', 'similarity'], ascending = [True, False])

            final_selection = final_selection.append(dict(cheapest_item.iloc[0]), ignore_index=True)
        except: continue

            
    if store == 'zehrs':
        zehrs_results = final_selection
    elif store == 'no_frills':
        no_frills_results = final_selection
    elif store == 'valu_mart':
        valu_mart_results = final_selection  
    
print(time.time() - start_time, 'seconds')