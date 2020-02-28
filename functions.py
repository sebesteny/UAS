from vincenty import vincenty


def GPS_to_distance_kilometres(gps_1, gps_2):
    # Distance between gps_1 and gps_2 in metres:
    d = vincenty(gps_1, gps_2)
    return d


# Defining the constants:
speed = 20  # m/s
speed_knots = speed * 1.9438  # knots
speed_cargo = 15  # m/s
take_off_time = 20  # s
landing_time = 20  # s
loading = 30  # s
battery_change_time = 30  # s
cargo_mass = 2  # kg
area_search_time = 30  # (seconds)
assumed_area_search_points = 40
base = (51.530134, -0.153656)  # coordinates
WP_1 = (51.525255, -0.149633)
WP_2 = (51.527844, -0.147925)
WP_3 = (51.531695, -0.148565)
WP_4 = (51.534749, -0.150967)
WP_5 = (51.534517, -0.157477)
WP_6 = (51.532327, -0.160145)

# Calculating distances:
distance_12 = GPS_to_distance_kilometres(WP_1, WP_2)
distance_23 = GPS_to_distance_kilometres(WP_2, WP_3)
distance_34 = GPS_to_distance_kilometres(WP_3, WP_4)
distance_45 = GPS_to_distance_kilometres(WP_4, WP_5)
distance_56 = GPS_to_distance_kilometres(WP_5, WP_6)
distance_61 = GPS_to_distance_kilometres(WP_6, WP_1)
distance_1_base = GPS_to_distance_kilometres(WP_1, base)
distance_2_base = GPS_to_distance_kilometres(WP_2, base)
distance_3_base = GPS_to_distance_kilometres(WP_3, base)
distance_4_base = GPS_to_distance_kilometres(WP_4, base)
distance_5_base = GPS_to_distance_kilometres(WP_5, base)
distance_6_base = GPS_to_distance_kilometres(WP_6, base)

# Calculating the length of routes:
route_A_length = distance_1_base + distance_12 + distance_23
route_B_length = distance_1_base + distance_12 + distance_23 + distance_34 + distance_45
route_C_length = distance_1_base + distance_12 + distance_23 + distance_34 + distance_45 + distance_56 + distance_61
speed_trial_length = distance_12 + distance_23 + distance_34

# Initializing the number of times each stage is done:
route_A_num = route_B_num = route_C_num = speed_trial_num = area_search_num = 0
strategy_list = []

# Initializing the list of strategies as an empty nested list:
for route_A_num in range(4):
    for route_B_num in range(4):
        for route_C_num in range(4):
            for speed_trial_num in range(2):
                for area_search_num in range(2):
                    new_strategy = [route_A_num, route_B_num, route_C_num, speed_trial_num, area_search_num]
                    strategy_list.append(new_strategy)

# Initializing lists that will contain the points gained by each strategy for the different stages:
cargo_points = []
speed_trial_points = []
area_search_points = []
total_points_gained = []
deductions = []
total_points = []

# Calculating the points gained by each strategy:
# Cargo points:
i = 0
for strategy in strategy_list:
    points_gained = (strategy_list[i][0] * route_A_length + strategy_list[i][1] * route_B_length + strategy_list[i][
        2] * route_C_length) * cargo_mass * 8
    if points_gained > 160:
        points_gained = 160
    cargo_points.append(points_gained)
    i += 1
# Speed trial points:
i =0
for strategy in strategy_list:
    points_gained = (strategy_list[i][3]) * (speed_knots-20)
    if points_gained < 0:
        points_gained = 0
    elif points_gained > 40:
        points_gained = 40
    speed_trial_points.append(points_gained)
    i += 1
# Area search points:
i = 0
for strategy in strategy_list:
    points_gained = (strategy_list[i][4]) * assumed_area_search_points
    area_search_points.append(points_gained)
    i +=1
# Total points:

# Calculating the time taken for each strategy:

# Calculating the deductions due to exceeding time for each strategy:


# test:
print(route_A_length)
print(route_B_length)
print(route_C_length)
print(cargo_points)
print(speed_trial_points)
print(area_search_points)