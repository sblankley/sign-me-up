# Author:   Stephanie Blankley (sblankley)
#           stephanie.blankley@gmail.com
# 
# 
# Helper functions to choose lane(s)

def ranked_lane(lane):
    # in order of preference
    #   lifeguard stand blocks view of clock from lanes 6-8
    #   lane 5 is the transition from shallow to deep
    #   deep side (lower numbers) is closer to the exit gate but further from clock
    #   shallow side (higher numbers) is closer to clock

    lane_heirarchy = [15, 14, 13, 12, 11, 16, 17, 10, 9, 3, 4, 2, 1, 5, 7, 6, 8]
    lane_int = int(lane.split()[1])
    score = lane_heirarchy.index(lane_int)
    return score

def choose_lanes(availabilities, desired_times):
    '''
    Given lane availabilities for one day, choose the lanes we want

    input:  availabilites       dictionary with timeslot string as keys and list of lane strings as values

    output: desired_slots        list of tuples in the form (timeslot, lane)
    '''
    desired_slots = []

    # See what lanes are available for multiple shifts
    lane_tracker = {}
    for slot, lanes in availabilities.items():
        for lane in lanes:
            if lane in lane_tracker:
                lane_tracker[lane].append(slot)
            else:
                lane_tracker[lane]=[slot]

    potential_lanes = []
    for lane, slots in lane_tracker.items():
        if all(times in slots for times in desired_times):
            potential_lanes.append(lane)
    if len(potential_lanes)==0:
        pass
    else:
        potential_lanes.sort(key=ranked_lane)
        for time in desired_times:
            desired_slots.append((time, potential_lanes[0]))

    return desired_slots