import json

SAVE_DATA_FILE_PATH = "SaveData.json"

# jsonを読み込んで辞書型を返す関数
def ReadSaveData():
    try:
        saveDataFile = open(SAVE_DATA_FILE_PATH)
        saveData = json.load(saveDataFile)
        animes = saveData["animes"]
        saveDataFile.close()
        return saveData

    except FileNotFoundError:
        print("Save data file not found. Please ensure the file exists.")
        return []

    except json.JSONDecodeError:
        print("Error decoding JSON from save data file.")
        saveDataFile.close()
        return []

# YYYY-MM-DD形式の日付を比較して、dateがcomperedDateよりも後の日付であればTrueを返す関数
def IsLaterDate(date, comperedDate):
    splitedDate = date.split("-")
    splitedComperedDate = comperedDate.split("-")

    if int(splitedDate[0]) > int(splitedComperedDate[0]):
        return True
    elif int(splitedDate[0]) == int(splitedComperedDate[0]):
        if int(splitedDate[1]) > int(splitedComperedDate[1]):
            return True
        elif int(splitedDate[1]) == int(splitedComperedDate[1]):
            if int(splitedDate[2]) >= int(splitedComperedDate[2]):
                return True

    return False
    

# 現在の日時とスケジュールのリストを受け取って、すでに公開済みで未視聴のものをリストにして返す関数
def GetAvailableList(nowDate, schedules):
    availables = []
    for schedule in schedules:
        if schedule["isNextReleased"] == True:
            availables.append(schedule)
        elif IsLaterDate(nowDate, schedule["nextDate"]):
            availables.append(schedule)

    return availables


         
             
         
        
    

