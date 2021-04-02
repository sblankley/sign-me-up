# Author:   Stephanie Blankley (sblankley)
#           stephanie.blankley@gmail.com
# 
# 
# Helper functions to sign up

def get_button_index(availabilities, desired_slot):
    
    '''
    Outputs index of button if desired_slot is available, else None
    '''

    button_index = 0
    for timeslot, lanes in availabilities.items():
        for lane in lanes:
            if timeslot==desired_slot[0] and lane==desired_slot[1]:
                return button_index
            else:
                button_index+=1
    return 'NotAvailable'


def select_slot(driver, availabilities, desired_slot):

    '''
    Checks the sign up box of the desired_slot

    input:      driver              the webdriver in which to execute
                availabilities      dictionary of time: [lanes] used to find button index
                desired_slot        tuples (time, lane) to check

    output:     success_str         status
    '''

    # grab all the buttons
    buttons = driver.find_elements_by_xpath("//input[@type='checkbox']")

    # make sure they align with the availabilities size
    num_buttons = len(buttons)
    num_avail = sum(len(slots) for slots in availabilities.values())
    if num_buttons == 0 or num_avail == 0:
        return 'NoButtonsToClick'
    elif num_buttons == num_avail:
        pass
    else:
        return 'AvailabilitySizeMismatch'

    # confirm desired slot available
    desired_button_index = get_button_index(availabilities, desired_slot)
    if desired_button_index == 'NotAvailable':
        return 'DesiredSlotNotAvailable'

    # scroll and check the box
    desired_button = buttons[desired_button_index]
    driver.execute_script("arguments[0].scrollIntoView();", desired_button)
    try:
        desired_button.click()
        return 'SlotSelected'
    except:
        return 'SlotNotSelected'


def sign_me_up(driver, availabilities, desired_slots, swimmer_info):

    '''
    Given availabilities, desired slots for the day, and who it's for, sign up!

    input:      driver              the webdriver in which to execute
                availabilities      dictionary of time: [lanes] used to find button index
                desired_slots       list of tuples (time, lane) to check
                swimmer_info        dictionary with first, last, and email of swimmer

    output:     success_str         status
    '''

    # select all desired slots
    unsuccessful_slots = 0
    for desired_slot in desired_slots:
        status = select_slot(driver, availabilities, desired_slot)
        if status is not 'SlotSelected':
            print(f"{status}: {desired_slot}") # don't return, try remaining slots
            unsuccessful_slots += 1
        else: # remove from availabilities
            availabilities[desired_slot[0]].remove(desired_slot[1])

    if unsuccessful_slots == len(desired_slots):
        return 'CannotSignUpForAnySlots', availabilities

    # move to next page
    try:
        driver.find_element_by_xpath("//input[@type='submit']").click()
    except:
        return 'UnableToGoToInfoPage', availabilities
    
    # fill out swimmer information
    try:
        driver.find_element_by_xpath("//input[@id='firstname']").send_keys(swimmer_info['first'])
        driver.find_element_by_xpath("//input[@id='lastname']").send_keys(swimmer_info['last'])
        driver.find_element_by_xpath("//input[@id='email']").send_keys(swimmer_info['email'])
    except:
        return 'SwimmerInfoNotInput', availabilities

    # submit
    try:
        driver.find_element_by_xpath("//button[@name='btnSignUp']").click()
        return 'Submitted', availabilities
    except:
        return 'UnableToSubmit', availabilities
