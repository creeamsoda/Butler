﻿from enum import Enum

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


def CheckRegisterCommandResult(commandResultDict):
	timeResult = CheckTime(commandResultDict["time"])
	dateResult = CheckDate(commandResultDict["nextDate"])
	nextEpisodeResult = CheckNumber(commandResultDict["nextEpisode"])
	ErrorString = ""
	if timeResult != [CheckTimeResult.Valid]:
		if CheckTimeResult.ContainsNotNum in timeResult:
			ErrorString += f"時間{commandResultDict["time"]}に半角数字以外が含まれています。\n"
		if CheckTimeResult.HourOutOfRange in timeResult:
			ErrorString += f"時間{commandResultDict["time"]}が0～23の範囲外です。\n"
		if CheckTimeResult.MinuteOutOfRange in timeResult:
			ErrorString += f"分{commandResultDict["time"]}が0～59の範囲外です。\n"
	
	if dateResult != [CheckDateResult.Valid]:
		if CheckDateResult.ContainsNotNum in dateResult:
			ErrorString += f"日付{commandResultDict["nextDate"]}に半角数字以外が含まれています。\n"
		if CheckDateResult.YearOutOfRange in dateResult:
			ErrorString += f"年{commandResultDict["nextDate"]}が1900～2100の範囲外です。\n"
		if CheckDateResult.MonthOutOfRange in dateResult:
			ErrorString += f"月{commandResultDict["nextDate"]}が1～12の範囲外です。\n"
		if CheckDateResult.DayOutOfRange in dateResult:
			ErrorString += f"日{commandResultDict["nextDate"]}が1～31の範囲外、もしくはカレンダーにない日付です。\n"

	if nextEpisodeResult != CheckNumberResult.Valid:
		if nextEpisodeResult == CheckNumberResult.ContainsNotNum:
			ErrorString += f"次回エピソード番号{commandResultDict["nextEpisode"]}に半角数字以外が含まれています。\n"
		elif nextEpisodeResult == CheckNumberResult.LengthOutOfRange:
			ErrorString += f"次回エピソード番号{commandResultDict["nextEpisode"]}が0以上の整数ではありません。\n"

	if ErrorString == "":
		return (True, "")
	else:
		return (False, ErrorString)
