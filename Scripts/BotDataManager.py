import json
from pathlib import Path

SAVE_DATA_FILE_PATH = Path(r".\Data\BotData.json")

class BotDataManager:
    #インスタンス作成時にデータを読み込む
    def __init__(self):
        self.Data = self.ReadSaveData()

    # jsonを読み込んで辞書型を返す関数
    @classmethod
    def ReadSaveData(self):
        try:
            saveDataFile = open(SAVE_DATA_FILE_PATH, mode="r", encoding="utf-8_sig")
            saveData = json.load(saveDataFile)
            saveDataFile.close()
            return saveData

        except FileNotFoundError:
            print("Save data file not found. Please ensure the file exists.")
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
