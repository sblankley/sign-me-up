# Sign Me Up

Program and tools for automating sign ups for lap lane reservations.

## Motivation

With social distancing protocols and capacity limits in place, gone are the days when we could go to the pool and hop in as we pleased. Now, we must make lane reservations-- one person per lane in time-alotted slots.

The pool I frequent uses [SignUpGenius](https://signupgenius.com), and while it does the job, it is a bit painful to use. I could be harsher about the UX but it's a free service and honestly that's not my real motivation for this project.

My two main grievances:
1. Sign ups for the following week drop on Fridays at 3pm. Many people sit at their computer until that time comes and sign up instantly, leaving few slots left for those of us who aren't able to refresh a screen and sign up in the 3:00pm to 3:05pm window (yes, it is that tight and sometimes tighter).
2. People sign up willy-nilly even if they don't plan to attend all slots. There is no cancellation policy other than "Please cancel reservations if you can't attend" (direct quote). There is no hope for complete no-shows, but many people will cancel 1-12 hours before, and it's not practical to constantly check the site for cancellations.

My solutions:
1. Make a bot to sign me (and friends) up for the week at the Friday drop time. *first version*
2. Make a bot to check a desired full time slot, and if someone cancels their reservation, sign us up in that place. *in progress*

## Approach

There are three main aspects to both solutions:
1. Scrape the site for what's available.
-- This is straight-forward as it is a simple site.
2. Given what's available, pick a lane.
-- I have my own favorite lanes, but it gets more complicated when I want two 1-hour slots and my favorites aren't available for both. Gets even more complicated when I want adjacent lanes with my friends.
3. Given the available lane choice, sign up.
-- This is easy when there's not a lot of movement on the site but is more chaotic around schedule release time when 20+ people are signing up at once.

## Prerequisites

### WebDriver

These scripts use the `selenium` python package to access the site. It can be installed using `pip`.

```bash
pip3 install selenium
```

Download the [geckodriver](https://github.com/mozilla/geckodriver/releases) executable and place in the root of this repo. This is for Firefox but can just as easily use another browser that `selenium` supports.

Add the executable to system path by running the following in the root directory prior to running the script.

```bash
export PATH=$PATH:${PWD}
```

or add the directory's path to `~/.bashrc` to avoid adding it each time.

### Swimmer Info

To sign up for a slot, the site requires first name, last name, and email address. If the email address aligns with a Sign Up Genius account, the user can modify the reservation later. For weekly sign-ups, the swimmer's weekly schedule is also needed. This information must be stored in the `swimmers.json` file in the root directory in the following format:
```json
{
    "NAME1": {
        "first": "FIRSTNAME",
        "last": "LASTNAME",
        "email": "EMAIL",
        "weekly-slots": {
            "weekdays": [
                "7:00am - 7:55am  ",
                "8:00am - 8:55am  "
            ],
            "weekends": [
                "10:00am - 10:55am  ",
                "11:00am - 11:55am  "
            ]
        }
    },
    "NAME2": {
        "first": "FIRSTNAME",
        "last": "LASTNAME",
        "email": "EMAIL",
        "weekly-slots": {
            "Mon": [
                "8:00am - 8:55am  "
            ],
            "Thurs": [
                "8:00am - 8:55am  "
            ]
        }
    }
}
```

## Usage

### Weekly Sign Up

Required arguments:
* now / wait
-- now: runs the script with the site as is
-- wait: refreshes the site until more sign up days are available 
* names of swimmers
-- at least one name of who to sign up for the week

```bash
python3 weekly-sign-up.py now Steph
```
```bash
python3 weekly-sign-up.py wait Steph Cassie
```

### Credit

Feel free to use, add to, and improve these tools (but please include me so I can sign up better, too!)