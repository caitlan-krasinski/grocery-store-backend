'''
Flipp flyer scraper 
Scraping is done entierly in selenium since item details are hidden behind popups
This scraper takes longer since it needs to load each item page  individually 
'''

# IMPORTS 
import pandas as pd
import time 
import scrapers.scraper as scraper

# START RUN 
start_time = time.time()

print('process started')

link  = 'https://flipp.com/en-ca/guelph-on/flyer/5231790-freshco-weekly-eflyer-10061012?postal_code=N1E1A1'

# SET OPTIONS 
options = scraper.set_options()
options.add_argument('--ignore-certificste-errors')
options.add_argument('--incognito')
# options.add_argument('--headless') # cant run headless for some reason 

# STARTUP DRIVER 
driver = scraper.initiate_driver(options)

scraper.nav_to_page(driver, link)

time.sleep(4) # wait for page load 

flyer_items = driver.find_elements_by_class_name('item-container')

items = []
for item in flyer_items:
    itemid = item.get_attribute('itemid')
    if itemid is not None:
        items.append(itemid)

print('collected item ids')

print('collecting item details')

df = pd.DataFrame(columns = ['product_name', 'price'])

for item in items:
    link = f'https://flipp.com/en-ca/guelph-on/item/{item}-freshco-weekly-eflyer-10061012?postal_code=N1E1A1'
    
    scraper.nav_to_page(driver, link)
    
    time.sleep(2)   

    name = driver.find_element_by_xpath('/html/body/flipp-dialog/div/flipp-toast-container/div/flipp-item-dialog/div/h2/span').text
    pre_price_text = driver.find_elements_by_class_name('pre-price-text')
    dollar = driver.find_elements_by_class_name('dollars')
    cents = driver.find_elements_by_class_name('cents')
    price_text = driver.find_elements_by_class_name('price-text')

    if len(pre_price_text) > 0: pre_price_text_str= pre_price_text[0].text
    if len(dollar) > 0: dollar_str= dollar[0].text
    if len(cents) > 0: cents_str= cents[0].text
    if len(price_text) > 0: price_text_str= price_text[0].text

    price = f'{pre_price_text_str}${dollar_str}.{cents_str} {price_text_str}'

     # append data to df 
    df = df.append({'product_name': name, 
                    'price': price,}
                , ignore_index=True)

df.to_csv(f'csv_files/freshco/flyer_deals.csv', index=False)

print(f'completed in {(time.time() - start_time)}')

driver.close()