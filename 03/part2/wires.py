import math

def calculate_position(start_pos, offset):
    direction = offset[0]
    distance = int(offset[1:])

    if direction is 'U':
        end_pos = start_pos[0], start_pos[1] - distance
    elif direction is 'D':
        end_pos = start_pos[0], start_pos[1] + distance
    elif direction is 'R':
        end_pos = start_pos[0] + distance, start_pos[1]
    elif direction is 'L':
        end_pos = start_pos[0] - distance, start_pos[1]
    else:
        print('Error: Invalid direction')
        end_pos = None

    return end_pos

def find_intersections(paths):
    intersections = []

    # Start at origin
    start_pos_1 = (0, 0)
    distance_path_1 = 0
    for path_1 in paths[0]:
        # Calculate ending position for step
        end_pos_1 = calculate_position(start_pos_1, path_1)
        direction_1 = path_1[0]

        # Start at origin
        start_pos_2 = (0, 0)
        distance_path_2 = 0
        for path_2 in paths[1]:
            # Calculate ending position for step
            end_pos_2 = calculate_position(start_pos_2, path_2)
            direction_2 = path_2[0]

            # Check if lines intersect
            if (direction_1 is 'L' or direction_1 is 'R') and (direction_2 is 'U' or direction_2 is 'D'):
                # path_1 horizontal, path_2 vertical
                if direction_1 is 'L':
                    left = end_pos_1
                    right = start_pos_1
                else:
                    left = start_pos_1
                    right = end_pos_1

                if direction_2 is 'U':
                    top = end_pos_2
                    bottom = start_pos_2
                else:
                    top = start_pos_2
                    bottom = end_pos_2

                # if (left[0] <= top[0] <= right[0]) and (top[1] <= left[1] <= bottom[1]):
                #     intersect_pos = top[0], left[1]
                #     intersections.append(intersect_pos)

            if (direction_1 is 'U' or direction_1 is 'D') and (direction_2 is 'L' or direction_2 is 'R'):
                # path_1 vertical, path_2 horizontal
                if direction_1 is 'U':
                    top = end_pos_1
                    bottom = start_pos_1
                else:
                    top = start_pos_1
                    bottom = end_pos_1

                if direction_2 is 'L':
                    left = end_pos_2
                    right = start_pos_2
                else:
                    left = start_pos_2
                    right = end_pos_2

                if left is not None:
                    if (left[0] <= top[0] <= right[0]) and (top[1] <= left[1] <= bottom[1]):
                        intersect_pos = top[0], left[1]

                        partial_distance_1 = math.sqrt(pow(start_pos_1[0] - intersect_pos[0], 2) + pow(start_pos_1[1] - intersect_pos[1], 2))
                        partial_distance_2 = math.sqrt(pow(start_pos_2[0] - intersect_pos[0], 2) + pow(start_pos_2[1] - intersect_pos[1], 2))

                        total_distance_1 = distance_path_1 + partial_distance_1
                        total_distance_2 = distance_path_2 + partial_distance_2
                        total_distance = total_distance_1 + total_distance_2

                        intersections.append((intersect_pos, total_distance))
            # Move position to endpoint
            start_pos_2 = end_pos_2
            distance_path_2 += int(path_2[1:])

        # Move position to endpoint
        start_pos_1 = end_pos_1
        distance_path_1 += int(path_1[1:])

    return intersections

if __name__ == '__main__':
    file_name = './input.txt'

    # Read paths
    paths = []
    with open(file_name) as file:
        for line in file.readlines():
            path = line.strip('\n').split(',')
            paths.append(path)

    print('Finding intersections')
    intersections = find_intersections(paths)

    print('Finding closest intersection')
    smallest_distance = -1
    closest_intersection = None
    for intersect in intersections:
        distance = intersect[1]

        if smallest_distance < 0 or distance < smallest_distance:
            smallest_distance = distance
            closest_intersection = intersect

    print(smallest_distance)
    print(closest_intersection)
