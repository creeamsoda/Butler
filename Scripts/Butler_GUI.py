import datetime
import SaveData
import RoopCancel
import UpdateSchedule
import MessageManager
import View

if __name__ == "__main__":
    #
    window = View.View()

    #データの読み込み
    saveData = SaveData.SaveData()
    animeSchedules = saveData.Data["animes"]
    #現在時から、すでに過ぎたものをピックアップする
    nowDate = datetime.date.today()
    availaableList = UpdateSchedule.GetAvailableList(nowDate, animeSchedules)
    cancellation = RoopCancel.RoopCancel()

    for available in availaableList:
        message = MessageManager.CreateAnimeMessage(available)
        kword = {"message":message, "period":0.05, "cancel":cancellation}
        #message=message, period=0.05, cancel=cancellation, startCount=0
        window.ShowMessageOneByOne(message, 0.05, cancellation)

    window.run()
    cancellation.cancel()