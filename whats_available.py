# Author:   Stephanie Blankley (sblankley)
#           stephanie.blankley@gmail.com
# 
# 
# Helper function to find what slots are available

def get_availabilities(driver):
    availabilities = {}
    elements = driver.find_elements_by_css_selector('tr')
    for element in elements:
        if "Sign Up" in element.text:
            text = element.text.split('\n')
            if ":" in text[0]:
                timeslot = text[0]
                availabilities[timeslot] = []
            else:
                lane = text[0]
                availabilities[timeslot].append(lane)
    return availabilities
