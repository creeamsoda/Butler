from enum import Enum

def CheckNumber(numberString):
	try:
		num = int(numberString)
	except ValueError:
		return CheckNumberResult.ContainsNotNum
	if num < 0:
		return CheckNumberResult.LengthOutOfRange
	return CheckNumberResult.Valid

class CheckNumberResult(Enum):
	Valid = 1
	ContainsNotNum = 2
	LengthOutOfRange = 3

def CheckTime(timeString):
	timeList = timeString.split(":")
	if len(timeList) != 2:
		return CheckTimeResult.ContainsNotNum
	checkHourResult = CheckHour(timeList[0])
	checkMinuteResult = CheckMinute(timeList[1])
	if checkHourResult == CheckTimeResult.Valid and checkMinuteResult == CheckTimeResult.Valid:
		return [CheckTimeResult.Valid]
	else:
		results = []
		if checkHourResult != CheckTimeResult.Valid:
			results.append(checkHourResult)
		if checkMinuteResult != CheckTimeResult.Valid:
			results.append(checkMinuteResult)
		return results


def CheckHour(hourString):
	try:
		hourInt = int(hourString)
	except ValueError:
		return CheckTimeResult.ContainsNotNum
	if hourInt < 0 or 23 < hourInt:
		return CheckTimeResult.HourOutOfRange
	return CheckTimeResult.Valid

def CheckMinute(minuteString):
	try:
		minuteInt = int(minuteString)
	except ValueError:
		return CheckTimeResult.ContainsNotNum
	if minuteInt < 0 or 59 < minuteInt:
		return CheckTimeResult.MinuteOutOfRange
	return CheckTimeResult.Valid


class CheckTimeResult(Enum):
	Valid = 1
	ContainsNotNum = 2
	HourOutOfRange = 3
	MinuteOutOfRange = 4

def CheckDate(dateString):
	dateList = dateString.split("-")
	if len(dateList) != 3:
		#ハイフンが含まれている？
		return [CheckDateResult.ContainsNotNum]

	checkYearResult = CheckYear(dateList[0])
	checkMonthResult = CheckMonth(dateList[1])
	checkDayResult = CheckDay(dateList[2])

	#フォーマットが適正なら、30日か31日か、閏年か平年かのチェックを行う
	if checkYearResult == CheckDateResult.Valid and \
			checkMonthResult == CheckDateResult.Valid and \
			checkDayResult == CheckDateResult.Valid:
		CheckCalenderResult = CheckCalender(dateList)
		return [CheckCalenderResult]
	else:
		results = []
		if checkYearResult != CheckDateResult.Valid:
			results.append(checkYearResult)
		if checkMonthResult != CheckDateResult.Valid:
			results.append(checkMonthResult)
		if checkDayResult != CheckDateResult.Valid:
			results.append(checkDayResult)
		return results

def CheckYear(yearString):
	try:
		yearInt = int(yearString)
	except ValueError:
		return CheckDateResult.ContainsNotNum

	if yearInt < 1900 or 2100 < yearInt:
		return CheckDateResult.YearOutOfRange

	return CheckDateResult.Valid


def CheckMonth(monthString):
	try:
		monthInt = int(monthString)
	except ValueError:
		return CheckDateResult.ContainsNotNum

	if monthInt < 1 or 12 < monthInt:
		return CheckDateResult.MonthOutOfRange

	return CheckDateResult.Valid


def CheckDay(dayString):
	try:
		dayInt = int(dayString)
	except ValueError:
		return CheckDateResult.ContainsNotNum

	if dayInt < 1 or 31 < dayInt:
		return CheckDateResult.DayOutOfRange

	return CheckDateResult.Valid

def CheckCalender(dateList):
	dateIntList = [int(x) for x in dateList]
	year, month, day = dateIntList
	isLeapYear = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

	if month == 2:
		if isLeapYear and day > 29:
			return CheckDateResult.DayOutOfRange
		elif not isLeapYear and day > 28:
			return CheckDateResult.DayOutOfRange

	elif month in [4, 6, 9, 11] and day > 30:
		return CheckDateResult.DayOutOfRange

	return CheckDateResult.Valid


class CheckDateResult(Enum):
	Valid = 1
	ContainsNotNum = 2
	YearOutOfRange = 3
	MonthOutOfRange = 4
	DayOutOfRange = 5