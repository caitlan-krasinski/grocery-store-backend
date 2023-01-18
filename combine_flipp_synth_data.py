import pandas as pd

stores = ['walmart', 'freshco', 'sobeys', 'food_basics']

for store in stores:
    flipp = pd.read_csv(f'clean_data/{store}/flyer_deals.csv')
    synth = pd.read_csv(f'clean_data/{store}/synthetic_data.csv')

    all_data = flipp.append(synth)

    all_data.to_csv(f'clean_data/{store}/{store}_data.csv', index=False)