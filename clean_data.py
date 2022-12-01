import re
import pandas as pd 


def clean_loblaw_co_data(df):
    prices = []
    units = []
    for index, row in df.iterrows():
        s = row.price
        s = re.findall('(?:[\£\$\€]{1}[,\d]+.?\d*)',s)[-1]
        s = s.replace('$', '') # remove $
        prices.append(s)
        
        unit = row.price
        try: unit = unit.split('/')[1]
        except: unit = None
        units.append(unit)
        
        try: float(s)
        except:print(s)
            
    df['price2'] = prices
    df['units'] = units

    return df
        


def clean_flipp_data(df):
    prices = []
    drop_items = []
    units = []
    for index, row in df.iterrows():
        s = row.price
        
        price = ''
        unit = ''
        
        # remove items that aren't groceries or for general pop 
        if '*' in s: drop = 1 # electronics 
        elif 'Scene+' in s: drop = 1 # offer not avail to everyone
        elif 'when you' in s: drop = 1 # offer not avail to everyone
        else: drop = 0
            
        # multiple units for deal  
        if '/$' in s: 
            num = int(s.split('/')[0])
            price_txt = re.findall('(?:[\£\$\€]{1}[,\d]+.?\d*)',s)[-1]
            price = float(price_txt.replace('$', ''))
            price = price/num
            price = round(price,2)
        
        try:
            price_txt = re.findall('(?:[\£\$\€]{1}[,\d]+.?\d*)',s)[-1] # take last price if multiple prices listed since it is the single unit price 
            price = price_txt.replace('$', '')
        except: 
            price = None
            drop = 1
        
        
        # see if there are units 
        try: 
            unit = re.findall('(?:[/lbkgml]+)',s)[-1]
            if unit == '/': unit = None
        except: unit = None
        
        prices.append(price)
        units.append(unit)
        drop_items.append(drop)
        
    #     if drop == 0:
    #         try: float(price)
    #         except:print(price)
            
    df['price2'] = prices
    df['units'] = units
    df['drop_col'] = drop_items 
    df = df[df['drop_col'] == 0]
    df = df.drop(columns=['drop_col'])  

    return df  


print('cleaning data')

# loblaw co
for store in ['zehrs', 'no_frills', 'valu_mart']:
    dairy = pd.read_csv(f'raw_data/{store}/dairy_and_eggs.csv')
    bakery = pd.read_csv(f'raw_data/{store}/bakery.csv')
    meat = pd.read_csv(f'raw_data/{store}/meat.csv')
    produce = pd.read_csv(f'raw_data/{store}/produce.csv')
    seafood = pd.read_csv(f'raw_data/{store}/seafood.csv')

    store_df = pd.DataFrame()
    store_df = store_df.append(dairy)
    store_df = store_df.append(bakery)
    store_df = store_df.append(meat)
    store_df = store_df.append(produce)
    store_df = store_df.append(seafood)
    store_df['store'] = store 

    df = clean_loblaw_co_data(store_df)
    df.to_csv(f'clean_data/{store}/regular_prices.csv', index=False)

print('done cleaning loblaw co')

for store in ['freshco', 'walmart', 'sobeys', 'food_basics', 'zehrs', 'valu_mart', 'no_frills']:
    store_df = pd.read_csv(f'raw_data/{store}/flyer_deals.csv')

    df = clean_flipp_data(store_df)
    df.to_csv(f'clean_data/{store}/flyer_deals.csv', index=False)

print('done cleaning flipp data')



    