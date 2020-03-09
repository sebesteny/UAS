from vincenty import vincenty


def GPS_to_distance_kilometres(gps_1, gps_2):
    # Distance between gps_1 and gps_2 in metres:
    d = vincenty(gps_1, gps_2)
    return d


# Defining the constants:
speed = 30  # m/s
speed_knots = speed * 1.9438  # knots
speed_cargo = 20  # m/s
take_off_time = 20  # s
landing_time = 20  # s
loading_time = 30  # s
battery_change_time = 30  # s
cargo_mass = 2  # kg
area_search_time = 30  # (seconds)
assumed_area_search_points = 40
assumed_ground_marker_points = 40
speed_trial_distance = 3  # km
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
ground_marker_points = []
deductions = []
total_points = []
T_2 = []
T_3 = []
T_4 = []

# Calculating the points gained by each strategy:
i = 0
for strategy in strategy_list:
    # Cargo points:
    cargo_points_gained = (strategy_list[i][0] * route_A_length + strategy_list[i][1] * route_B_length +
                           strategy_list[i][
                               2] * route_C_length) * cargo_mass * 8
    if cargo_points_gained > 160:
        cargo_points_gained = 160
    cargo_points.append(cargo_points_gained)
    # Speed trial points:
    speed_points_gained = (strategy_list[i][3]) * (speed_knots - 20)
    if speed_points_gained < 0:
        speed_points_gained = 0
    elif speed_points_gained > 40:
        speed_points_gained = 40
    speed_trial_points.append(speed_points_gained)
    # Ground marker ID points:
    ground_marker_points_gained = (strategy_list[i][3]) * assumed_ground_marker_points
    ground_marker_points.append(ground_marker_points_gained)
    # Area search points:
    area_points_gained = (strategy_list[i][4]) * assumed_area_search_points
    area_search_points.append(area_points_gained)

    # Calculating the time taken for each strategy:
    # Time spent to fly to drop zone (DZ):
    time_to_DZ = (strategy_list[i][0] * route_A_length + strategy_list[i][1] * route_B_length + strategy_list[i][
        2] * route_C_length) * 1000 / speed_cargo  # s
    # Time spent from DZ to take-off and landing point (TOLP)
    time_to_TOLP = (strategy_list[i][0] * distance_3_base + strategy_list[i][1] * distance_5_base + strategy_list[i][
        2] * distance_1_base) * 1000 / speed  # s
    # T_2:
    time_to_load = (strategy_list[i][0] + strategy_list[i][1] + strategy_list[i][2] - 1) * (loading_time +
                                                                                            battery_change_time)
    if time_to_load < 0:
        time_to_load = 0
    time_2 = (strategy_list[i][0] + strategy_list[i][1] + strategy_list[i][2]) * (take_off_time + landing_time) + \
             time_to_load + time_to_DZ + time_to_TOLP
    T_2.append(time_2)
    # T_3:
    time_3 = strategy_list[i][3] * (battery_change_time + take_off_time + landing_time + speed_trial_length / speed) \
             + strategy_list[i][4] * area_search_time
    T_3.append(time_3)
    # T_4:
    time_4 = time_2 + time_3
    T_4.append(time_4)

    # Calculating the deductions due to exceeding time for each strategy:
    # Deductions due to T_2:
    deduction_2 = (time_2 - 600) * 2
    if deduction_2 < 0:
        deduction_2 = 0
    deduction_4 = (time_4 - 900) * 2
    if deduction_4 < 0:
        deduction_4 = 0
    total_deductions = deduction_2 + deduction_4
    deductions.append(total_deductions)
    # Total points:
    total_points_gained = cargo_points_gained + speed_points_gained + area_points_gained + ground_marker_points_gained \
                          - total_deductions
    total_points.append(total_points_gained)
    i += 1
# Finding the best strategy:
max_value = max(total_points)
max_index = total_points.index(max_value)
best_strategy = strategy_list[max_index]

# test:
print(route_A_length)
print(route_B_length)
print(route_C_length)
print(cargo_points)
print(speed_trial_points)
print(area_search_points)
print(T_2)
print(T_3)
print(T_4)
print(deductions)
print(strategy_list)
print(total_points)
print(max_index)
print(max_value)
print(best_strategy)
print(deductions[max_index])
print(distance_1_base)