def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def number_of_days(month, year):
    if month in [0, 1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        if is_leap_year(year):
            return 29
        else:
            return 28


def days_diff(date1, date2):
    def days(date):
        y, m, d = date
        days = 365 * (y-1) + 30 * (m-1) + d
        days += ((m + (m+1) // 8) // 2) - 2 # months of 31 days
        days += y//4 - y//100 + y//400 # leap years
        if m < 3: days += 2 - (not y%4 and (y%100>0 or not y%400)) # January-February
        return days
    return abs(days(date1) - days(date2))