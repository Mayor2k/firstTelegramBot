import time
import calendar


def _fix_date(day, month, year):
    return_array = [day, month, year]
    return_array[1] += 1
    if return_array[1] > 12:
        return_array[1] = 1
        return_array[2] += 1
    return_array[0] = return_array[0] + 1 - calendar.monthrange(return_array[2], return_array[1])[1]
    if return_array[0] == 0:
        return_array[0] = 1
    return return_array


def _format_months_and_weekdays(weekday, month):
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat","Sun"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return weekdays[weekday], months[month-1]


def delivery_days_list(day, month, year):
    global weekday1
    return_array = [[0] * 4] * 5

    for i in range(5):
        day1 = day + 7 if i == 0 else return_array[i - 1][0] + 1
        month1 = month if i == 0 else return_array[i - 1][2]
        year1 = year if i == 0 else return_array[i - 1][3]
        try:
            weekday1 = calendar.weekday(year1, month1, day1)
        except ValueError:
            day1, month1, year1 = _fix_date(day1, month1, year1)[0], _fix_date(day1, month1, year1)[1], \
                                  _fix_date(day1, month1, year1)[2]
            weekday1 = calendar.weekday(year1, month1, day1)
        finally:
            if weekday1 == 5:
                if day1 > calendar.monthrange(2019, 5)[1]:
                    day1, month1, year1 = _fix_date(day1 + 2, month1, year1)[0], \
                                          _fix_date(day1 + 2, month1, year1)[1], \
                                          _fix_date(day1 + 2, month1, year1)[2]
                else:
                    day1 += 2
                weekday1 = 0
            elif weekday1 == 6:
                if day1 > calendar.monthrange(2019, 5)[1]:
                    day1, month1, year1 = _fix_date(day1 + 1, month1, year1)[0], \
                                          _fix_date(day1 + 1, month1, year1)[1], \
                                          _fix_date(day1 + 1, month1, year1)[2]
                else:
                    day1 += 1
                weekday1 = 0

        return_array[i] = [day1, weekday1, month1, year1]

    for x in range(5):
        weekday = _format_months_and_weekdays(return_array[x][1],return_array[x][2])[0]
        month = _format_months_and_weekdays(return_array[x][1],return_array[x][2])[1]
        return_array[x] = [str(return_array[x][0]), weekday,month, str(return_array[x][3])]
    return return_array


def get_current_date():
    date = time.strftime('%d,' + '%m,' + '%Y', time.gmtime())
    date = date.split(",")
    date = [int(date[x]) for x in range(3)]
    return date


def garbage(string):
    remove_symbols = "[('',)]"
    for char in remove_symbols:
        string = string.replace(char, "")
    return string
