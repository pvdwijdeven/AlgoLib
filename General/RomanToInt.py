table = [('M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100), ('XC', 90), ('L', 50), ('XL', 40), ('X', 10),
         ('IX', 9), ('V', 5), ('IV', 4), ('I', 1)]


def int_to_roman(integer):
    parts = []
    for letter, value in table:
        while value <= integer:
            integer -= value
            parts.append(letter)
    return ''.join(parts)


def rom_to_int(string):
    result = 0
    for letter, value in table:
        while string.startswith(letter):
            result += value
            string = string[len(letter):]
    return result


print rom_to_int("MCMLXXIII")
print int_to_roman(1973)