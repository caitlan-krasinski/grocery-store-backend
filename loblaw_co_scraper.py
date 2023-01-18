''' 
NOTES: each page will have its own unique XPATHS and I suspect it could break in the 
future but for now we will go with it will need to gather all unique XPATHS 
some sleep times are longer to ensure the driver doesn't seach before a page is 
fully loaded 
'''


# IMPORTS 
import pandas as pd
import time 
from bs4 import BeautifulSoup
import scrapers.scraper as scraper

# variable store 
store_vars = { 
              'zehrs_produce':{'store':'zehrs',
                    'category_name':'produce',
                    'link':'https://www.zehrs.ca/food/fruits-vegetables/c/28000?navid=flyout-L2-fruits-vegetables',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[6]/div/div[2]/div[4]/div/button'}
                , 'zehrs_dairy_and_egg':{'store':'zehrs',
                    'category_name':'dairy_and_eggs',
                    'link':'https://www.zehrs.ca/food/dairy-eggs/c/28003?navid=flyout-L2-Dairy-and-Eggs',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button'}
                , 'zehrs_meat':{'store':'zehrs',
                    'category_name':'meat',
                    'link':'https://www.zehrs.ca/food/meat/c/27998?navid=flyout-L2-Meat',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button'}
                , 'zehrs_bakery':{'store':'zehrs',
                    'category_name':'bakery',
                    'link':'https://www.zehrs.ca/food/bakery/c/28002?navid=flyout-L2-Bakery',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button'}
                , 'zehrs_seafood':{'store':'zehrs',
                    'category_name':'seafood',
                    'link':'https://www.zehrs.ca/food/fish-seafood/c/27999?navid=flyout-L2-Fish-and-Seafood',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button'}
                , 'valu_mart_produce':{'store':'valu_mart',
                    'category_name':'produce',
                    'link':'https://www.valumart.ca/food/fruits-vegetables/c/28000?navid=flyout-L2-fruits-vegetables',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[6]/div/div[2]/div[4]/div/button'}
                , 'valu_mart_dairy_and_egg':{'store':'valu_mart',
                    'category_name':'dairy_and_eggs',
                    'link':'https://www.valumart.ca/food/dairy-eggs/c/28003?navid=flyout-L2-Dairy-and-Eggs',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button'}
                , 'valu_mart_meat':{'store':'valu_mart',
                    'category_name':'meat',
                    'link':'https://www.valumart.ca/food/meat/c/27998?navid=flyout-L2-Meat',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button'}
                , 'valu_mart_bakery':{'store':'valu_mart',
                    'category_name':'bakery',
                    'link':'https://www.valumart.ca/food/bakery/c/28002?navid=flyout-L2-Bakery',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button'}
                , 'valu_mart_seafood':{'store':'valu_mart',
                    'category_name':'seafood',
                    'link':'https://www.valumart.ca/food/fish-seafood/c/27999?navid=flyout-L2-Fish-and-Seafood',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button'}
                , 'no_frills_produce':{'store':'no_frills',
                    'category_name':'produce',
                    'link':'https://www.nofrills.ca/food/fruits-vegetables/c/28000?navid=flyout-L2-fruits-vegetables',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[6]/div/div[2]/div[4]/div/button'}
                , 'no_frills_dairy_and_egg':{'store':'no_frills',
                    'category_name':'dairy_and_eggs',
                    'link':'https://www.nofrills.ca/food/dairy-eggs/c/28003?navid=flyout-L2-Dairy-and-Eggs',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button'}
                , 'no_frills_meat':{'store':'no_frills',
                    'category_name':'meat',
                    'link':'https://www.nofrills.ca/food/meat/c/27998?navid=flyout-L2-Meat',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button'}
                , 'no_frills_bakery':{'store':'no_frills',
                    'category_name':'bakery',
                    'link':'https://www.nofrills.ca/food/bakery/c/28002?navid=flyout-L2-Bakery',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button'}
                , 'no_frills_seafood':{'store':'no_frills',
                    'category_name':'seafood',
                    'link':'https://www.nofrills.ca/food/fish-seafood/c/27999?navid=flyout-L2-Fish-and-Seafood',
                    'load_more_xpath':'//*[@id="site-content"]/div/div/div[5]/div/div[2]/div[4]/div/button' }
}


# START RUN 
start_time = time.time()


# SET OPTIONS 
options = scraper.set_options()
options.add_argument('--ignore-certificste-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

# STARTUP DRIVER 
driver = scraper.initiate_driver(options)

# run each store for each department 
for store_prod in store_vars.keys():
    print(f'Starting {store_prod}')

    store_details = store_vars[store_prod]

    scraper.nav_to_page(driver, store_details['link'])

    time.sleep(8) # wait for page load 

    scraper.close_cookies_blocker(driver, '//*[@id="privacy-policy"]/div/div/button')

    time.sleep(5) # wait for page load 

    scraper.click_load_more(driver, store_details['load_more_xpath'])

    time.sleep(5) # wait for page load 

    scraper.check_that_bottom_is_reached(driver, store_details['load_more_xpath'])

    # extract html
    page_source = scraper.grab_html(driver)
    soup = BeautifulSoup(page_source, 'lxml')

    # find all product divs for that page 
    product_divs = soup.find_all("div", {"class": "product-tracking"})

    # initialize data frame
    df = pd.DataFrame(columns = ['category', 'brand', 'product_text', 'product_name', 'price_text', 'sale_price', 'per_unit_price_text', 'is_sale'])

    # iterate through each prod div and collect name, price and per_unit_price
    for div in product_divs:
        prod_details = div.find_all("div", {"class": "product-tile__details"})
        
        name = prod_details[0].find_all("h3", {"class": "text text--small4 text--left text--default-color product-tile__details__info__name"})[0].text

        try: # ex: fruit doesnt have a brand so allow pass 
            brand = prod_details[0].find_all("span", {"class": "product-name__item product-name__item--brand"})[0].text
        except:
            brand = ''

        # deal_badge = prod_details[0].find_all("div", {"class": "product-tile-deal-badge"})

        # try: 
        #     sale_badge = deal_badge[0].find_all("div", {"class": "product-badge__icon product-badge__icon--sale product-badge__icon--product-tile"})[0]
        #     # sale_text = sale_badge[0].find_all("div", {"class": "product-badge__icon__text product-badge__icon__text--sale"})[0]
        #     sale = True
        # except: 
        #     sale = False 

        product = prod_details[0].find_all("span", {"class": "product-name__item product-name__item--name"})[0].text
        
        prod_details = prod_details[0].find_all("div", {"class": "product-tile__details__info__section"})
        prod_info = prod_details[0].find_all("div", {"class": "product-prices product-prices--product-tile"})

        # if sale: 
        try:
            # if there is a was-price tag then it is on sale currently 
            price_text = prod_info[0].find_all("span", {"class": "price selling-price-list__item__price selling-price-list__item__price--was-price"})[0].text
            sale_price = prod_info[0].find_all("span", {"class": "price selling-price-list__item__price selling-price-list__item__price--now-price"})[0].text
            sale = True
        except:
            price_text = prod_info[0].find_all("span", {"class": "price selling-price-list__item__price selling-price-list__item__price--now-price"})[0].text
            sale_price = None
            sale = False

        try: # some items don't have a per unit price
            per_unit_price_text = prod_info[0].find_all("span", {"class": "price comparison-price-list__item__price"})[0].text
        except:
            per_unit_price_text = None

        
        # append data to df 
        df = df.append({'category': store_details['category_name'], 
                        'brand' : brand, 
                        'product_text' : product, 
                        'product_name': name, 
                        'price_text': price_text,
                        'sale_price': sale_price,
                        'per_unit_price_text': per_unit_price_text,
                        'is_sale': sale}
                    , ignore_index=True)

        df.to_csv(f'raw_data/{store_details["store"]}/{store_details["category_name"]}.csv', index=False)

    print(f'completed {store_prod} \n\n')

