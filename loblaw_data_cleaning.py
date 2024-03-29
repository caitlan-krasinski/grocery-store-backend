'''
script to clean loblaw co stores data after scraping.
'''

import pandas as pd
import re 
from datetime import date

stores = ['zehrs', 'no_frills', 'valu_mart']


def clean_product_name(text, brand):
    # add space after brand 
    try:
        s = text.replace(brand, f'{brand} ')
    except:
        s = text
    
    # search for all numbers with letter directly in front 
    try:
        find_num = re.search('(?<=\w)\d', s)
        # index of that pattern match 
        idx = find_num.start()
        # split on the pattern index 
        return s[:idx] + ' ' + s[idx:]
    except: 
        return text

def clean_date(date_str):
    if date_str == date_str:
        return date_str.split('Ends ')[1]
    else: 
        return None

def get_todays_date():
    today = date.today()
    return today.strftime("%m/%d/%Y")


for store in stores:

    # read in raw data
    categories = ['dairy_and_eggs', 'bakery', 'meat', 'produce', 'seafood', 'pantry', 'snacks', 'drinks', 'frozen', 'household_items']
    raw_data = pd.DataFrame()
    for category in categories:
        try:
            data  = pd.read_csv(f'raw_data/{store}/{category}.csv')
            raw_data = raw_data.append(data)
        except: continue
    raw_data['store'] = store

    clean_data = pd.DataFrame(columns = ['store', 'category', 'brand', 'product', 'full_product_text', 'price', 'sale_price', 'price_unit'
                , 'per_unit_price', 'sale_per_unit_price', 'units', 'price_per_1', 'is_sale'])

    for index, row in raw_data.iterrows():

        is_sale = row.is_sale 
        
        if is_sale:
            price_was = row.price_text
            price = row.sale_price
        else:
            price = row.price_text
            price_was = price

        price_per_1 = '/' not in re.findall('(?<=.[0-9]{2}).*$', price)[0]

        list_price = float(re.findall('(([0-9]+)\.([0-9]+))', price)[0][0])

        if price_per_1:
            price_unit = 'each'
        else: 
            price_unit = re.findall('(?<=.[0-9]{2}).*$', price)[0]

        price = float(re.findall('(([0-9]+)\.([0-9]+))', price)[0][0])
        price_was = float(re.findall('(([0-9]+)\.([0-9]+))', price_was)[0][0])
        
        per_unit_price_text = row.per_unit_price_text

        if per_unit_price_text == per_unit_price_text: 
            # pup, unit = find_per_unit_price(per_unit_price_text)
            pup = float(per_unit_price_text.split('/ ')[0].replace('$', '').replace(',', ''))
            unit = per_unit_price_text.split('/ ')[1]

            # pup for was_price 
            scaling_factor = price / pup
            pup_was = price_was / scaling_factor
        else: # no units
            pup, pup_was, unit = None, None, None


        if not is_sale:
            price, pup = None, None

        full_product_text = clean_product_name(row.product_name, row.brand)
        
        clean_data = clean_data.append({
                        'store': store, 
                        'category': row.category,
                        'brand': row.brand, 
                        'product': row.product_text, 
                        'full_product_text': full_product_text,
                        'list_price': list_price, 
                        'price': price_was,
                        'sale_price':  price,
                        'price_unit': price_unit, 
                        'per_unit_price': pup_was,
                        'sale_per_unit_price': pup,
                        'units': unit,
                        'price_per_1': price_per_1,
                        'is_sale': is_sale,
                        'sale_valid_until': clean_date(row.sale_valid_to), 
                        'data_last_refreshed_at': get_todays_date()
                    }, ignore_index = True)

    clean_data.to_csv(f'clean_data/{store}/{store}_data.csv', index=False)
