from ast import pattern
import re

import CheckDataFormat

def GetMentionedMessage(messageList):
	mentionedList = []
	for message in messageList:
		if not "text" in message:
			continue
		if "@U094M8WTYRZ" in message["text"]:
			mentionedList.append(message)

	return mentionedList


def ParseRegistration(messageList):
	"""
		コマンド
		@(ボットのメンション) 登録 "<アニメ名>" <放送開始時(0~23)>:<放送開始分(0~59)> <次回放送日(yyyy-mm-dd)> <次回エピソード番号>
		時間、日付で一桁の場合でもゼロ埋めをしなくてもいい
		例: @bot 登録 "機動戦士ガンダム GQuuuuuux" 0:29 2025-04-09 1
	"""
	registrationList = []
	for message in messageList:
		text = message["text"]
		# 正規表現でコマンドを解釈する
		# 項目間の空白はなくてもなんとかなるよう柔軟に解釈する。
		# 連続でコマンドをうったときに、前のコマンド丸ごとをタイトルとして認識しないよう、[^\n]で改行を目印にしている
		# [\"\'](.+?)[\"\']にしないのは"や'を含むタイトルを登録できるようにするため
		pattern = r"登録\s*?[\"\']([^\n]+)[\"\']\s*(\d\d?)\s*:\s*(\d\d?)\s*(\d{4}\s*-\d\d?\s*-\d\d?)\s*(\d+)"
		matchResult = re.findall(pattern, text)
		if matchResult:
			for match in matchResult:
				animeName = match[0]
				hour = match[1]
				minute = match[2]
				time = f"{hour.zfill(2)}:{minute.zfill(2)}"
				date = match[3]
				nextEpisode = match[4]
				registerCommandResult = {
					"name": animeName,
					"time": time,
					"nextDate": date,
					"nextEpisode": nextEpisode
				}
				formatCheck = CheckDataFormat.CheckRegisterCommandResult(registerCommandResult)
				if formatCheck[0] == True:
					registrationList.append(registerCommandResult)
				else:
					print("Error:不正な登録コマンド"+formatCheck[1])

		return registrationList

def ParseWatched(messageList):
	"""
		コマンド
		@(ボットのメンション) 見た "<アニメ名>"(,"<さらに続けて他のアニメ名>")
		例: @bot 見た "機動戦士ガンダム GQuuuuuux", "鬼滅の刃"
	"""
	watchedNameList = []
	for message in messageList:
		text = message["text"]
		# 見たコマンドの正規表現
		# 登録コマンドのようにタイトルには"や'を許容する一方で改行は許容しない。
		# その後で[\"\']\s*,\s*[\"\']のパターンでsplitをすることで, 万が一2つのタイトルをまとめて一つと解釈してしまっても分けれるようにする。
		ArgumentsPattern = r"見た(?:\s*[\"\']([^\n]+)[\"\']\s*,)*\s*[\"\']([^\n]+)[\"\']"
		ArgumentsMatchResult = re.findall(ArgumentsPattern, text)

		print("ParseWatched:matchResult:", ArgumentsMatchResult)
		print(r"matchTest [\"\']\s*,\s[\"\']", re.findall(r"[\"\']\s*,\s[\"\']",text))

		titleMatchResult = []
		for match in ArgumentsMatchResult:
			if len(match) == 1:
				for title in re.split(r"[\"\']\s*,\s[\"\']", match):
					titleMatchResult.append(title)
			elif len(match) > 1:
				for matchInOneCommand in match:
					for title in re.split(r"[\"\']\s*,\s[\"\']", matchInOneCommand):
						titleMatchResult.append(title)
			for title in titleMatchResult:
				watchedNameList.append(title)
			print("titleMatchResult:", titleMatchResult)
			titleMatchResult = []


	return watchedNameList

def ParseWatchedInThread(messageList):
	"""
		コマンド
		@(ボットのメンション) 見た "<アニメ名>"(,"<さらに続けて他のアニメ名>")
		例: @bot 見た "機動戦士ガンダム GQuuuuuux", "鬼滅の刃"
		または、未視聴リストの番号に合わせて
		@(ボットのメンション) 見た <リストの番号>(,<リストの番号>)
		例: @bot 見た 1,3,4
		いちおうタイトルと番号が混在していても対応できるようにする。
		例: @bot 見た "機動戦士ガンダム GQuuuuuux", 3, "鬼滅の刃", 1, 2
	"""

	watchedNameList = []
	watchedTsAndNumList = []
	for message in messageList:
		text = message["text"]
		#pattern = r"見た(?:\s*[\"\']([^\n]+)[\"\']\s*,|\s*(\d+)\s*,)*\s*[\"\']([^\n]+)[\"\']|\s*(\d+)"
		#pattern = r"見た\s*[\"\']?([^\n]+)(?:(?<=\d)\s*[\n|$]|[\"\']\s*[\n|$])"
		#pattern = r"見た\s*[\"\']([^\n]+?)[\"\']\s*\n?\Z|見た\s*(\d+[^\n]+?)[\"\']\s*\n?\Z|見た\s*(\d+[^\n]*?\d+)\s*\n?\Z|見た\s*[\"\']([^\n]+?\d+)\s*\n?\Z"
		pattern = r"見た\s*[\"\']([^\n]+?)[\"\'](?:\s*\n|\s*$)|見た\s*(\d+[^\n]+?)[\"\'](?:\s*\n|\s*$)|見た\s*(\d+[^\n]*?\d+)(?:\s*\n|\s*$)|見た\s*[\"\']([^\n]+?\d+)(?:\s*\n|\s*$)"
		matchResult = re.findall(pattern, text)
		print("text:",repr(text))
		print("matchResult:InThread",matchResult)

		if matchResult:
			# 一つのメッセージに対する返信内のコマンドの結果を一つのリストにまとめる
			watchedNumListInOneMessage = [message["thread_ts"]]
			for match in matchResult:
				for i in range(0, 4):
					if match[i] == "":
						continue

					# まずはタイトル部分のみ抽出
					titles = re.split(r"[\"\']\s*,(?:\s*\d*\s*,)*\s*[\"\']", match[i])
					# FIXME↑先頭と末尾の数字引数の削除([0]とかでアクセスして数字とカンマ以外をgetで良さそう)
					# 次に数字部分のみ抽出
					nums = []
					if i == 0:
						# matchResultは先頭がタイトル文字列、末尾もタイトル文字列
						numsArgs = re.findall(r"[\"\']\s*,((?:\s*\d+\s*,)+)*\s*[\"\']",match[i])
					elif i == 1:
						# matchResultは先頭が数字、末尾がタイトル文字列
						numsArgs = re.findall(r"[\"\']\s*,((?:\s*\d+\s*,)+)*\s*[\"\']",match[i])
						for num in re.search(r"^(?:(\d+)\s*,\s*)+",match[i]):
							numsArgs.append(num)
					elif i == 2:
						# matchResultは先頭が数字、末尾も数字
						numsArgs = re.findall(r"[\"\']\s*,((?:\s*\d+\s*,)+)*\s*[\"\']",match[i])
						if len(titles) == 0:
							# すべて数字
							for num in re.split(r"\s*,\s*",match[i]):
								numsArgs.append(num)
						else:
							# タイトル文字列を一つ以上含む
							for num in re.search(r"^(?:(\d+)\s*,\s*)+[\"\']",match[i]):
								numsArgs.append(num)
							for num in re.search(r"[\"\'](?:\s*,\s*(\d+))*\s*$",match[i]):
								numsArgs.append(num)
					elif i == 3:
						# matchResultは先頭がタイトル文字列、末尾が数字
						numsArgs = re.findall(r"[\"\']\s*,((?:\s*\d+\s*,)+)*\s*[\"\']",match[i])
						for num in re.search(r"[\"\'](?:\s*,\s*(\d+))*\s*$",match[i]):
								numsArgs.append(num)

				print("titles:",titles)
				print("numArgs:", numsArgs)
			"""
			for match in matchResult:
				if len(match) == 1:
					# タイトルが一つだけの場合
					try:
						num = int(match)
						watchedNumListInOneMessage.append(num)
					except ValueError:
						# 数字に変換できない場合はタイトルとして扱う
						for title in re.split(r"[\"\']\s*,\s[\"\']", match):
							watchedNameList.append(title)
				elif len(match) > 1:
					for nameOrNum in match:
						try:
							num = int(nameOrNum)
							watchedNumListInOneMessage.append(num)
						except ValueError:
							# 数字に変換できない場合はタイトルとして扱う
							watchedNameList.append(re.split(r"[\"\']\s*,\s[\"\']", nameOrNum))
			watchedTsAndNumList.append(watchedNumListInOneMessage)
	print(f"watchedTsAndNumList{watchedTsAndNumList}\nwatchedNameList{watchedNameList}")
	return (watchedTsAndNumList,watchedNameList)
"""

# 見たコマンドなどでアニメを番号指定されたときに、どの番号がどのアニメに対応していたかを自分が送った元の未視聴リマインドメッセージから取得する関数
def GetIndexFromRemindMessage(remindMessage):
	text = remindMessage["text"]
	pattern = r"\d+\. (.*?) 第(\d+)話\n"
	matchResult = re.search(pattern, text)
	indexAndNameList = []
	for match in matchResult:
		name = match
		indexAndNameList.append(name)
	return indexAndNameList