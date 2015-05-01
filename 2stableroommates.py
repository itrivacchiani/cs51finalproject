import copy, sys, csv, os

csv_f = csv.reader(open('preferences.csv', 'rU'))

problem = csv_f.next()[0].lower()
# csv file does not correctly indicate stable marriage or 
# hospital resident as the problem to be solved
if (problem != "stable roommates" and problem != "stable roommate"):
  if (problem == "stable marriage" or problem == "hospital resident"):
    print("preferences.csv indicates stable marriage or hospital resident as the problem rather than stable roommates.")
    print("\nPlease choose a new problem in the menu or edit the problem name in preferences.csv")
  else:
    print("\n\npreferences.csv does not indicate a possible problem.")
    print("Please change the problem name in preferences.csv to \nstable marriage, hospital resident, or stable roommates.")
    print("Then make the appropriate problem choice.")
  os.system("python menu.py")

num_roommates = int(csv_f.next()[0])

people = {}
for i in xrange(0, num_roommates):
  s1 = csv_f.next()[0]
  s2 = csv_f.next()[0]
  people[s1] = s2.split(' ')

for k in people.keys():
  print("%s "%k)
  for x in people[k]:
    print("%s"%x)

def fillRank(people):
  rank = {}
  for k in people.keys():
    rank[k] = {}
    for v in people[k]:
      rank[k][v] = people[k].index(v)
  return rank

rank = fillRank(people)

# Given a person x and a position i,
# this function will return a tuple (y,r) where
# y is the person of rank i on x's preference list
# and r is the rank of x in y's preference list.
def GetPersonRank(x,i):
  y = people[x][i]
  r = rank[y][x]
  return (y,r)

leftperson = {} # person 'x' is currently proposing to
leftrank = {} # rank of that person
rightperson = {} # person 'x' holds a proposal for
rightrank = {} # rank of that person
holds_proposal = {} # boolean

# PhaseI creates plausible semi-matchings 
# between roommates
def phaseI(): 

  # initialization
  for k in people.keys():
    n = len(people.keys())
    holds_proposal[k] = False
    rightperson[k] = k 
    rightrank[k] = n
    leftrank[k] = 1
  # creates semi-engagements (plausible matches)
  for k in people.keys():
    proposer = k
    while True: 
      (next, rank) = GetPersonRank(proposer, leftrank[proposer])
      while (rank > rightrank[next]):
        leftrank[proposer] = leftrank[proposer] + 1 
        (next, rank) = GetPersonRank(proposer, leftrank[proposer])
      previous = rightperson[next]
      rightrank[next] = rank
      rightperson[next] = proposer
      leftperson[proposer] = next
      proposer = previous 
      if (holds_proposal[next] == False): 
        break 
    holds_proposal[next] = True
    if (leftrank[proposer] == n):
      return False # can only be engaged to self, no stable match
  return True # move onto phaseII, there may be stable match

cycle = []

def seekCycle(): 

  for k in people.keys():
    if (leftrank[k] < rightrank[k]):
      break
  if (leftrank[k] >= rightrank[k]):
    return (0,0,"")
  else :
    last = 1 
    while True:
      cycle[last] = k
      last = last + 1 
      p = leftrank[k]
      while True: 
        p = p + 1 
        (y,r) = GetPersonRank(k,p)
        if (r <= rightrank[y]):
          break
      secondrank[k] = p
      secondperson[k] = y
      secondrightrank[k] = r
      k = rightperson[secondperson[x]]
      if (k in cycle):
        break 
    last = last - 1
    first = last - 1
    while (cycle[first] != k):
      first = first - 1 
    return (first, last, cycle)

cycle2 = []

def phaseII():
  solution_possible = True
  solution_found = False 
  while (solution_possible and not solution_found):
    (first, last, cycle) = seekCycle()
    if (cycle == ""):
      solution_found = True 
    else:
      cycle2 = cycle[first:last]
      for i in range(cycle2):
        leftrank[k] = secondrank[k]
        rightrank[leftperson[k]] = secondrightrank[k]
        rightperson[leftperson[k]] = k
      for i in range(cycle2):
        if (leftrank[k] > rightrank[k]):
          sol_possible = False 
  return solution_found

print("hi")

if not phaseI:
  print("There is no possible stable roommates arrangement")
  os.system("python menu.py")
else:
  if not phaseII:
    print("There is no solution.")
    os.system("python menu.py")
  else:
    print ("hi")
    for i in cycle2:
      print("%s" % i)
    for i in cycle:
      print("%s" % i)
      print("hi")


