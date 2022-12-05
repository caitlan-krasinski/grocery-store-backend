import re
import pandas as pd 


def clean_loblaw_co_data(df):
    prices = []
    per_unit_prices = []
    unit_types = []

    for index, row in df.iterrows():
        s = row.price
        s = re.findall('(?:[\£\$\€]{1}[,\d]+.?\d*)',s)[-1]
        s = s.replace('$', '') # remove $
        
        pup = 0
        per_unit_price = row.per_unit_price
        if not isinstance(per_unit_price, float):  # not nan
            unit = per_unit_price.split('/')[1]
            price = float(per_unit_price.split('/')[0].replace('$', '').replace(',', ''))
            unit_type = ''
            if 'kg' in unit: 
                gram = float(unit.split('kg')[0])*1000 # 1000 g in kg
                pup = price / gram
                unit_type = 'g'
            elif 'g' in unit:
                gram = float(unit.split('g')[0])
                pup = price / gram
                unit_type = 'g'
            elif 'ml' in unit:
                ml = float(unit.split('ml')[0])
                pup = price / ml
                unit_type = 'ml'
        else: 
            pup = s
            unit_type = ''
        
        prices.append(s)
        per_unit_prices.append(pup)
        unit_types.append(unit_type)
        
    df['per_unit_price2'] = per_unit_prices
    df['unit_type'] = unit_types
    df['price2'] = prices

    return df
        


def clean_flipp_data(df):
    prices = []
    drop_items = []
    per_unit_prices = []
    unit_types = []
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
        pup = price
        try: 
            unit = re.findall('(?:[/lbkgml]+)',s)[-1] # this may error out in which cas no units 
            
            if unit == '/': unit = None

            if unit is not None:  # not nan
                unit_type = ''
                if 'kg' in unit: 
                    gram = unit.split('kg')[0]
                    if gram == '/': gram = 1
                    pup = float(price) / (float(gram)*1000) # 1000 g in kg
                    unit_type = 'g'
                elif 'g' in unit:
                    gram = unit.split('g')[0]
                    if gram == '/': gram = 1
                    pup = float(price) / float(gram)
                    unit_type = 'g'
                elif 'lb' in unit:
                    gram = unit.split('lb')[0]
                    if gram == '/': gram = 1
                    pup = float(price) / (float(gram)*453.592)
                    unit_type = 'g'
                elif 'ml' in unit:
                    ml = unit.split('ml')[0]
                    if ml == '/': ml = 1
                    pup = float(price) / float(ml)
                    unit_type = 'ml'
                elif 'l' in unit:
                    ml = unit.split('l')[0]
                    if unit == '/': ml = 1
                    pup = float(price) / (float(ml)*1000)
                    unit_type = 'ml'
                else: 
                    pup = price
                    unit_type = None
            else: 
                pup = price
                unit_type = None
        except: 
            pup = price
            unit_type = None
        
        
        prices.append(price)
        per_unit_prices.append(pup)
        unit_types.append(unit_type)    
        drop_items.append(drop)
               
    df['price2'] = prices
    df['per_unit_price2'] = per_unit_prices
    df['unit_type'] = unit_types
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



    