import copy

resident_prefs = {'emily' : ['Stanford', 'Harvard', 'Berkeley', 'Yale', 'Princeton'],
                  'jenn' : ['Harvard', 'Stanford', 'Yale', 'Princeton', 'Berkeley'],
                  'angela' : ['Harvard', 'Princeton', 'Stanford', 'Yale', 'Berkeley'],
                  'elise' : ['Princeton', 'Stanford', 'Yale', 'Berkeley', 'Harvard'],
                  'pascale' : ['Yale', 'Stanford', 'Harvard', 'Berkeley', 'Princeton'],
                  'sam' : ['Yale', 'Stanford', 'Harvard', 'Berkeley', 'Princeton']}
hospital_prefs = {'Stanford' : (1, ['emily', 'angela', 'elise', 'jenn', 'sam', 'pascale']),
                  'Harvard' : (2, ['pascale', 'emily', 'sam','angela', 'elise', 'jenn']),
                  'Berkeley' : (1, ['jenn', 'angela', 'emily', 'elise', 'pascale']),
                  'Princeton' : (1, ['pascale', 'sam','angela', 'emily', 'jenn', 'elise']),
                  'Yale' : (1, ['sam','jenn', 'elise', 'pascale', 'emily', 'angela'])}

def matcher():
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
        print(" %s placed at %s" % (res, fav_hosp))
      else:
        # hospital's residence list is over capacity
        # need to reject one resident
        # sort list based on hospital's preference list,
        # and reject last resident of list
        fav_hosp_reslist.sort(key=lambda x: hospital_prefs[fav_hosp][1].index(x))
        rejected_res = fav_hosp_reslist[-1]
        fav_hosp_reslist.pop()
        print(" %s rejected by %s" % (rejected_res, fav_hosp))
        rejected_res_pref = resident_prefs2[rejected_res]
        if rejected_res_pref:
          resident_free.append(rejected_res)

  print(" \n .......Final Results.......")
  for k,v in hospital_actual.items():
    print(" \n Hospital of %s | Capacity of %s" % (k, v[0]))
    print(" Residents:")
    for r in v[1]:
      print(" %s " % r)

def checker():
