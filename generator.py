#!/usr/bin/env python
__version__ = "0.1"

from datetime import date, timedelta, datetime
import collections
import sys

# history_dict = {date(2016, 01, 20): [394], date(2016, 01, 21): [395]}
# date_format = "%B %d, %Y"
date_format = "%Y-%m-%d"
learn_start_date = date(2100, 01, 20)
learn_end_date = date(2000, 01, 20)
pre_lesson = 000
history_recode_file = "history.txt"
lesson_seperator = ','

def main():
    # read command line arguments
    for arg in sys.argv[1:]:
        # print arg
        if ('a' == arg):
            _addHistoryRecords()
        elif ('g' == arg):
            _generatePlan()

def _generatePlan():
    start_date = raw_input('Start date: ')
    start_date = parseDate(start_date)

    end_date = raw_input('End date: ')
    end_date = parseDate(end_date)

    generatePlan(start_date, end_date)

def generatePlan(start_date, end_date):
    history_dict = parseHistoryToDict()
    scanHistoryDict(history_dict)

    learn_dict = history_dict
    review_dict = {}
    intervals = [1, 2, 4, 7, 15]
    global pre_lesson

    for date in daterange(learn_start_date, end_date):
        # add new lesson if needed, don't change past days
        if date > learn_end_date and not isHoliday(date):
            # print "history[", review_date, "]: ", new_lesson
            learn_dict[date] = list()
            learn_dict[date].append(pre_lesson + 1)
            pre_lesson += 1

        if not learn_dict.has_key(date):
            continue

        # add review dates
        for y in intervals:
            review_date = date + timedelta(days=y)
            if not review_dict.has_key(review_date):
                review_dict[review_date] = list()
            review_dict[review_date].extend(learn_dict[date])

    # sort dict by key
    learn_dict = collections.OrderedDict(sorted(learn_dict.items()))
    review_dict = collections.OrderedDict(sorted(review_dict.items()))

    writePlan(start_date, end_date, learn_dict, review_dict)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def isHoliday(date):
    return date.isoweekday() == 6 or date.isoweekday() == 7


def parseHistoryToDict():
    history_dict = {}

    with open(history_recode_file) as f:
        for line in f:
            date = line.split(':')[0]
            date = parseDate(date)
            lessonList = line.split(':')[1]
            lessonList = [int(k) for k in lessonList.split(',')]
            history_dict[date] = lessonList

    history_dict = collections.OrderedDict(sorted(history_dict.items()))
    return history_dict


def _addHistoryRecords():
    file = open(history_recode_file, "a")

    while True:
        date = raw_input('Date: ')
        if not date:
            break
        date = parseDate(date)
        lessonList = raw_input('Lesson(s): ')
        lessonList = [int(k) for k in lessonList.split(',')]
        # lessonList = list(eval(lessonList))
        addHistoryRecord(date, lessonList, file)

    file.close()

def addHistoryRecord(date, lessonList, file):
    file.write(date.strftime(date_format))
    file.write(':')
    file.write(','.join(str(x) for x in lessonList))
    file.write('\n')


def scanHistoryDict(history_dict):
    global pre_lesson, learn_start_date, learn_end_date

    for x in history_dict:
        if x < learn_start_date:
            learn_start_date = x

        if x > learn_end_date:
            learn_end_date = x

        if pre_lesson < max(history_dict[x]):
            pre_lesson = max(history_dict[x])

    print "------------- Ebbinghaus Plan -------------"


def writePlan(start_date, end_date, learn_dict, review_dict):
    for date in daterange(start_date, end_date):
        s = []
        s.append(date.strftime(date_format))
        s.append(' ')

        if learn_dict.has_key(date):
            s.append("learn ")
            s.append(', '.join(str(x) for x in learn_dict[date]))
        else:
            s.append("learn ***")

        if review_dict.has_key(date):
            s.append(", review ")
            s.append(', '.join(str(x) for x in review_dict[date]))
        else:
            s.append(", review ***")
        # if learn_dict.has_key(date):
        # s = str(x), " learn", learn_dict[date]
        #
        # if review_dict.has_key(x):
        #     s += "review", review_dict[x]
        s = ''.join(s)
        print s
        # print , "review", review_dict[x]

def parseDate(_date):
    if 'today' in _date.lower():
        ret = date.today()

        if len(_date.split('-')) > 1:
            ret -= timedelta(int(_date.split('-')[1]))
        elif len(_date.split('+')) > 1:
            ret += timedelta(int(_date.split('+')[1]))

        return ret
    else:
        return datetime.strptime(_date, date_format).date()

# addHistoryRecord(date.today(), [123, 124])
# generatePlan(date(2016, 01, 20), date(2016, 02, 10))
# _addHistoryRecords()
# print parseHistoryToDict()

# must locate at the end???
if __name__ == "__main__":
    main()