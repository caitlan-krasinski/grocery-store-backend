'''
Flipp flyer scraper v2 powered by requests 
Selenium to scrape item ids
requests to call backend url of flipp to collect metadata 

reference: https://gist.github.com/jQwotos/37c54992881824d7084680ee91c9633c 
'''

# IMPORTS 
import pandas as pd
import time 
import scrapers.scraper as scraper
import flipp_scraper_functions 


flyer_vars = { 'freshco':{'store':'freshco',
                    'link': 'https://flipp.com/en-ca/waterloo-on/flyer/5325015-freshco-weekly-eflyer-11171123?postal_code=N2J4L6'}
            , 'walmart':{'store':'walmart', # need to double check walmart data each week 
                    'link':'https://flipp.com/en-ca/waterloo-on/flyer/5426645-walmart-flyer?postal_code=N2J4L6'}
            , 'sobeys':{'store':'sobeys',
                    'link':'https://flipp.com/en-ca/waterloo-on/flyer/5329089-sobeys-weekly-flyer-ontario?postal_code=N2J4L6'}
            , 'food_basics':{'store':'food_basics',
                    'link':'https://flipp.com/en-ca/waterloo-on/flyer/5326814-food-basics-flyer?postal_code=N2J4L6'}
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


    df = pd.DataFrame()

    # make request for each item id 
    for item in items:
        item_json = flipp_scraper_functions.scrape_item(item)['item']
        df = df.append(item_json, ignore_index=True)

    # save data
    df = df[['merchant'
        , 'brand'
        , 'name'
        , 'description'
        , 'current_price'
        , 'pre_price_text'
        , 'price_text'
        , 'sku'
        , 'flyer_valid_from'
        , 'flyer_valid_to'
        , 'image_url' ]] 
    df.to_csv(f'raw_data/{flyer["store"]}/flyer_deals.csv', index=False)

    print(f'completed {flyer["store"]} in {(time.time() - start_time)} \n')

driver.close() # close driver window 