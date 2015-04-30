people = {'angela' : ['emily','audrey','stephanie'],
          'emily' : ['angela','stephanie','audrey'],
          'stephanie' : ['audrey','emily','angela'],
          'audrey' : ['angela','stephanie','emily']}

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
def getPersonRank(x,i):
  y = people[x][i]
  r = rank[y][x]
  return (y,r)

# PhaseI creates plausible semi-matchings 
# between roommates
def phaseI(): 
  leftperson = {} # person 'x' is currently proposing to
  leftrank = {} # rank of that person
  rightperson = {} # person 'x' holds a proposal for
  rightrank = {} # rank of that person
  holds_proposal = {} # boolean

  # initialization
  for k in people.keys():
    n = len(people.keys())
    holds_proposal[k] =: false
    rightperson[k] = k 
    rightrank[k] = n
    leftrank[k] = 1
  # creates semi-engagements (plausible matches)
  for k in people.keys():
    proposer = k
    while true: 
      (next, rank) = GetPersonRank(proposer, leftrank[proposer])
      while (rank > rightrank[next]):
        leftrank[proposer] = leftrank[proposer] + 1 
        (next, rank) = GetPersonRank(proposer, leftrank[proposer])
      previous = rightperson[next]
      rightrank[next] = rank
      rightperson[next] = proposer
      leftperson[proposer] = next
      proposer = previous 
      if (holds_proposal[next] == false): 
        break 
    holds_proposal[next] = true
    if (leftrank[proposer] == n):
      return false # can only be engaged to self, no stable match
  return true # move onto phaseII, there may be stable match

def seekCycle(): 
  cycle = []

  for k in people.keys():
    if (leftrank[k] < rightrank[k]):
      break
  if (leftrank[k] >== rightrank[k]):
    return (0,0,"")
  else 
    last = 1 
    while true:
      cycle[last] = k
      last = last + 1 
      p = leftrank[k]
      while true: 
        p = p + 1 
        (y,r) = GetPersonRank(k,p)
        if (r <== rightrank[y]):
          break
      secondrank[k] = p
      secondperson[k] = y
      secondrightrank[k] = r
      k = rightperson[secondperson[x]]
      if (k in cycle):
        break 
    last = last - 1
    first = last - 1
    while (cycle[first] !== k):
      first = first - 1 
    return (first, last, cycle)

def phaseII():
  solution_possible = true
  solution_found = false 
  while (solution_possible && !solution_found):
    (first, last, cycle) = seekCycle()
    if (cycle == ""):
      solution_found = true 
    else 
      cycle2 = cycle[first:last]
      for i in range(cycle2):
        leftrank[k] = secondrank[k]
        rightrank[leftperson[k]] = secondrightrank[k]
        rightperson[leftperson[k]] = k
      for i in range(cycle2):
        if (leftrank[k] > rightrank[k]):
          sol_possible = false 
  return solution_found



