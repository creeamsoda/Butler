import tkinter as tk
from unittest import result

import CheckDataFormat as CD

#数字のみを受け付けるフォーム
class NumberEntry():
	def __init__(self, frame, EntryGrid):
		self.entryFrame = tk.Frame(frame)
		self.entryFrame.grid(row=EntryGrid[0], column=EntryGrid[1])
		self.entry = tk.Entry(self.entryFrame, width=32)
		self.entry.grid(row=0, column=0)
		self.suggestTextVariable = tk.StringVar()
		self.suggestMessage = tk.Message(self.entryFrame, textvariable=self.suggestTextVariable)
		self.suggestMessage.grid(row=1, columnspan=2)
		self.validateCommand = (self.entry.register(self.CheckNumber), "%P")
		self.entry.configure(validate='all', validatecommand=self.validateCommand)

	def CheckNumber(self, entryString):
		#入力変更を許可した場合の文字列が引数としてPに渡される
		entryString = entryString
		result = CD.CheckNumber(entryString)
		if result == CD.CheckNumberResult.Valid:
			self.suggestTextVariable.set("有効な入力です")
			
		elif result == CD.CheckNumberResult.ContainsNotNum:
			self.suggestTextVariable.set("数字を入力してください")
			
		elif result == CD.CheckNumberResult.LengthOutOfRange:
			self.suggestTextVariable.set("0以上の数字を入力してください")
			
		return True

	def IsValid(self):
		entryString = self.entry.get()
		result = CD.CheckNumber(entryString)
		if result == CD.CheckNumberResult.Valid:
			return True
		else:
			return False

	def Get(self):
		return self.entry.get()

	def DeleteAll(self):
		self.entry.delete(0, tk.END)
		self.suggestTextVariable.set("")

class TimeEntry():
	def __init__(self, frame, EntryGrid):
		self.timeEntryFrame = tk.Frame(frame)
		self.timeEntryFrame.grid(row=EntryGrid[0], column=EntryGrid[1])
		self.hourEntry = tk.Entry(self.timeEntryFrame, width=4)
		self.hourEntry.grid(row=1, column=0)
		self.hourLabel = tk.Label(self.timeEntryFrame, text="時")
		self.hourLabel.grid(row=0, column=0)
		self.minuteEntry = tk.Entry(self.timeEntryFrame, width=4)
		self.minuteEntry.grid(row=1, column=1)
		self.minuteLabel = tk.Label(self.timeEntryFrame, text="分")
		self.minuteLabel.grid(row=0, column=1)
		self.checkTimeResults = [CD.CheckTimeResult.HourOutOfRange, CD.CheckTimeResult.MinuteOutOfRange]
		self.suggestTextVariable = tk.StringVar()
		self.suggestMessage = tk.Message(self.timeEntryFrame, textvariable=self.suggestTextVariable)
		self.suggestMessage.grid(row=2, columnspan=2)
		self.hourValidateCommand = (self.hourEntry.register(self.CheckHourEntry), "%P")
		self.hourEntry.configure(validate='all', validatecommand=self.hourValidateCommand)
		self.minuteValidateCommand = (self.minuteEntry.register(self.CheckMinuteEntry), "%P")
		self.minuteEntry.configure(validate='all', validatecommand=self.minuteValidateCommand)

	def Get(self):
		"""
		時と分を取得する。
		時は2桁、分は2桁の数字で入力すること。
		例: 01:23
		入力がすでに正しい状態であることを前提としている。
		"""
		hourString = self.hourEntry.get()
		minuteString = self.minuteEntry.get()
		if len(hourString) < 2:
			hourString = hourString.zfill(2)
		if len(minuteString) < 2:
			minuteString = minuteString.zfill(2)
		return f"{hourString}:{minuteString}"

	def IsValid(self):
		if self.checkTimeResults == [CD.CheckTimeResult.Valid, CD.CheckTimeResult.Valid]:
			return True
		return False

	def DeleteAll(self):
		self.hourEntry.delete(0, tk.END)
		self.minuteEntry.delete(0, tk.END)
		self.suggestTextVariable.set("")

	def CheckHourEntry(self, entryString):
		entryString = entryString
		result = CD.CheckHour(entryString)
		self.checkTimeResults[0] = result
		self.CheckTimeResultsAndShowSuggestMessage()
		return True

	def CheckMinuteEntry(self, entryString):
		entryString = entryString
		result = CD.CheckMinute(entryString)
		self.checkTimeResults[1] = result
		self.CheckTimeResultsAndShowSuggestMessage()
		return True

	def CheckTimeResultsAndShowSuggestMessage(self):
		self.suggestTextVariable.set("")
		if self.checkTimeResults == [CD.CheckTimeResult.Valid, CD.CheckTimeResult.Valid]:
			self.suggestTextVariable.set("有効な時間です")
			return
		if self.checkTimeResults[0] == CD.CheckTimeResult.ContainsNotNum:
			self.suggestTextVariable.set(self.suggestTextVariable.get()+"\n"+"時の入力は半角数字で入力してください")
		if self.checkTimeResults[1] == CD.CheckTimeResult.ContainsNotNum:
			self.suggestTextVariable.set(self.suggestTextVariable.get()+"\n"+"分の入力は半角数字で入力してください")
		if self.checkTimeResults[0] == CD.CheckTimeResult.HourOutOfRange\
			or self.checkTimeResults[1] == CD.CheckTimeResult.MinuteOutOfRange:
			self.suggestTextVariable.set(self.suggestTextVariable.get()+"\n"+"00:00~23:59までの時間を入力してください")
		

#　エントリーフォームを日付入力に対応させる

class DateEntry():
	def __init__(self, frame, EntryGrid):
		self.dateEntryFrame = tk.Frame(frame)
		self.dateEntryFrame.grid(row=EntryGrid[0], column=EntryGrid[1])
		
		self.yearEntry = tk.Entry(self.dateEntryFrame, width=4)
		self.yearEntry.grid(row=1, column=0)
		self.yearLabel = tk.Label(self.dateEntryFrame, text="年")
		self.yearLabel.grid(row=0, column=0)
		self.monthEntry = tk.Entry(self.dateEntryFrame, width=2)
		self.monthEntry.grid(row=1, column=1)
		self.monthLabel = tk.Label(self.dateEntryFrame, text="月")
		self.monthLabel.grid(row=0, column=1)
		self.dayEntry = tk.Entry(self.dateEntryFrame, width=2)
		self.dayEntry.grid(row=1, column=2)
		self.dayLabel = tk.Label(self.dateEntryFrame, text="日")
		self.dayLabel.grid(row=0, column=2)
		self.checkResults = [CD.CheckDateResult.YearOutOfRange, CD.CheckDateResult.MonthOutOfRange, CD.CheckDateResult.DayOutOfRange]
		self.suggestTextVariable = tk.StringVar()
		self.suggestMessage = tk.Message(self.dateEntryFrame, textvariable=self.suggestTextVariable)
		self.suggestMessage.grid(row=2, columnspan=3)

		#self.validateCommand = (self.entry.register(self.CheckAndModifyEntry), '%d', '%i', '%P', '%s', '%S', '%v', '%V')
		self.yearValidateCommand = (self.yearEntry.register(self.CheckYearEntry), "%P")
		self.yearEntry.configure(validate='all', validatecommand=self.yearValidateCommand)
		self.monthValidateCommand = (self.monthEntry.register(self.CheckMonthEntry), "%P")
		self.monthEntry.configure(validate='all', validatecommand=self.monthValidateCommand)
		self.dayValidateCommand = (self.dayEntry.register(self.CheckDayEntry), "%P")
		self.dayEntry.configure(validate='all', validatecommand=self.dayValidateCommand)

	def Get(self):
		"""
		年、月、日の順に取得する。
		年は4桁、月と日は2桁の数字で入力すること。
		例: 2023-01-01
		入力がすでに正しい状態であることを前提としている。
		"""
		yearString = self.yearEntry.get()
		monthString = self.monthEntry.get()
		dayString = self.dayEntry.get()
		if len(yearString) < 4:
			yearString = yearString.zfill(4)
		if len(monthString) < 2:
			monthString = monthString.zfill(2)
		if len(dayString) < 2:
			dayString = dayString.zfill(2)

		return f"{self.yearEntry.get()}-{self.monthEntry.get()}-{self.dayEntry.get()}"

	def DeleteAll(self):
		self.yearEntry.delete(0, tk.END)
		self.monthEntry.delete(0, tk.END)
		self.dayEntry.delete(0, tk.END)
		self.suggestTextVariable.set("")
		

	"""
	'%d'	Type of action.:
		0: deletion,
		1: insertion,
		-1: focus in, focus out, or a change to the textvariable.

	'%i'	Index of the beginning of the insertion or deletion.
		-1: focus in, focus out, or a change to the textvariable.

	'%P'	The text in the entry will have if the change is allowed.

	'%s'	The text in the entry before the change.

	'%S'	The text in the entry being inserted or deleted.

	'%v'	The current value of the widget's validate option.

	'%V'	The reason for this callback.
		'focusin', 'focusout', 'key', or 'forced'.
		'forced' means the textvariable was changed.

	"""
	def CheckYearEntry(self, entryString):
		entryString = entryString
		result = CD.CheckYear(entryString)
		self.checkResults[0] = result
		self.CheckDateResultsAndShowSuggestMessage()
		#validatecommandは入力を受け付けるかどうかを返す必要があるため、とりあえずTrueを返す
		return True

	def CheckMonthEntry(self, entryString):
		entryString = entryString
		result = CD.CheckMonth(entryString)
		self.checkResults[1] = result
		self.CheckDateResultsAndShowSuggestMessage()
		#validatecommandは入力を受け付けるかどうかを返す必要があるため、とりあえずTrueを返す
		return True

	def CheckDayEntry(self, entryString):
		entryString = entryString
		result = CD.CheckDay(entryString)
		self.checkResults[2] = result
		self.CheckDateResultsAndShowSuggestMessage()
		#validatecommandは入力を受け付けるかどうかを返す必要があるため、とりあえずTrueを返す
		return True

	def CheckDateResultsAndShowSuggestMessage(self):
		print("checkresultsAndShowSuggestM")
		self.suggestTextVariable.set("")

		if self.checkResults == [CD.CheckDateResult.Valid, CD.CheckDateResult.Valid, CD.CheckDateResult.Valid]:
			self.suggestTextVariable.set("有効な日付です")
			return

		if self.checkResults[0]== CD.CheckDateResult.ContainsNotNum:
			self.suggestTextVariable.set(self.suggestTextVariable.get()+"\n"+"年の入力は半角数字で入力してください")
		if self.checkResults[1]== CD.CheckDateResult.ContainsNotNum:
			self.suggestTextVariable.set(self.suggestTextVariable.get()+"\n"+"月の入力は半角数字で入力してください")
		if self.checkResults[2]== CD.CheckDateResult.ContainsNotNum:
			self.suggestTextVariable.set(self.suggestTextVariable.get()+"\n"+"日の入力は半角数字で入力してください")
		
		if self.checkResults[0]== CD.CheckDateResult.YearOutOfRange\
			or self.checkResults[1]== CD.CheckDateResult.MonthOutOfRange\
				or self.checkResults[2]== CD.CheckDateResult.DayOutOfRange:
			self.suggestTextVariable.set(self.suggestTextVariable.get()+"\n"+"対応していない日付です")
		
	def IsValid(self):
		if self.checkResults == [CD.CheckDateResult.Valid, CD.CheckDateResult.Valid, CD.CheckDateResult.Valid]:
			return True
		return False


