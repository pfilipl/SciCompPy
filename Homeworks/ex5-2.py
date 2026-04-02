import datetime


def print_working_days(date1, date2):
    weekdays = []
    while date1 < date2:
        if date1.isoweekday() < 6:
            weekdays.append(date1)
        date1 += datetime.timedelta(1)

    results = f'There is {len(weekdays)} weekdays between entered dates:'
    for date in weekdays:
        results += f'\n{date}'

    print(results)


date1 = datetime.date.fromisoformat(input("Enter first date (ISO format): "))
date2 = datetime.date.fromisoformat(input("Enter second date (ISO format): "))

print_working_days(date1, date2)

"""
Example:

Enter first date (ISO format): 2026-04-02                                                                                                  
Enter second date (ISO format): 2026-04-08
There is 4 weekdays between entered dates, they are:
2026-04-02
2026-04-03
2026-04-06
2026-04-07
"""