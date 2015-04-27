resident_prefs = {emily : [Stanford, Harvard, Berkeley],
                  jenn : [Harvard, Stanford, Berkeley]}
hospital_prefs = {Stanford : (12, [emily, jenn]),
                  Harvard : (12, [emily, jenn]),
                  Berkeley : (5, [jenn, emily])}

# Initialize all residents and hospitals to free
resident_free = (resident_prefs.keys())[:]
hospital_actual = {}

# to initialize hospitals_res to have the same keys
# as hinfo but with values (that are lists) that only
# contain the capacity of each hospital.
for k,v in hospital_prefs.items():
	hospital_actual[k] = (v[0],[])

while resident_free:
  	res = resident_free.pop(0)
    res_pref = resident_prefs[res]
    fav_hosp = res_pref.pop(0)
    # the first term in the value (that is a tuple of capacity and resident list)
    
    # first add the resident to the hospital's resident list regardless
    # of capacity. sort the list based on hospital's preference list.
    hospital_actual[fav_hosp][1] += res
    hospital_actual[fav_hosp][1].sort(key=lambda x: hospital_prefs[fav_hosp][1].index(x))
      
    # the hospital is beyond capacity so we add the last (least preferred resident)
    # to resident_free and remove the last resident from the hospital's resident list.
    if (len(hospital_actual[fav_hosp][1]) > hospital_actual[fav_hosp][0]):
      	resident_free.append(hospital_actual[fav_hosp][1][-1])
        hospital_actual[fav_hosp] = hospital_actual[fav_hosp][1][:-1]
