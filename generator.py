#!/usr/bin/env python
_version_ = "0.1"

import datetime, collections

history_dict = {datetime.date(2016, 01, 20): [394], datetime.date(2016, 01, 21): [395]}

print datetime.datetime.today()
print datetime.datetime.today().isoweekday()

# for x in history_dict:
# print x, ':', history_dict[x]

def generatePlan(start, end):
    new_lesson = 396
    learn_dict = history_dict
    review_dict = {}
    intervals = [1, 3, 6]

    for x in range(start, end):
        date = datetime.date(2016, 01, 20) + datetime.timedelta(days=x)
        # print "x is" , learn_dict.keys()[0], ",history date is ", date
        # add new lesson if needed
        if not learn_dict.has_key(date) and not isHoliday(date):
            # print "history[", review_date, "]: ", new_lesson
            learn_dict[date] = list()
            learn_dict[date].append(new_lesson)
            # review_dict[review_date].append(new_lesson)
            new_lesson += 1

        if not learn_dict.has_key(date):
            continue

        # add review dates
        for y in intervals:
            review_date = date + datetime.timedelta(days=y)
            # print "review_date: " , review_date, " history_date", date
            if not review_dict.has_key(review_date):
                review_dict[review_date] = list()
                # if not learn_dict.has_key(review_date) and not isHoliday(review_date):
                #     # print "history[", review_date, "]: ", new_lesson
                #     learn_dict[review_date] = {new_lesson}
                #     # review_dict[review_date].append(new_lesson)
                #     new_lesson += 1

            review_dict[review_date].extend(learn_dict[date])
            # print review_date, "review", review_dict[review_date]

    # sort dict by key
    learn_dict = collections.OrderedDict(sorted(learn_dict.items()))
    review_dict = collections.OrderedDict(sorted(review_dict.items()))

    for x in learn_dict:
        s = str(x) , " learn" , learn_dict[x]
        if review_dict.has_key(x):
            s += "review", review_dict[x]
        print s
        # print , "review", review_dict[x]


def isHoliday(date):
    print date, date.isoweekday()
    return date.isoweekday() == 6 or date.isoweekday() == 7


generatePlan(0, 10)