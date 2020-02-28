from vincenty import vincenty


def GPS_to_distance_metres(gps_1, gps_2):
    # Distance between gps_1 and gps_2 in metres:
    d = vincenty(gps_1, gps_2) * 1000
    return (d)


# route_A_length = distance_12 + distance_23 + distance_34
# route_B_length = distance_12 + distance_23 + distance_34
# route_C_length = distance_12 + distance_23 + distance_34
# speed_trial_length = distance_12 + distance_23 + distance_34
# area_search_time = 30  # (seconds)






# test:
WP_1 = (42.3541165, -71.0693514)
WP_2 = (40.7791472, -73.9680804)
distance_12 = GPS_to_distance_metres(WP_1, WP_2)
print(d)
