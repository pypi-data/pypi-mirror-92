from datetime import datetime


def get_duration(start, end):
    print(start, type(start))
    start = datetime.strptime(str(start), '%Y-%m-%d %H:%M')
    end = datetime.strptime(str(end), '%Y-%m-%d %H:%M')
    day = (end - start).days
    minute = ((end - start).seconds // 60)
    return day*24*60+minute
