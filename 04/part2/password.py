def check_valid_password(password):
    decreasing = False
    two_adjacent = False

    last_digit = -1
    adjacent_digits = []

    for digit in password:
        digit = int(digit)

        # Check for decreasing digits
        if last_digit > digit:
            decreasing = True

        # Build adjacent_digits
        if digit == last_digit:
            # Add to current list of adjacent digits
            adjacent_digits[-1].append(digit)
        else:
            # Add another list of digits
            adjacent_digits.append([digit])

        # Set last_digit
        last_digit = digit

    for list in adjacent_digits:
        if len(list) == 2:
            two_adjacent = True

    if two_adjacent and not decreasing:
        return True
    else:
        return False

def count_passwords_in_range(start, stop):
    valid_passwords = []

    for i in range(start, stop+1):
        password = str(i)
        if check_valid_password(password):
            valid_passwords.append(password)


    return len(valid_passwords)

if __name__ == '__main__':
    print('Finding passwords')
    print(count_passwords_in_range(197487, 673251))
