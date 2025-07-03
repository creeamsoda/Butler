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
