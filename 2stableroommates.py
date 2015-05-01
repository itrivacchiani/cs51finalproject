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

best = {} # current best roommate 'x' is currently proposing to
bestrank = {} # rank of x's most feasible choice on x's list
worst = {} # person whose proposal x has but isn't top choice
worstrank = {} # rank of worst's in x's list
holds_proposal = {} # boolean
second = {} # the next best person that x would accept
secondrank = {} # second's rank on x's list
secondperception = {} # rank of x on second[x]'s preference list, 
                      # ie. how second[x] perceives x

# PhaseI creates plausible semi-matchings 
# between roommates
def phaseI(): 

  # initialization
  for k in people.keys():
    n = len(people.keys())
    holds_proposal[k] = False
    worst[k] = k 
    worstrank[k] = n
    bestrank[k] = 0
  # creates semi-engagements (plausible matches)
  for k in people.keys():
    proposer = k
    while True: 
      if bestrank[proposer] == len(people.keys()):
          break
      # next is the "best" person and rank is the perception
      (next, rank) = GetPersonRank(proposer, bestrank[proposer])
      while (rank > worstrank[next]):
        bestrank[proposer] = bestrank[proposer] + 1 
        # You've reached yourself in the bestrank :(, therefore forever alone
        (next, rank) = GetPersonRank(proposer, bestrank[proposer])
      previous = worst[next]
      worstrank[next] = rank
      worst[next] = proposer
      best[proposer] = next
      proposer = previous 
      if (holds_proposal[next] == False): 
        break 
    holds_proposal[next] = True
    if (bestrank[proposer] == n):
      return False # can only be engaged to self, no stable match
  return True # move onto phaseII, there may be stable match

cycle = []

def seekCycle(): 

  for k in people.keys():
    if (bestrank[k] < worstrank[k]):
      break
  if (bestrank[k] >= worstrank[k]):
    return (0,0,"")
  else :
    last = 1 
    while True:
      cycle[last] = k
      last = last + 1 
      p = bestrank[k]
      while True: 
        p = p + 1 
        (y,r) = GetPersonRank(k,p)
        if (r <= worstrank[y]):
          break
      secondrank[k] = p
      second[k] = y
      secondperception[k] = r
      k = worst[second[x]]
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
        bestrank[k] = secondrank[k]
        worstrank[best[k]] = secondperception[k]
        worst[best[k]] = k
      for i in range(cycle2):
        if (bestrank[k] > worstrank[k]):
          solution_possible = False 
  return solution_found

if not phaseI():
  print("There is no possible stable roommates arrangement")
  os.system("python menu.py")
else:
  if not phaseII():
    print("There is no solution.")
    os.system("python menu.py")
  else:   
    print("\n Rooming Results \n")
    for k in best.keys():
      print("Person: %s" % k)
      print("Best Roommate Match: %s \n" % best[k])
