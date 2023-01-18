'''
script to clean flipp data after scraping.
main computational load comes from the per unit price parsing and calculating
'''

import pandas as pd
import re 

def extract_number_unit(text, unit):
    '''
    search for number of lbs/kg/etc involved 
    ex: for "Natrel Fine-Filtered 1%, 2% or Skim Milk 4 L" we want to identify that this product is 4L
    '''
    if re.findall(f'(([0-9]+)-([0-9]+) {unit})', text) != []: # xxx-xxx <unit>
        return int(re.findall(f'(([0-9]+)-([0-9]+) {unit})', text)[0][0].split('-')[0])
    elif re.findall(f'(([0-9]+)\.([0-9]+)-([0-9]+)\.([0-9]+) {unit})', text) != []: # x.x-x.x <unit>
        return float(re.findall(f'(([0-9]+)\.([0-9]+)-([0-9]+)\.([0-9]+) {unit})', text)[0][0].split('-')[0])
    elif re.findall(f'(([0-9]+)\.([0-9]+) {unit})', text) != []: # x.x <unit>
        return float(re.findall(f'(([0-9]+)\.([0-9]+) {unit})', text)[0][0].split(f' {unit}')[0])
    elif re.findall(f'(([0-9]+) {unit})', text) != []: # xxx <unit>
        return int(re.findall(f'(([0-9]+) {unit})', text)[0][0].split(f' {unit}')[0])
    elif re.findall(f'(([0-9]+)-{unit})', text) != []: # xx-<unit>
        return int(re.findall(f'(([0-9]+)-{unit})', text)[0][0].split('-')[0])
    else: # /<unit> or <unit>. from price_text column
        return 1

def per_unit_price(price, text):

    '''
    Calculate per unit pricing for a product 
    either parses from product name or description text or is explicitly given in the price_text column

    Identitfies what unit is used and then performs PUP calc 
    '''

    if text.lower() == 'each':
        pup = price
    elif 'kg' in text:
        unit = '100g'
        number_of_units = extract_number_unit(text, 'kg')
        pup = float(price) / (float(number_of_units)*1000)*100 
    elif 'g' in text:
        unit = '100g'
        number_of_units = extract_number_unit(text, 'g')
        pup = (float(price) / float(number_of_units))*100 
    elif 'lb' in text or 'LB' in text:
        unit = '100g'
        number_of_units = extract_number_unit(text.lower(), 'lb')
        pup = float(price) / (float(number_of_units)*453.592)*100 # 453.592 g in 1 lb 
    elif 'L' in text:
        unit = '100ml'
        number_of_units = extract_number_unit(text, 'L')
        pup = float(price) / (float(number_of_units)*1000)*100
    elif 'ml' in text:
        unit = '100ml'
        number_of_units = extract_number_unit(text, 'ml')
        pup = (float(price) / float(number_of_units))*100
    elif "'s'" in text: # ex: 5's
        unit = 'packs'
        number_of_units = extract_number_unit(text, "'s'")
        pup = float(price) / (float(number_of_units))
    elif 'pk' in text:  # ex: 5 pk
        unit = 'packs'
        number_of_units = extract_number_unit(text, 'pk')
        pup = float(price) / (float(number_of_units))
    elif 'pack' in text: # ex: 5 pack 
        unit = 'packs'
        number_of_units = extract_number_unit(text, 'pack')
        pup = float(price) / (float(number_of_units))
    else: # no applicable units
        number_of_units = 1
        unit = None
        pup = price 
        
    return pup, unit


## CLEAN 

stores = ['freshco', 'walmart', 'food_basics', 'sobeys']

for store in stores: 

    raw_data = pd.read_csv(f'raw_data/{store}/flyer_deals.csv')

    clean_data = pd.DataFrame(columns = ['merchant', 'brand', 'product', 'description', 'current_price', 'per_unit_price', 'units'
                , 'sku', 'flyer_valid_from', 'flyer_valid_to', 'image_url'])

    for index, row in raw_data.iterrows():
        product = row['name']
        description = row['description']
        price = row.current_price 
        multi_deal = row.pre_price_text
        product_unit = row.price_text
            
        # break down price if multi unit deal (ex: 2/ or 3 for)
        if multi_deal == multi_deal: 
            number_of_units_for_deal = int(re.findall(r'[\d]+', multi_deal)[0])
            price = float(price / number_of_units_for_deal)


        # identify per unit pricing 

        if product_unit == product_unit: # explicitly in product_unit col
            pup, unit = per_unit_price(price, product_unit)

        elif re.findall('''((([0-9]+)-([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)\.([0-9]+)-([0-9]+)\.([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)\.([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)-(kg|g|lb|L|ml|pk|pack)))''',product) != []: # parse from product name
            product_units = re.findall('''((([0-9]+)-([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)\.([0-9]+)-([0-9]+)\.([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)\.([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)-(kg|g|lb|L|ml|pk|pack)))''',product)[0][0]
            pup, unit = per_unit_price(price, product_units)  
            
        elif description == description and re.findall('''((([0-9]+)-([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)\.([0-9]+)-([0-9]+)\.([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)\.([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)-(kg|g|lb|L|ml|pk|pack)))''',description) != []: # parse from product desc
            product_units = re.findall('''((([0-9]+)-([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)\.([0-9]+)-([0-9]+)\.([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)\.([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+) (kg|g|lb|L|ml|pk|pack))|(([0-9]+)-(kg|g|lb|L|ml|pk|pack)))''',description)[0][0]
            pup, unit = per_unit_price(price, product_units)  

        else: # no applicable units 
            pup, unit = price, None 

        clean_data = clean_data.append({
                        'merchant': row.merchant, 
                        'brand': row.brand, 
                        'product': product, 
                        'description': row.description, 
                        'price': row.current_price, 
                        'per_unit_price': pup,
                        'units': unit, # unit for pup (ml, g, etc)
                        'sku': row.sku,
                        'flyer_valid_from': row.flyer_valid_from,
                        'flyer_valid_to': row.flyer_valid_to, 
                        'image_url': row.image_url
                    }, ignore_index = True)
    
    # save clean_data 
    clean_data.to_csv(f'clean_data/{store}/flyer_deals.csv')

    