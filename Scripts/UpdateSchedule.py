import Common

# ���݂̓����ƃX�P�W���[���̃��X�g���󂯎���āA���łɌ��J�ς݂Ŗ������̂��̂����X�g�ɂ��ĕԂ��֐�
def GetAvailableList(nowDate, schedules):
    availables = []
    for schedule in schedules:
        if schedule["isNextReleased"] == True:
            availables.append(schedule)
        elif Common.IsLaterDate(nowDate, schedule["nextDate"]):
            availables.append(schedule)

    return availables


         
             
         
        
    

