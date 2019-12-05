def follow_path(path):
    # Follow path
    coord = 0, 0
    coord_list = []

    for step in path:
        direction = step[0]
        distance = int(step[1:])

        dir_x, dir_y = 0, 0

        if direction is 'U':
            dir_y = -1
        elif direction is 'D':
            dir_y = 1
        elif direction is 'L':
            dir_x = -1
        elif direction is 'R':
            dir_x = 1
        else:
            print('Error: Invalid Direction "%s"' % direction)

        for i in range(distance):
            coord = coord[0] + dir_x, coord[1] + dir_y
            coord_list.append(coord)

    return coord_list

def find_intersections(path1, path2):
    intersections = []

    pos_1 = (0, 0)
    for p1 in path1:
        direction_1 = p1[0]
        distance_1 = int(p1[1:])

        # Calculate end point of path1
        if direction_1 is 'U':
            end_pos_1 = pos_1[0], pos_1[1] - distance_1
        elif direction_1 is 'D':
            end_pos_1 = pos_1[0], pos_1[1] + distance_1
        elif direction_1 is 'R':
            end_pos_1 = pos_1[0] + distance_1, pos_1[1]
        elif direction_1 is 'L':
            end_pos_1 = pos_1[0] - distance_1, pos_1[1]
        else:
            print('Error: Invalid direction_1')
            return None

        pos_2 = (0, 0)
        for p2 in path2:
            direction_2 = p2[0]
            distance_2 = int(p2[1:])

            # Calculate end point of path2
            if direction_2 is 'U':
                end_pos_2 = pos_2[0], pos_2[1] - distance_2
            elif direction_2 is 'D':
                end_pos_2 = pos_2[0], pos_2[1] + distance_2
            elif direction_2 is 'R':
                end_pos_2 = pos_2[0] + distance_2, pos_2[1]
            elif direction_2 is 'L':
                end_pos_2 = pos_2[0] - distance_2, pos_2[1]
            else:
                print('Error: Invalid direction_2')
                return None

            # Check if lines intersect
            if (direction_1 is 'U' or direction_1 is 'D') and (direction_2 is 'U' or direction_2 is 'D'):
                # Two vertical lines
                pass
            elif (direction_1 is 'L' or direction_1 is 'R') and (direction_2 is 'L' or direction_2 is 'R'):
                # Two horizontal lines
                pass
            else:
                if direction_1 is 'U':
                    pass
                elif direction_1 is 'D':
                    pass
                elif direction_1 is 'L':
                    pass
                elif direction_1 is 'R':
                    pass

            pos_2 = end_pos_2

        pos_1 = end_pos_1

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
    intersections = find_intersections(paths[0], paths[1])

    print('Finding closest intersection')
    smallest_distance = -1
    closest_intersection = None
    for int in intersections:
        distance = int[0] + int[1]

        if smallest_distance < 0 or distance < smallest_distance:
            closest_intersection = int
            smallest_distance = distance

    print(smallest_distance)
    print(closest_intersection)
