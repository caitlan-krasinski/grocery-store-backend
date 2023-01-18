'''
reference: https://gist.github.com/jQwotos/37c54992881824d7084680ee91c9633c 
'''

import requests

link = 'https://flipp.com'
backend_link = 'https://backflipp.wishabi.com/flipp'
search_link = f'{backend_link}/items/search'
item_link = f'{backend_link}/items/' 

def scrape_item(item_id):
    return requests.get(f"{item_link}/{item_id}").json()