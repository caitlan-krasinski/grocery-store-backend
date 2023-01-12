# grocery-store-data-scrapers
Scrapers for FYDP grocery product and price data

## Setup
`pip install -r requirements.txt`

## Runs
**Script to scrape, preprocess and index data:**
`python get_data.py` - to be run weekly on Thursdays 
<br></br>
**Script for search:**
`python search.py <grocery_list>`

*grocery_list* argument must be passed as a string like so: `"['2% milk', 'Cheddar Cheese', 'white sliced bread']"`

## Some helpful resources:

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25

https://medium.com/codex/web-scraping-with-selenium-in-python-832cf4b827a4
