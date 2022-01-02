from selenium import webdriver
import requests,bs4,os
browser= webdriver.Chrome()
browser.get('https://en.wikipedia.org/wiki/Main_Page')
elem = browser.find_element_by_name('search')
elem.send_keys('Samsung')
elem = browser.find_element_by_id('searchButton')
elem.click()

i = 0
while True:
    i += 1
    j = 0    
    while True:
        j += 1
        elems = browser.find_elements_by_css_selector(".toclevel-"+str(i)+" tocsection-"+str(j)+" > a")
        for text in elems:
            if j == 1:            
                print(text)
            else:
                print('\t'+text)
        break;
    
        
    
    
