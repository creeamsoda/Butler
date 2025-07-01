import json

SAVE_DATA_FILE_PATH = "SaveData.json"

# json��ǂݍ���Ŏ����^��Ԃ��֐�
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

# YYYY-MM-DD�`���̓��t���r���āAdate��comperedDate������̓��t�ł����True��Ԃ��֐�
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
    

# ���݂̓����ƃX�P�W���[���̃��X�g���󂯎���āA���łɌ��J�ς݂Ŗ������̂��̂����X�g�ɂ��ĕԂ��֐�
def GetAvailableList(nowDate, schedules):
    availables = []
    for schedule in schedules:
        if schedule["isNextReleased"] == True:
            availables.append(schedule)
        elif IsLaterDate(nowDate, schedule["nextDate"]):
            availables.append(schedule)

    return availables


         
             
         
        
    

