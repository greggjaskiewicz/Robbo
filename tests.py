#!/usr/bin/python

MAX_NUMBER_LEVELS = 3

def getall_maps():
    global maps_list_raw
    maps_list_raw = []
    maps_list_cooked = []
    for f in range(1, MAX_NUMBER_LEVELS):
        with open('level_%s.txt' % f, 'r') as maps:  # < - appending line to a new list, containing each of the levels
            maps_list_raw.append(maps)
            for l in maps:
                maps_list_cooked.append(l)
    return maps_list_cooked

print getall_maps()


# a gdyby tak:

zbior_map = {1: [' mapa 1 '],
             2: [' mapa 2 '],
             3: [' mapa 3 ']}

# MAX_NUMBER_LEVELS = keys, assigned to maps

SCREWS = [[10, 50], [20, 80], [30, 90]]


screws_x = []
for s in SCREWS:
    print s[0], s[1]


