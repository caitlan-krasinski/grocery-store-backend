''' 
Selenium functions in order to control webpage and reveal 
product details hidden behind load-more buttons.
Keeps webdriver logic out of sight in the run_scraper file 
for simplicity and readability
'''

from selenium import webdriver
import time


def set_options():
    '''Sets the options field for the driver'''

    return webdriver.ChromeOptions()

def initiate_driver(driver_path, options):
    '''start chrome driver'''

    return webdriver.Chrome(driver_path, options=options)

def nav_to_page(driver, link):
    '''open page'''

    driver.get(link)

def close_cookies_blocker(driver, cookie_close_xref):
    '''cookie blocker pops up when you first go to a page, 
    this function clicks the close button on the popup'''

    cookies_block = driver.find_element_by_xpath(xpath='//*[@id="privacy-policy"]/div/div/button').click()
    print('\t closed cookie blocker')  

def scroll_to_bottom(driver, load_more_xpath):
    '''click load more results button until at bottom 
    based on the xpath of the button'''

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
            print(f'\t {count} page(s) loaded')

        except:
            break

def check_that_bottom_is_reached(driver, load_more_xpath):
    '''in case the scroll_to_bottom function moves on before the button
    element can load, this function checks if the button comes up
    and we stopped scrolling prematurely'''

    try: 
        load_more = driver.find_element_by_xpath(load_more_xpath)
        print('\t failed run')
    except:
        print('\t reached bottom of page')

def grab_html(driver):
    # extract page source
    page_source = driver.page_source
    return page_source
