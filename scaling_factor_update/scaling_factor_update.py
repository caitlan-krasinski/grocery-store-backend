import pandas as pd
from pickle import load, dump
import ast, sys

# gather args
store = sys.argv[1]
category = sys.argv[2]
change = int(ast.literal_eval(sys.argv[3]))

file = open('scaling_factor_update/updated_factors.pkl', 'rb')
updated_factors = load(file)
file.close()

# settings -> can adjust as needed 
STEP_SIZE = 0.05 # -> 5% 

# add to scaling factor 
if store in updated_factors.keys():
    store_dict = updated_factors[store]
    if category in store_dict.keys():
        #update 
        updated_factors[store][category] += change*STEP_SIZE
    else:
        updated_factors[store][category] = change*STEP_SIZE
else:
    updated_factors[store] = {category: change*STEP_SIZE}

# save 
dump(updated_factors, open('scaling_factor_update/updated_factors.pkl', 'wb'))