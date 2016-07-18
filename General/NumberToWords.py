#!/bin/python

numdict = {"zero": "Zero", 0: "", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
           8: "Eight", 9: "Nine",
           10: "Ten",
           11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen", 15: "Fifteen", 16: "Sixteen", 17: "Seventeen",
           18: "Eighteen", 19: "Nineteen", 20: "Twenty", 30: "Thirty", 40: "Forty", 50: "Fifty", 60: "Sixty",
           70: "Seventy", 80: "Eighty", 90: "Ninety", 100: "Hundred", 10 ** 3: "Thousand", 10 ** 6: "Million",
           10 ** 9: "Billion", 10 ** 12: "Trillion"}


def show_3_digits(number):
    text = ""
    if number >= 100:
        hundred = number / 100
        text = numdict[hundred] + " " + numdict[100]
    else:
        hundred = 0
    ten = (number - hundred * 100) / 10
    if ten >= 2:
        text += " " + numdict[ten * 10] + " " + numdict[number - hundred * 100 - ten * 10]
    elif ten >= 0:
        text += " " + numdict[number - hundred * 100]
    return " " + text


def get_words_from_number(number):
    if number == 10 ** 12:
        return numdict[1] + " " + numdict[10 ** 12]
    sn = str(number)
    x = ""
    if len(sn) > 9:
        sn1 = sn[:len(sn) - 9]
        sn = sn[len(sn) - 9:]
        billion = show_3_digits(int(sn1))
        if billion.strip():
            x += billion + " " + numdict[10 ** 9]
    if len(sn) > 6:
        sn1 = sn[:len(sn) - 6]
        sn = sn[len(sn) - 6:]
        million = show_3_digits(int(sn1))
        if million.strip():
            x += million + " " + numdict[10 ** 6]
    if len(sn) > 3:
        sn1 = sn[:len(sn) - 3]
        sn = sn[len(sn) - 3:]
        thousand = show_3_digits(int(sn1))
        if thousand.strip():
            x += thousand + " " + numdict[10 ** 3]
    x += show_3_digits(int(sn))
    if not x:
        x = numdict["zero"]
    return x.strip().replace("  ", " ")


def test():
    print get_words_from_number(123456789123)


if __name__ == "__main__":
    test()
