'''
Flipp flyer scraper 
Scraping is done entierly in selenium since item details are hidden behind popups
This scraper takes longer since it needs to load each item page individually 
'''

# IMPORTS 
import pandas as pd
import time 
import scrapers.scraper as scraper


flyer_vars = { 'freshco':{'store':'freshco',
                    'link': 'https://flipp.com/en-ca/waterloo-on/flyer/5325015-freshco-weekly-eflyer-11171123?postal_code=N2J4L6',
                    'item_link':'https://flipp.com/en-ca/waterloo-on/item/{item}-freshco-weekly-eflyer-11171123?postal_code=N2J4L6'}
            , 'walmart':{'store':'walmart',
                    'link':'https://flipp.com/en-ca/waterloo-on/flyer/5324716-walmart-flyer?postal_code=N2J4L6',
                    'item_link':'https://flipp.com/en-ca/waterloo-on/item/{item}-walmart-flyer?postal_code=N2J4L6'}
            , 'sobeys':{'store':'sobeys',
                    'link':'https://flipp.com/en-ca/waterloo-on/flyer/5329089-sobeys-weekly-flyer-ontario?postal_code=N2J4L6',
                    'item_link':'https://flipp.com/en-ca/waterloo-on/item/{item}-sobeys-weekly-flyer-ontario?postal_code=N2J4L6'}
            , 'food_basics':{'store':'food_basics',
                    'link':'https://flipp.com/en-ca/waterloo-on/flyer/5326814-food-basics-flyer?postal_code=N2J4L6',
                    'item_link':'https://flipp.com/en-ca/waterloo-on/item/{item}-food-basics-flyer?postal_code=N2J4L6'}

            # loblaw co stores have to be difficult and add in dat range, this may be something we have to add in each week we run but also
            # can work out a way to dynamically add in flyer ranges 
            , 'zehrs':{'store':'zehrs',
                    'link':'https://flipp.com/en-ca/waterloo-on/flyer/5326328-zehrs-weekly-flyer-valid-thursday-november-17-wednesday-november-23?postal_code=N2J4L6',
                    'item_link':'https://flipp.com/en-ca/waterloo-on/item/{item}-zehrs-weekly-flyer-valid-thursday-november-17-wednesday-november-23?postal_code=N2J4L6'}
            , 'valu_mart':{'store':'valu_mart',
                    'link':'https://flipp.com/en-ca/waterloo-on/flyer/5322987-valumart-weekly-flyer-valid-thursday-november-17-wednesday-november-23?postal_code=N2J4L6',
                    'item_link':'https://flipp.com/en-ca/waterloo-on/item/{item}-valumart-weekly-flyer-valid-thursday-november-17-wednesday-november-23?postal_code=N2J4L6'}
            , 'no_frills':{'store':'no_frills',
                    'link':'https://flipp.com/en-ca/waterloo-on/flyer/5324898-no-frills-weekly-flyer-valid-thursday-november-17-wednesday-november-23?postal_code=N2J4L6',
                    'item_link':'https://flipp.com/en-ca/waterloo-on/item/{item}-no-frills-weekly-flyer-valid-thursday-november-17-wednesday-november-23?postal_code=N2J4L6'}

}

print('process started')


# SET OPTIONS 
options = scraper.set_options()
options.add_argument('--ignore-certificste-errors')
options.add_argument('--incognito')
# options.add_argument('--headless') # cant run headless for some reason 

# STARTUP DRIVER 
driver = scraper.initiate_driver(options)

for flyer_details in flyer_vars.keys():
    # START RUN 
    start_time = time.time()

    flyer = flyer_vars[flyer_details]

    print(f'running {flyer["store"]} flyer')
    link = flyer['link']

    scraper.nav_to_page(driver, link)

    time.sleep(4) # wait for page load 

    # find all item tags 
    flyer_items = driver.find_elements_by_class_name('item-container')

    # iterate through each <a> and get the item ids 
    items = []
    for item in flyer_items:
        itemid = item.get_attribute('itemid')
        if itemid is not None:
            items.append(itemid)

    print('collected item ids')

    print('collecting data')

    df = pd.DataFrame(columns = ['product_name', 'price_text'])

    count=0
    for item in items:

        try: 
            # popup details for each item is located at this link 
            link = eval("f'{}'".format(flyer['item_link']))
            
            scraper.nav_to_page(driver, link)
            
            time.sleep(2)   

            # collect item name and price - all name and pricing data will be left raw 
            name = driver.find_element_by_xpath('/html/body/flipp-dialog/div/flipp-toast-container/div/flipp-item-dialog/div/h2/span').text
            pre_price_text = driver.find_elements_by_class_name('pre-price-text')
            dollar = driver.find_elements_by_class_name('dollars')
            cents = driver.find_elements_by_class_name('cents')
            price_text = driver.find_elements_by_class_name('price-text')

            # make sure each detail is present 
            if len(pre_price_text) > 0: pre_price_text_str= pre_price_text[0].text
            if len(dollar) > 0: dollar_str= dollar[0].text
            if len(cents) > 0: cents_str= cents[0].text
            if len(price_text) > 0: price_text_str= price_text[0].text

            price = f'{pre_price_text_str} ${dollar_str}.{cents_str} {price_text_str}'

            # append data to df 
            df = df.append({'product_name': name, 
                            'price_text': price,}
                        , ignore_index=True)
        except: 
            count+=1
            print(f'{count} failure(s)')
            continue

    # save data 
    df.to_csv(f'raw_data/{flyer["store"]}/flyer_deals.csv', index=False)

    print(f'completed {flyer["store"]} in {(time.time() - start_time)}')

driver.close() # close driver window 