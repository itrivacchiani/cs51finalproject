Instructions

Our algorithms are quite easy to use; they are accessed through a standard I/O interface in menu.py. To begin, execute “python menu.py” from your terminal (we assume you have at least Python 2.7 installed - Windows users might have a problem based  on how your terminal emulator is set up, but you can easily get around this by using the CS50 appliance). You’ll be greeted with an enumerated list of the problems for which we wrote algorithms to solve. To run the algorithm, select a problem and enter its number. You’ll notice that the algorithm runs immediately, prints a solution to the terminal, and returns to the menu. The algorithm ran on a .csv file that is included in our project directory and which can be edited to change the input. The format for inputs to each problem are as follows (currently we only work with integer capacities and weights/costs):

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Hospital Resident or Stable Marriage

in preferences.csv
---------------------------------------
hospital resident
<number of “residents”>
<number of “hospitals”>
<resident0_name>
<hospitals in order of resident0’s decreasing preference, separated by space>
<resident1_name>
<hospitals in order of resident1’s decreasing preference, separated by space>
...
<hospital0_name and capacity, separated by a space>
<residents in order of hospital0’s decreasing preference, separated by space>
<hospital1_name and capacity, separated by a space>
<residents in order of hospital1’s decreasing preference, separated by space>
...
---------------------------------------

*specific example*

---------------------------------------
hospital resident
5
5
abi
Harvard Stanford Berkeley USC UCLA
eve
Stanford UCLA USC Harvard Berkeley
hope
UCLA USC Harvard Berkeley Stanford
ray
Harvard UCLA Berkeley Stanford USC
dee
USC Harvard Stanford Berkeley UCLA
Harvard 1
eve hope abi ray dee
Stanford 2
hope dee eve ray abi
UCLA 1
dee ray eve abi hope
USC 2
ray dee eve abi hope
Berkeley 3
ray eve abi hope dee
---------------------------------------
stable marriage
<number of “guys”>
<number of “girls”>
<guy0_name>
<girls in order of guy0’s decreasing preference, separated by space>
<guy1_name>
<girls in order of guy1’s decreasing preference, separated by space>
...
---------------------------------------

*specific example*

---------------------------------------
stable marriage
5
5
ray
abi eve dee hope lia
bob
eve dee lia hope abi
kurt
dee hope abi lia eve
tim
hope abi lia dee eve
eli
abi dee eve hope lia
abi
eli ray bob kurt tim
dee
bob kurt tim eli ray
eve
kurt bob eli ray tim
hope
bob eli kurt tim ray
lia
bob ray time kurt eli
---------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Stable Roommates

in preferences.csv

---------------------------------------
stable roommates
<number of total people to be sorted (even #)>
<person0_name>
<other people in order of person0’s decreasing roommate preference, separated by space>
<person1_name>
<other people in order of person1’s decreasing roommate preference, separated by space>
...
---------------------------------------

*specific example*

---------------------------------------
stable roommates
10
abi
eve cath ivy jan dee fay bea hope ray
eve
cath ivy jan abi dee fay bea hope ray
ivy
abi eve cath bea hope ray jan dee fay 
bea
abi eve hope ray cath ivy jan dee fay
hope
abi eve cath ivy jan dee fay bea ray
cath
abi eve ivy jan dee fay bea hope ray
jan
abi eve cath ivy dee fay bea hope ray
dee
abi eve cath ivy jan fay bea hope ray
fay
abi eve cath ivy jan dee bea hope ray
ray
abi eve cath ivy jan dee fay bea hope
---------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Maximum Cardinality Bipartite Matching

in bipartitegraph.csv

---------------------------------------
maximum cardinality bipartite matching
<number of vertices>
<names of vertices, separated by space>
<vertex 1>
<names of vertices it connects to, separated by space>
<vertex 2>
<names of vertices it connects to, separated by space>
...
---------------------------------------
for vertices with no edges going out of them, the names of the vertices it connects to will just be itself

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Min Cost Max Flow

in graphs.csv

---------------------------------------
flow graph
<number of vertices>
<names of vertices, separated by space>
<vertex 1>
<names of vertices it connects to, separated by space>
<capacities for the corresponding edges, separated by space>
<costs for the corresponding edges, separated by space>
<vertex 2>
<names of vertices it connects to, separated by space>
<capacities for the corresponding edges, separated by space>
<costs for the corresponding edges, separated by space>
...
---------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Maximum Weight Perfect Matching

in matchingdata.csv

---------------------------------------
<number of vertices>
<name of vertex1>
<weights of edge to other vertices, separated by space>
<name of vertex2>
<weights of edge to other vertices, separated by space>
...
---------------------------------------

*specific example*

---------------------------------------
8
Arcanine
2 5 5 8 10 7 6 4 1 7
Bulbasaur
9 2 7 7 7 9 10 5 6 4
Charmander
7 3 6 7 8 2 6 9 10 3
Dragonite
8 5 10 6 9 8 6 7 1 4
Eevee
2 3 9 7 6 6 1 9 7 1
Flareon
8 10 10 3 4 8 8 6 5 1
Gengar
9 10 9 8 4 9 4 7 3 7
Haunter
8 8 3 3 9 1 7 8 1 3
---------------------------------------
set weight to very high integer if connection is unwanted

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Max Flow

in graph.csv

The same as for Min Cost Max Flow, but costs can be bogus values