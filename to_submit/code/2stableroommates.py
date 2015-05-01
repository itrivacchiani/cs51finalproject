import copy, sys, csv, os

data = open('preferences.csv', 'rU')
csv_f = csv.reader(data)

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

# fills in all the students from the csv file into
# the people dictionary as keys
people = {}
for i in xrange(0, num_roommates):
  s1 = csv_f.next()[0]
  s2 = csv_f.next()[0]
  people[s1] = s2.split(' ')

# generates a dictionary rank given the people dictionary
# such that rank[y,x] is y's rank on x's list
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
# current best possible roommate 'x' is proposing to
best = {} 
# rank of x's most feasible roommate choice
bestrank = {} 
# person whose proposal x has but isn't x's top choice
worst = {} 
# rank of worst in x's list
worstrank = {} 
# boolean
holds_proposal = {} 
# the next best person that x would accept
second = {}
# second's rank on x's list 
secondrank = {} 
# rank of x on second[x]'s preference list, 
# ie. how second[x] perceives x
secondperception = {}                  

# PhaseI creates plausible semi-matchings 
# between roommates
def phaseI(): 
  # initializing
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
      # next is the k's top choice, rank is best's perception of k
      (next, rank) = GetPersonRank(proposer, bestrank[proposer])
      # next prefers its current match better than k
      while (rank > worstrank[next]):
        # proposer must move on 
        bestrank[proposer] = bestrank[proposer] + 1 
        (next, rank) = GetPersonRank(proposer, bestrank[proposer])
      # previous proposed to next
      previous = worst[next]
      worstrank[next] = rank
      worst[next] = proposer
      best[proposer] = next
      proposer = previous 
      if (holds_proposal[next] == False): 
        break 
    holds_proposal[next] = True
    if (bestrank[proposer] == n):
      # can only be engaged to self, no stable match
      return False 
  # move onto phaseII, there may be stable match
  return True 

cycle = []

# finds the potential "rotations" for previous semi-matching
# to be broken apart to form new matches 
def seekCycle(): 
  for k in people.keys():
    # find unmatched person
    if (bestrank[k] < worstrank[k]):
      break
  # no unmatched person found -> return empty cycle, no work! 
  if (bestrank[k] >= worstrank[k]):
    return (0,0,"")
  # unmatched person found
  else :
    last = 1 
    while True:
      cycle[last] = k
      last = last + 1 
      p = bestrank[k]
      while True:
        # find second choice  
        p = p + 1 
        (y,r) = GetPersonRank(k,p)
        # y would accept because k is higher in rank
        if (r <= worstrank[y]):
          break
      # saving the second choice
      secondrank[k] = p
      second[k] = y
      secondperception[k] = r
      k = worst[second[x]]
      if (k in cycle):
        break 
    last = last - 1
    first = last - 1
    # start cycle again
    while (cycle[first] != k):
      first = first - 1 
    return (first, last, cycle)

# based on seekCycle results
cycle2 = []

def phaseII():
  solution_possible = True
  solution_found = False 
  while (solution_possible and not solution_found):
    (first, last, cycle) = seekCycle()
    # stable rooming matches are already present
    if (cycle == ""):
      solution_found = True 
    else:
      cycle2 = cycle[first:last]
      # executing the switches and new arrangements
      for i in range(cycle2):
        bestrank[k] = secondrank[k]
        worstrank[best[k]] = secondperception[k]
        worst[best[k]] = k
      for i in range(cycle2):
        # gone through everybody, no stable match is possible
        if (bestrank[k] > worstrank[k]):
          solution_possible = False 
  return solution_found

# output of the matching results (or that no matching is possible)
if not phaseI() or not phaseII():
  print("There is no stable rooming situation")
else:   
  print("\n Rooming Results \n")
  for k in best.keys():
    print("Person: %s" % k)
    print("Best Roommate Match: %s \n" % best[k])

data.close()
os.system("python menu.py")