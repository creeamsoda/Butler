import CheckDataFormat as CD

# YYYY-MM-DD形式の日付を比較して、dateがcomperedDateよりも後の日付であればTrueを返す関数
def IsLaterDate(date, comperedDate):
    splitedDate = str(date).split("-")
    #splitedDate = date.strftime("%y%m%d").split("-")
    splitedComperedDate = str(comperedDate).split("-")

    if int(splitedDate[0]) > int(splitedComperedDate[0]):
        return True
    elif int(splitedDate[0]) == int(splitedComperedDate[0]):
        if int(splitedDate[1]) > int(splitedComperedDate[1]):
            return True
        elif int(splitedDate[1]) == int(splitedComperedDate[1]):
            if int(splitedDate[2]) >= int(splitedComperedDate[2]):
                return True

    return False

def GetOneWeekLaterDate(date):
    # dateはdatetime.date型であることを想定
    dateList = str(date).split("-")
    nextDateIntList = [int(dateList[0]), int(dateList[1]), int(dateList[2]) + 7]
    results = CD.CheckDate(f"{nextDateIntList[0]}-{nextDateIntList[1]}-{nextDateIntList[2]}")
    if results == [CD.CheckDateResult.Valid]:
        return f"{nextDateIntList[0]}-{nextDateIntList[1]}-{nextDateIntList[2]}"
    # 日付が月をまたぐ場合の処理
    elif nextDateIntList[1] == 2:
        monthEndDay = 28 if nextDateIntList[0] % 4 != 0 or (nextDateIntList[0] % 100 == 0 and nextDateIntList[0] % 400 != 0) else 29
    elif nextDateIntList[1] in [4, 6, 9, 11]:
        monthEndDay = 30
    else:
        monthEndDay = 31

    nextDateIntList[1] += 1
    nextDateIntList[2] = nextDateIntList[2]% monthEndDay

    if nextDateIntList[1] > 12:
        nextDateIntList[1] = 1
        nextDateIntList[0] += 1

    return f"{nextDateIntList[0]}-{nextDateIntList[1]}-{nextDateIntList[2]}"