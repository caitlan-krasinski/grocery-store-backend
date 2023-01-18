print('##################### PROCESS STARTED #####################')

# 1. scrapers 
import loblaw_co_scraper
import flipp_scraper_v2 # upgrade to v2 

# 2. cleaning
import flipp_data_cleaning 
import loblaw_data_cleaning

# 3. generate
import generate_synthetic_data

# 4. index 
# revamp indexing with new data 
import build_index

print('##################### PROCESS COMPLETE #####################')
print('###################### DATA COLLECTED ######################')
