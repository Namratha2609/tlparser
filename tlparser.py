import re
import sys

def getTimeLog():
	filename = sys.argv[1]

	report = []
	timeList = []
	flag = False
	count = 1
	totalDiff = 0

	def isCorrect(tempTime):
		first = ""
		second = ""
		if "am" in tempTime:
			first = tempTime.split(" - ")[0].split("am")[0]
			second = tempTime.split(" - ")[1].split("am")[0]
		else:
			first = tempTime.split(" - ")[0].split("pm")[0]
			second = tempTime.split(" - ")[1].split("pm")[0]

		first_h = int(first.split(":")[0])
		if first_h == 12:
			first_h = 0
		first_m = int(first.split(":")[1])
		second_h = int(second.split(":")[0])
		if second_h == 12:
			second_h = 0
		second_m = int(second.split(":")[1])

		timeDiff = (second_h  * 60 + second_m) - (first_h  * 60 + first_m)
		return timeDiff

	def isCorrectPMAM(tempTime):
		first = tempTime.split(" - ")[0].split("pm")[0]
		second = tempTime.split(" - ")[1].split("am")[0]

		first_h = int(first.split(":")[0])
		first_m = int(first.split(":")[1])
		second_h = int(second.split(":")[0])
		if second_h < 12:
			second_h += 12
		second_m = int(second.split(":")[1])
		timeDiff = (second_h  * 60 + second_m) - (first_h  * 60 + first_m)
		return timeDiff

	def isCorrectAMPM(tempTime):
		first = tempTime.split(" - ")[0].split("am")[0]
		second = tempTime.split(" - ")[1].split("pm")[0]
		first_h = int(first.split(":")[0])
		first_m = int(first.split(":")[1])
		second_h = int(second.split(":")[0])
		if second_h != 12:
			second_h += 12
		second_m = int(second.split(":")[1])
		timeDiff = (second_h  * 60 + second_m) - (first_h  * 60 + first_m)
		return timeDiff

	# read file
	with open(filename) as file:
		for temp in file:
			flagCor = False
			if flag:
				if re.findall(r"\d+:\d+am - \d+:\d+am", temp.lower()):
					tempTime = re.findall(r"\d+:\d+am - \d+:\d+am", temp.lower())
					if isCorrect(tempTime[0]) >= 0:
						timeList.append(tempTime[0])
						totalDiff += isCorrect(tempTime[0])
					else:
						report.append(count)
				elif re.findall(r"\d+:\d+am - \d+:\d+pm", temp.lower()):
					tempTime = re.findall(r"\d+:\d+am - \d+:\d+pm", temp.lower())
					totalDiff += isCorrectAMPM(tempTime[0])
					timeList.append(tempTime[0])
				elif re.findall(r"\d+:\d+pm - \d+:\d+pm", temp.lower()):
					tempTime = re.findall(r"\d+:\d+pm - \d+:\d+pm", temp.lower())
					if isCorrect(tempTime[0]) >= 0:
						timeList.append(tempTime[0])
						totalDiff += isCorrect(tempTime[0])
					else:
						report.append(count)
				elif re.findall(r"\d+:\d+pm - \d+:\d+am", temp.lower()):
					tempTime = re.findall(r"\d+:\d+pm - \d+:\d+am", temp.lower())
					totalDiff += isCorrectPMAM(tempTime[0])
					timeList.append(tempTime[0])
				else:
					report.append(count)
			else:
				if "Time Log" in temp:
					flag = True
			count += 1

	print(totalDiff)
	print("Total Period: " + str(totalDiff // 60) + "h " + str(totalDiff % 60) + "m")
	print()
	for temp in report:
		print(str(temp) + " line has some thing error")

if _name_ == "_main_":
	getTimeLog()