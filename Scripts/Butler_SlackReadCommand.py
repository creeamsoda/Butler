from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
import sys
import json
import datetime
import BotDataManager
import SaveData
import MessageParser
import UpdateSchedule

# FIXME コマンドライン引数のかずのチェック 
SLACK_BOT_TOKEN = sys.argv[1]

client = WebClient(token=SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)

print("Command Run")

# Store conversation history
conversation_history = []
# ID of the channel you want to send the message to
channel_id = sys.argv[2]


botDataManager = BotDataManager.BotDataManager()
data = botDataManager.Data
ownMessageTss = data["ownMessageTs"]
print("ownMessageTs")
for ts in ownMessageTss:
    print(ts)

saveData = SaveData.SaveData()

latestLoadTs=data["latestLoadMessageTimeStamp"]

try:
    # Call the conversations.history method using the WebClient
    # conversations.history returns the first 100 messages by default
    # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
    # すでに取得済みのメッセージより後に送られたものだけを取得
    result = client.conversations_history(channel=channel_id,oldest=latestLoadTs, limit=30)

    conversation_history = result["messages"]

    # Print results
    logger.info("{} messages found in {}".format(len(conversation_history), channel_id))
    for message in conversation_history:
        #print("Message: {}".format(message.get("text", "No text found")))
        print(conversation_history)

    mentionedHistory = MessageParser.GetMentionedMessage(conversation_history)
    registrationList = MessageParser.ParseRegistration(mentionedHistory)
    if registrationList is not None:
        for registration in registrationList:
            # 登録処理
            newData = saveData.CreateAnimeData(registration)
            saveData.Data["animes"].append(newData)

    watchedNameList = MessageParser.ParseWatched(mentionedHistory)
    if watchedNameList is not None:
        for watchedName in watchedNameList:
            # 見た処理
            saveData.SetWatched(watchedName)
            print(f"{watchedName}見た")

    # タイムスタンプを更新
    if conversation_history:
        data["latestLoadMessageTimeStamp"] = conversation_history[0]["ts"]

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))


"""
try:
    # Call the chat.postMessage method using the WebClient
    postResult = client.chat_postMessage(
        channel=channel_id, 
        text="Hello world6"
    )
    print(postResult["ts"])
    ownMessageTss.append(postResult["ts"])
    logger.info(postResult)

except SlackApiError as e:
    logger.error(f"Error posting message: {e}")
"""
"""
スレッド内のやつを取るのは一旦諦める

getReplyResults = []
for ownMessageTs in ownMessageTss:
    try:
        # Call the conversations.replies method using the WebClient
        getReplyResults.append(client.conversations_replies(
            channel=channel_id,
            ts=ownMessageTs
        ))
    except SlackApiError as e:
        logger.error(f"Error getting replies: {e}")


mentionedReplies = []
for getReplyResult in getReplyResults:
    if getReplyResult["ok"]:
        for message in getReplyResult["messages"]:
            if "text" in message and "@U094M8WTYRZ" in message["text"]:
                mentionedReplies.append(message)

(watchedTsAndNumListThread, watchedNameListThread) = MessageParser.ParseWatchedInThread(mentionedReplies)
if watchedNameListThread is not None:
    for watchedName in watchedNameListThread:
        # 見た処理
        saveData.SetWatched(watchedName)
        print(f"{watchedName}見た")

if watchedTsAndNumListThread is not None:
    for watchedTsAndNum in watchedTsAndNumListThread:
        # 見た処理。まずは返信先のメッセージを取得してインデックスを取得
        threadTs = watchedTsAndNumListThread[0]
        indexAndNameList = []
        for message in conversation_history:
            if message["ts"] == threadTs:
                # メッセージのインデックスを取得
                indexAndNameList = MessageParser.GetIndexAndNameListFromMessage(message)
        if indexAndNameList is not None:
            for index in watchedTsAndNumListThread[1:]:
                if index < len(indexAndNameList):
                    watchedName = indexAndNameList[index]
                    saveData.SetWatched(watchedName)
                    print(f"{watchedName}を番号で見た")
        


print("mentionsReplies")
print(mentionedReplies)
"""

data["ownMessageTs"] = ownMessageTss


# jsonにセーブ
botDataManager.WriteSaveData(data)
saveData.WriteSaveData(saveData.Data)