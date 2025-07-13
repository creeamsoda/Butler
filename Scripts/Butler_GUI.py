import datetime
import SaveData
import RoopCancel
from Message import AskWatchedMessage
import UpdateSchedule
import MessageManager
import View

def SwitchToRegisterWindow():
    window.ShowRegisterWindow()

def RegisterFromEntry():
    entryData = window.getAllEntry()
    if not window.isAllEntryValid():
        window.ShowRegisterFailLabel(True)
        return
    window.ShowRegisterFailLabel(False)
    #登録処理
    newData = saveData.CreateAnimeData(entryData)
    saveData.Data["animes"].append(newData)
    saveData.WriteSaveData(saveData.Data)
    print("登録完了")
    window.ClearRegisterWindow()
    window.ShowBasicWindow()

if __name__ == "__main__":
    #
    window = View.View()
    window.onRegisterButtonClickCallback.append(RegisterFromEntry)
    window.onShowRegisterWindowButtonClickCallback.append(SwitchToRegisterWindow)

    #データの読み込み
    saveData = SaveData.SaveData()
    animeSchedules = saveData.Data["animes"]
    #現在時から、すでに過ぎたものをピックアップする
    nowDate = datetime.date.today()
    availaableList = UpdateSchedule.GetAvailableList(nowDate, animeSchedules)

    messageManager = MessageManager.MessageManager(window, saveData)
    for available in availaableList:
        messageManager.EnqueueMessage(AskWatchedMessage.AskWatchedMessage(available))


    """
    cancelTest = RoopCancel.RoopCancel()
    cancelId = window.window.after(5000, print, "キャンセルせず")
    cancelTest.setId(window.window, cancelId)
    cancelTest.setOnCancel(print, "キャンセルされました", "引数2つ目")
    cancelTest.setOnCancel(print, "キャンセルされました2", "引数2つ目2")
    cancelTest.cancel()
    """

    window.run()

# 