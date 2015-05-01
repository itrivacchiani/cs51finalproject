import os, sys

systemName = sys.platform

directoryAddress = os.getcwd()

def directorylist_python(dirAddress):
	dirlist = []
	for file in os.listdir(dirAddress):
	  if file.endswith(".py"):
	  	dirlist.append(file)
	return dirlist

directoryList = directorylist_python(directoryAddress)
directoryList.remove("menu.py")
problemNames = ["Hospital Resident or Stable Marriage", \
				"Stable Roommates", \
				"Maximum Cardinality Bipartite Matching", \
<<<<<<< HEAD
				"Min Cost Max Flow", "something"]
=======
				"Min Cost Max Flow", \
				"Max Flow"]
>>>>>>> e48dcad240ae99e2e1fbc4c7ef7b27f430b2c77a
directoryList.sort()

print("\n\nMENU for CS51 Final Project\n")

counter = 0
while counter < len(problemNames):
	print("("+str(counter+1)+") " + problemNames[counter])
	counter += 1

problemNum = int(input("\nWhich problem would you like to solve? (Type a number.) "))
problemFile = directoryList[problemNum - 1]

os.system("python " + problemFile)
