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

def phaseI