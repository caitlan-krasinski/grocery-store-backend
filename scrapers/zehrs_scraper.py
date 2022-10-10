# web scraper for zehrs product data 
# built using selenium and beautiful soup 

# NOTES: each page will have its own unique XPATHS and I suspect it could break in the future but for now we will go with it 
# will need to gather all unique XPATHS 
# some sleep times are longer to ensure the driver doesn't seach before a page is fully loaded 

# IMPORTS 
from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup


# timer
start_time = time.time()

print('process started')

######################################## Scroll to bottom ########################################

# set driver options 
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificste-errors')
options.add_argument('--incognito')
options.add_argument('--headless') # keep commented for testing but can use headless when doing regular runs 

# initiate driver
driver = webdriver.Chrome('/Users/CaitlanKrasinski/Desktop/chromedriver', options=options)

# VARIABLES 
category_name = 'produce'
link = 'https://www.zehrs.ca/food/fruits-vegetables/c/28000?navid=flyout-L2-fruits-vegetables'
load_more_xpath = '//*[@id="site-content"]/div/div/div[6]/div/div[2]/div[4]/div/button'

# nav to link 
# category_name = 'produce'
# fruits_and_vegetables_link = 'https://www.zehrs.ca/food/fruits-vegetables/c/28000?navid=flyout-L2-fruits-vegetables'
driver.get(link)

# close cookies popup 
time.sleep(8) # wait for page load 

# find button and click button 
cookies_block = driver.find_element_by_xpath(xpath='//*[@id="privacy-policy"]/div/div/button').click()
print('closed cookie blocker')

# wait for page load 
time.sleep(5)

# click load more results button until at bottom 
load_more = driver.find_element_by_xpath(load_more_xpath)

count = 0
while True:
    try:
        # click the button
        load_more.click()

        # wait for page load 
        time.sleep(5)

        # re-find the button 
        load_more = driver.find_element_by_xpath(load_more_xpath)

        count+=1
        print(f'{count} page(s) loaded')

    except:
        break

# double check we reached bottom 
time.sleep(5)
try: 
    load_more = driver.find_element_by_xpath(load_more_xpath)
    print('failed run')
except:
    print('reached bottom of page')
    

# extract page source
page_source = driver.page_source

######################################### DATA COLLECTION #########################################

# extract html
soup = BeautifulSoup(page_source, 'lxml')

# find all product divs for that page 
product_divs = soup.find_all("div", {"class": "product-tracking"})

# initialize data frame
df = pd.DataFrame(columns = ['category', 'product_name', 'price', 'per_unit_price'])

# iterate through each prod div and collect name, price and per_unit_price
for div in product_divs:
    prod_details = div.find_all("div", {"class": "product-tile__details"})
    
    name = prod_details[0].find_all("h3", {"class": "text text--small4 text--left text--default-color product-tile__details__info__name"})[0].text
    
    prod_details = prod_details[0].find_all("div", {"class": "product-tile__details__info__section"})
    prod_info = prod_details[0].find_all("div", {"class": "product-prices product-prices--product-tile"})
    
    price = prod_info[0].find_all("span", {"class": "price selling-price-list__item__price selling-price-list__item__price--now-price"})[0].text
    
    try: # some items don't have a per unit price
        per_unit_price = prod_info[0].find_all("span", {"class": "price comparison-price-list__item__price"})[0].text
    except:
        per_unit_price = None 
    
    # append data to df 
    df = df.append({'category': category_name, 
                    'product_name': name, 
                    'price': price,
                    'per_unit_price': per_unit_price}
                   , ignore_index=True)


######################################### WRITE DATA #########################################
df.to_csv(rf'./grocery-store-data-scrapers/csv_files/{category_name}.csv', index=False)

print(f'completed in {(time.time() - start_time)}')