<<<<<<< HEAD
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
=======
import copy, sys, csv

csv_f = csv.reader(open('preferences.csv'))
n = int(csv_f.next()[0])

guyprefers = {}
galprefers = {}
for i in xrange(0,n):
    s1 = csv_f.next()[0]
    s2 = csv_f.next()[0]
    guyprefers[s1] = s2.split(' ')
for i in xrange(0,n):
    s1 = csv_f.next()[0]
    s2 = csv_f.next()[0]
    galprefers[s1] = s2.split(' ')

guys = sorted(guyprefers.keys())
gals = sorted(galprefers.keys())


def check(engaged):
    inverseengaged = dict((v,k) for k,v in engaged.items())
    for she, he in engaged.items():
        shelikes = galprefers[she]
        shelikesbetter = shelikes[:shelikes.index(he)]
        helikes = guyprefers[he]
        helikesbetter = helikes[:helikes.index(she)]
        for guy in shelikesbetter:
            guysgirl = inverseengaged[guy]
            guylikes = guyprefers[guy]
            if guylikes.index(guysgirl) > guylikes.index(she):
                print("%s and %s like each other better than "
                      "their present partners: %s and %s, respectively"
                      % (she, guy, he, guysgirl))
                return False
        for gal in helikesbetter:
            girlsguy = engaged[gal]
            gallikes = galprefers[gal]
            if gallikes.index(girlsguy) > gallikes.index(he):
                print("%s and %s like each other better than "
                      "their present partners: %s and %s, respectively"
                      % (he, gal, she, girlsguy))
                return False
    return True

def matchmaker():
    guysfree = guys[:]
    engaged  = {}
    guyprefers2 = copy.deepcopy(guyprefers)
    galprefers2 = copy.deepcopy(galprefers)
    while guysfree:
        guy = guysfree.pop(0)
        guyslist = guyprefers2[guy]
        gal = guyslist.pop(0)
        fiance = engaged.get(gal)
        if not fiance:
            # She's free
            engaged[gal] = guy
            print("  %s and %s" % (guy, gal))
        else:
            # The bounder proposes to an engaged lass!
            galslist = galprefers2[gal]
            if galslist.index(fiance) > galslist.index(guy):
                # She prefers new guy
                engaged[gal] = guy
                print("  %s dumped %s for %s" % (gal, fiance, guy))
                if guyprefers2[fiance]:
                    # Ex has more girls to try
                    guysfree.append(fiance)
            else:
                # She is faithful to old fiance
                if guyslist:
                    # Look again
                    guysfree.append(guy)
    return engaged


print('\nEngagements:')
engaged = matchmaker()

print('\nCouples:')
print('  ' + ',\n  '.join('%s is engaged to %s' % couple
                          for couple in sorted(engaged.items())))
print()
print('Engagement stability check PASSED'
      if check(engaged) else 'Engagement stability check FAILED')

print('\n\nSwapping two fiances to introduce an error')
engaged[gals[0]], engaged[gals[1]] = engaged[gals[1]], engaged[gals[0]]
for gal in gals[:2]:
    print('  %s is now engaged to %s' % (gal, engaged[gal]))
print()
print('Engagement stability check PASSED'
      if check(engaged) else 'Engagement stability check FAILED')
>>>>>>> 1b039a172f720f311c158245bf9a31f51412e48b
