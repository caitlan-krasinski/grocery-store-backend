import requests

link = 'https://flipp.com'
backend_link = 'https://backflipp.wishabi.com/flipp'
search_link = f'{backend_link}/items/search'
item_link = f'{backend_link}/items/' 

def scrape_item(item_id):
    return requests.get(f"{item_link}/{item_id}").json()