def count_passwords_in_range(start, stop):
    valid_passwords = []

    for i in range(start, stop+1):
        password = str(i)
        adjacent = False
        decreasing = False
        for digit in range(0, len(password)-1):
            if password[digit] == password[digit+1]:
                adjacent = True
            if password[digit] > password[digit+1]:
                decreasing = True

        if adjacent and not decreasing:
            valid_passwords.append(i)

    return len(valid_passwords)

if __name__ == '__main__':
    print('Finding passwords')
    print(count_passwords_in_range(197487, 673251))
