# This file is responsible for scraping out the data from the pay scale website - web scraping
# the challenges I faced with the following code was recaptcha, after every first, second or Third and later to that 15th change of the url it asked for the recaptcha.
# the code will fail when the recaptcha appears. To solve it, I gave myself of 15-25 sec of window to solve it when timer appears. It is kind of a semi-bot to collect the information.
# there are some workaround to it - such as adding wait time, changing user-agent frequently.

import csv
import random

#result = [ {"column_name" : "value", "column_name" : "value", "column_name" : "value"}  ---> Row1 is a dict with key as column name and value as data
#           {"column_name" : "value", "column_name" : "value", "column_name" : "value"}] ---> Row2

result = []

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from constants import data_url

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

crawler = webdriver.Chrome()
crawler.get(url=data_url)

def pagination_process(column_name):

    # pause script so that page can be loaded and change
    time.sleep(random.choice(range(7, 12)))

    table_body_rows = crawler.find_elements(By.CLASS_NAME, value='data-table__row')

    time.sleep(2)
    for body_row in table_body_rows:
        row_value = [td.text for td in body_row.find_elements(By.TAG_NAME, value='td')] #----> signal row values

        result_row_dict = {column_name[i]:row_value[i] for i in range(len(row_value))}
        result.append(result_row_dict)

time.sleep(10) # in case of re-captcha

table = crawler.find_element(By.CLASS_NAME, 'data-table')
table_heads = table.find_elements(By.TAG_NAME, value='th')
heading = [row.text for row in table_heads] #---> list of heading

pagination_btns = crawler.find_elements(By.CLASS_NAME, value='pagination__btn--inner')
total_page = int(pagination_btns[-2].text)

for i in range(1, total_page+1):
    #collect the data
    pagination_process(heading)

    time.sleep(random.choice(range(7, 12)))

    #go to the next page/
    pagination_btns = crawler.find_elements(By.CLASS_NAME, value='pagination__btn')
    pagination_btns[-1].click()

    print(i ,len(result))

print(result)

with open('./data/highest_salary.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=heading)
    writer.writeheader()
    writer.writerows(result)
