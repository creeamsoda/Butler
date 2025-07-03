import Common

# 現在の日時とスケジュールのリストを受け取って、すでに公開済みで未視聴のものをリストにして返す関数
def GetAvailableList(nowDate, schedules):
    availables = []
    for schedule in schedules:
        if schedule["isNextReleased"] == True:
            availables.append(schedule)
        elif Common.IsLaterDate(nowDate, schedule["nextDate"]):
            availables.append(schedule)

    return availables


         
             
         
        
    

