# Author:   Stephanie Blankley (sblankley)
#           stephanie.blankley@gmail.com
# 
#
# Script for signing up for the week

import os
import sys
import json
import re
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import Select, WebDriverWait

# helper functions
import whats_available
import choose_lanes
import sign_up

link = 'https://www.signupgenius.com/tabs/13577D800A4C9E95-lapswim'
base_link = 'https://www.signupgenius.com/go/'

with open('swimmers.json') as swimmer_file:
    swimmers_file = json.load(swimmer_file)

def daily_sign_up(driver, daily_link, swimmers):

    driver.get(daily_link)
    availabilities = whats_available.get_availabilities(driver)

    # what day is it
    header_text = driver.find_element_by_class_name('SUGHeaderText').text
    day = re.split(',|\.| ', header_text)[2]
    print(f"\n{day}")
    if day in ['Mon','Tues','Wed','Thurs','Fri']:
        keyword = 'weekdays'
    elif day in ['Sat','Sun']:
        keyword = 'weekends'
    else:
        keyword = ''

    for swimmer in swimmers:
        swimmer_info = swimmers_file[swimmer]
        if 'weekly-slots' not in swimmer_info:
            continue
        weekly_slots = swimmer_info['weekly-slots']
        if keyword in weekly_slots:
            desired_times = weekly_slots[keyword]
        elif day in weekly_slots:
            desired_times = weekly_slots[day]
        else:
            continue
        
        desired_slots = choose_lanes.choose_lanes(availabilities, desired_times)
    
        status, availabilities = sign_up.sign_me_up(driver, availabilities, desired_slots, swimmer_info)
        print(f"{status}: {swimmer}")

        driver.get(daily_link) # refresh page for next swimmer

def main(wait_flag, swimmers):

    driver = Firefox()
    driver.get(link)
    tabs = driver.find_elements_by_class_name('tabItem')
    num_tabs = len(tabs)
    old_num_tabs = num_tabs

    if wait_flag == 'wait':
        # refresh page until more tabs (days) available
        while True:
            driver.refresh()
            tabs = driver.find_elements_by_class_name('tabItem')
            num_tabs = len(tabs)
            if num_tabs > old_num_tabs:
                tabs = tabs[old_num_tabs:]
                break
    
    # grab each day's url
    daily_links = []
    for tab in tabs:
        onclick = tab.get_attribute('onclick')
        options = onclick.split('\'')
        extension = options[1]
        day_link = base_link + extension
        daily_links.append(day_link)

    daily_links.reverse() # saturday is last and fills up first

    for daily_link in daily_links:
        daily_sign_up(driver, daily_link, swimmers)


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print('Missing arguments')
        print('Usage: python3 weekly-sign-up.py <wait/now> Swimmer1 Swimmer2 <...>')
    else:
        wait_flag = str(sys.argv[1])
        swimmers = []
        for swimmer in sys.argv[2:]:
            if str(swimmer) in swimmers_file:
                swimmers.append(str(swimmer))
            else:
                print(f"{swimmer} not in swimmers.json")

        main(wait_flag, swimmers)
