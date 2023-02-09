'''Script to run 3 step data retrieval and cleaning process'''

import time 

print('##################### PROCESS STARTED #####################')

# 1. scrapers 
print('------------ scraping data')

start_time = time.time() 
print('starting loblaw co scraping')
import loblaw_co_scraper
print(f'completed in {time.time() - start_time} \n')

start_time = time.time() 
print('starting flipp scraping')
import flipp_scraper_v2 # upgrade to v2 
print(f'completed in {time.time() - start_time} \n')

# 2. cleaning
print('------------ cleaning data')

start_time = time.time() 
print('starting loblaw co cleaning')
import loblaw_data_cleaning
print(f'completed in {time.time() - start_time} \n')

start_time = time.time() 
print('starting flipp co cleaning')
import flipp_data_cleaning 
print(f'completed in {time.time() - start_time} \n')

# 3. generate
print('------------ generating synthetic data')

start_time = time.time() 
import generate_synthetic_data
import combine_flipp_synth_data
print(f'completed in {time.time() - start_time} \n')


## INDEXING DEPRECATED 
# # 4. index 
# print('------------ building indexes')

# start_time = time.time() 
# import build_index
# print(f'completed in {time.time() - start_time} \n')

print('##################### PROCESS COMPLETE #####################')
print('###################### DATA COLLECTED ######################')
