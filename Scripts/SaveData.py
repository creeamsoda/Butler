﻿import json
from pathlib import Path
import Common

SAVE_DATA_FILE_PATH = Path(r"./Data/SaveData.json")

class SaveData():
    #インスタンス作成時にデータを読み込む
    def __init__(self):
        self.Data = self.ReadSaveData()

    # jsonを読み込んで辞書型を返す関数
    @classmethod
    def ReadSaveData(self):
        try:
            saveDataFile = open(SAVE_DATA_FILE_PATH, mode="r", encoding="utf-8_sig")
            saveData = json.load(saveDataFile)
            animes = saveData["animes"]
            saveDataFile.close()
            return saveData

        except FileNotFoundError as e:
            print(f"Save data file not found. Please ensure the file exists.{e}")
            return []

        except json.JSONDecodeError:
            print("Error decoding JSON from save data file.")
            saveDataFile.close()
            return []

    def WriteSaveData(self, saveData):
        try:
            saveDataFile = open(SAVE_DATA_FILE_PATH, mode="w", encoding="utf-8_sig")
            json.dump(saveData, saveDataFile, indent=4, ensure_ascii=False)
            saveDataFile.close()
            print("Save data written successfully.")
        except IOError as e:
            print(f"Error writing to save data file: {e}")

    def CreateAnimeData(self, entryData):
        return {"name":entryData["name"], "nextDate":entryData["nextDate"], "time":entryData["time"], "nextEpisode":entryData["nextEpisode"], "isNextReleased":False, "isNextLast":False}

    def SetWatched(self, name):
        for anime in self.Data["animes"]:
            if anime["name"] == name:
                anime["nextDate"] = Common.GetOneWeekLaterDate(anime["nextDate"])
                anime["nextEpisode"] = str(int(anime["nextEpisode"]) + 1)
                anime["isNextReleased"] = False
                break
        self.WriteSaveData(self.Data)
