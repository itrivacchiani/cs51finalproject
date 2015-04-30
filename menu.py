import os, sys

systemName = sys.platform

problemsDirAddress = os.getcwd() + "/Problems"

problemsDirList = os.listdir(problemsDirAddress)
problemsDirList.remove("preferences.csv")

counter = 0
while counter < len(problemsDirList):
	print("("+str(count+1)+") " + problemsDirList[count])
	count += 1

print("Welcome to our CS51 Final Project!")
print("By John Gee, Sam Cheng, Angela Ma, and Emily Wang")
print("We implemented the solutions to the following problems.")
print("For the hospital-resident/stable marriage problems, input data into "perferences.csv" in the format specified in the preferences_format file.")
print("For the stable roommates problems, input data into the csv files in the format specified in the writeup.")

problemNum = int(input("Which problem would you like to solve? (Type a number.)"))
problemFile = problemsDirList[problemNum - 1]

if systemName == "darwin":
	os.system("python " + problemFile)
else:
	os.system(problemFile)