# Upgraded functions v1 with the following:
# Code now contains points_gained_so_far and time_spent_so_far variables
# so the it can be used to find best strategy after each package delivery
# Routes are defined as lists containing the way points
# The travel to the drop zone was included in the route_length calculations
# Created a function for calculating the length of a route
# time_to_TOLP calc replaced with a more universal formula using the lists of the routes

from vincenty import vincenty


def GPS_to_distance_kilometres(gps_1, gps_2):
    # Distance between gps_1 and gps_2 in metres:
    d = vincenty(gps_1, gps_2)
    return d


# A function that calculates the length of a route:
def calculate_route_length(route):
    route_length = 0
    for number in range(len(route) - 1):
        distance = GPS_to_distance_kilometres(route[number], route[number + 1])
        route_length += distance
    return route_length


def initialize_strategy_list():
    strategy_list = []
    # Initializing the list of strategies as an empty nested list:
    for route_A_num in range(4):
        for route_B_num in range(4):
            for route_C_num in range(4):
                for speed_trial_num in range(2):
                    for area_search_num in range(2):
                        new_strategy = [route_A_num, route_B_num, route_C_num, speed_trial_num, area_search_num]
                        strategy_list.append(new_strategy)
    return strategy_list


# Defining the constants:
points_gained_so_far = 120
time_spent_so_far = 400  # s
speed = 30  # m/s
speed_knots = speed * 1.9438  # knots
speed_cargo = 20  # m/s
take_off_time = 20  # s
landing_time = 20  # s
loading_time = 30  # s
battery_change_time = 30  # s
cargo_mass = 2  # kg
area_search_time = 60  # (seconds)
assumed_area_search_points = 40
assumed_ground_marker_points = 40
base = (51.530134, -0.153656)  # coordinates
WP_1 = (51.525255, -0.149633)
WP_2 = (51.527844, -0.147925)
WP_3 = (51.531695, -0.148565)
WP_4 = (51.534749, -0.150967)
WP_5 = (51.534517, -0.157477)
WP_6 = (51.532327, -0.160145)
DZ = (51.532327, -0.148565)

# Defining the routes as a list of variables that contain longitudinal and lateral coordinates:
route_A = [base, WP_1, WP_2, WP_3, DZ]
route_B = [base, WP_1, WP_2, WP_3, WP_4, WP_5, DZ]
route_C = [base, WP_1, WP_2, WP_3, WP_4, WP_5, WP_6, WP_1, DZ]
route_speed_trial = [base, WP_1, WP_2, WP_3]

# Calculating the route lengths:
route_A_length = calculate_route_length(route_A)
route_B_length = calculate_route_length(route_B)
route_C_length = calculate_route_length(route_C)
speed_trial_length = calculate_route_length(route_speed_trial)

# Initializing lists that will contain the points gained by each strategy for the different stages:
total_points = []
strategy_list = initialize_strategy_list()

# Calculating the points gained by each strategy:
i = 0
for strategy in strategy_list:
    # Cargo points:
    cargo_points_gained = (strategy_list[i][0] * route_A_length + strategy_list[i][1] * route_B_length +
                           strategy_list[i][
                               2] * route_C_length) * cargo_mass * 8 + points_gained_so_far
    if cargo_points_gained > 160:
        cargo_points_gained = 160
    # Speed trial points:
    speed_points_gained = (strategy_list[i][3]) * (speed_knots - 20)
    if speed_points_gained < 0:
        speed_points_gained = 0
    elif speed_points_gained > 40:
        speed_points_gained = 40
    # Ground marker ID points:
    ground_marker_points_gained = (strategy_list[i][3]) * assumed_ground_marker_points
    # Area search points:
    area_points_gained = (strategy_list[i][4]) * assumed_area_search_points

    # Calculating the time taken for each strategy:
    # Time spent to fly to drop zone (DZ):
    time_to_DZ = (strategy_list[i][0] * route_A_length + strategy_list[i][1] * route_B_length + strategy_list[i][
        2] * route_C_length) * 1000 / speed_cargo  # s
    # Time spent from DZ to take-off and landing point (TOLP)
    time_to_TOLP = (strategy_list[i][0] * GPS_to_distance_kilometres(route_A[-1], base) + strategy_list[i][1] *
                    GPS_to_distance_kilometres(route_B[-1], base) + strategy_list[i][2] *
                    GPS_to_distance_kilometres(route_C[-1], base)) * 1000 / speed  # s
    # T_2:
    time_to_load = (strategy_list[i][0] + strategy_list[i][1] + strategy_list[i][2] - 1) * (loading_time +
                                                                                            battery_change_time)
    if time_to_load < 0:
        time_to_load = 0
    time_2 = (strategy_list[i][0] + strategy_list[i][1] + strategy_list[i][2]) * (take_off_time + landing_time) + \
             time_to_load + time_to_DZ + time_to_TOLP + time_spent_so_far
    # T_3:
    time_3 = strategy_list[i][3] * (battery_change_time + take_off_time + landing_time + speed_trial_length * 1000 /
                                    speed) + strategy_list[i][4] * area_search_time
    # T_4:
    time_4 = time_2 + time_3

    # Calculating the deductions due to exceeding time for each strategy:
    # Deductions due to T_2:
    deduction_2 = (time_2 - 600) * 2
    if deduction_2 < 0:
        deduction_2 = 0
    deduction_4 = (time_4 - 900) * 2
    if deduction_4 < 0:
        deduction_4 = 0
    total_deductions = deduction_2 + deduction_4
    # Total points:
    total_points_gained = cargo_points_gained + speed_points_gained + area_points_gained + ground_marker_points_gained \
                          - total_deductions
    total_points.append(total_points_gained)
    i += 1
# Finding the best strategy:
max_value = max(total_points)
max_index = total_points.index(max_value)
best_strategy = strategy_list[max_index]

# Saving the best strategy in a txt file:
# Start with the longer routes because those have the best point/unit time ratio
frame = 0
nav_command = 16
file = open("mission.txt", "w")
file.write('QGC WPL 110\n')
if best_strategy[2] != 0:
    i = 0
    for element in route_C:
        x = element[0]
        y = element[1]
        z = 30  # later change to element[2]
        file.write(str(i) + '\t' + '0\t' + str(frame) + '\t' + str(nav_command) + '\t' + '0\t0\t0\t0\t' + str(x) +
                   '\t' + str(y) + '\t' + str(z) + '\t' + '0\n')
        i += 1
    # Adding the last WP again as a dummy WP:
    file.write(str(i) + '\t' + '0\t' + str(frame) + '\t' + str(nav_command) + '\t' + '0\t0\t0\t0\t' + str(x) +
               '\t' + str(y) + '\t' + str(z) + '\t' + '0\n')
elif best_strategy[1] != 0:
    i = 0
    for element in route_B:
        x = element[0]
        y = element[1]
        z = 30  # later change to element[2]
        file.write(str(i) + '\t' + '0\t' + str(frame) + '\t' + str(nav_command) + '\t' + '0\t0\t0\t0\t' + str(x) +
                   '\t' + str(y) + '\t' + str(z) + '\t' + '0\n')
        i += 1
    # Adding the last WP again as a dummy WP:
    file.write(str(i) + '\t' + '0\t' + str(frame) + '\t' + str(nav_command) + '\t' + '0\t0\t0\t0\t' + str(x) +
               '\t' + str(y) + '\t' + str(z) + '\t' + '0\n')
elif best_strategy[0] != 0:
    i = 0
    for element in route_A:
        x = element[0]
        y = element[1]
        z = 30  # later change to element[2]
        file.write(str(i) + '\t' + '0\t' + str(frame) + '\t' + str(nav_command) + '\t' + '0\t0\t0\t0\t' + str(x) +
                   '\t' + str(y) + '\t' + str(z) + '\t' + '0\n')
        i += 1
    # Adding the last WP again as a dummy WP:
    file.write(str(i) + '\t' + '0\t' + str(frame) + '\t' + str(nav_command) + '\t' + '0\t0\t0\t0\t' + str(x) +
               '\t' + str(y) + '\t' + str(z) + '\t' + '0\n')
elif best_strategy[3] != 0:
    i = 0
    for element in route_speed_trial:
        x = element[0]
        y = element[1]
        z = 30  # later change to element[2]
        file.write(str(i) + '\t' + '0\t' + str(frame) + '\t' + str(nav_command) + '\t' + '0\t0\t0\t0\t' + str(x) +
                   '\t' + str(y) + '\t' + str(z) + '\t' + '0\n')
        i += 1
    # Adding the last WP again as a dummy WP:
    file.write(str(i) + '\t' + '0\t' + str(frame) + '\t' + str(nav_command) + '\t' + '0\t0\t0\t0\t' + str(x) +
               '\t' + str(y) + '\t' + str(z) + '\t' + '0\n')
# elif best_strategy[4] != 0:
# FIGURE SOMETHING OUT FOR AREA SEARCH --> GRID?


# test:
print(route_A_length)
print(route_B_length)
print(route_C_length)
print(total_points)
print(max_value)
print(best_strategy)
print(GPS_to_distance_kilometres(route_C[-1], base))
print(speed_trial_length)
