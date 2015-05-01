import copy, sys, csv, os

csv_f = csv.reader(open('preferences.csv', 'rU'))

problem = csv_f.next()[0].lower()
# csv file does not correctly indicate stable marriage or 
# hospital resident as the problem to be solved
if (problem != "stable marriage" and problem != "hospital resident"):
	if (problem == "stable roommate" or problem == "stable roommates"):
		print("preferences.csv indicates stable roommates as the problem rather than stable marriage or hospital resident.")
		print("\nPlease choose a new problem in the menu or edit the problem name in preferences.csv")
	else:
		print("\n\npreferences.csv does not indicate a possible problem.")
		print("Please change the problem name in preferences.csv to \nstable marriage, hospital resident, or stable roommates.")
		print("Exiting to menu.")
	os.system("python menu.py")

marriage = (problem == "stable marriage")
num_res = int(csv_f.next()[0])
num_hosp = int(csv_f.next()[0])

resident_prefs = {}
hospital_prefs = {}
for i in xrange(num_res):
	s1 = csv_f.next()[0]
	s2 = csv_f.next()[0]
	resident_prefs[s1] = s2.split(' ')
for i in xrange(num_hosp):
	s1 = csv_f.next()[0]
	s2 = csv_f.next()[0]
	if marriage:
		hospital_prefs[s1] = (1, s2.split(' '))
	else:
		hospital_prefs[s1.split(' ')[0]] = (int(s1.split(' ')[1]), s2.split(' '))


# Initialize all residents and hospitals to free
resident_free = (resident_prefs.keys())[:]
hospital_actual = {}
hospital_prefs2 = copy.deepcopy(hospital_prefs)
resident_prefs2 = copy.deepcopy(resident_prefs)

# to initialize hospitals_res to have the same keys
# as hinfo but with values (that are lists) that only
# contain the capacity of each hospital.
for k,v in hospital_prefs.items():
	hospital_actual[k] = (v[0],[])

while resident_free:
	res = resident_free.pop(0)
	res_pref = resident_prefs2[res]
	fav_hosp = res_pref.pop(0)
	fav_hosp_reslist = hospital_actual.get(fav_hosp)[1]
	fav_hosp_cap = hospital_actual.get(fav_hosp)[0]
	# the first term in the value (that is a tuple of capacity and resident list)
	fav_hosp_reslist.append(res)

	if (len(fav_hosp_reslist) <= fav_hosp_cap):
		# can just add resident to list
		if marriage:
			print("%s engaged to %s" % (res, fav_hosp))
		else:
			print("%s placed at %s" % (res, fav_hosp))
	else:
		# hospital's residence list is over capacity
		# need to reject one resident
		# sort list based on hospital's preference list,
		# and reject last resident of list
		fav_hosp_reslist.sort(key=lambda x: hospital_prefs[fav_hosp][1].index(x))
		rejected_res = fav_hosp_reslist[-1]
		fav_hosp_reslist.pop()
		print("%s rejected by %s" % (rejected_res, fav_hosp))
		rejected_res_pref = resident_prefs2[rejected_res]
		if rejected_res_pref:
			resident_free.append(rejected_res)
		else:
			if marriage:
				print("%s rejected by everyone" % rejected_res)
			else:
				print("Resident %s rejected by all hospitals " % rejected_res)

print(" \n .......Final Results.......")
for k,v in hospital_actual.items():
	if marriage:
		print("\n %s is married to %s" % (k,v[1][0]))
	else:
		print("\n Hospital of %s | Capacity of %s" % (k, v[0]))
		print(" Residents:")
		for r in v[1]:
			print("%s " % r)

os.system("python menu.py")