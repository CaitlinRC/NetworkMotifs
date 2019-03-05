import networkx as nx
import matplotlib.pyplot as plt

def findTriad(currentGraph, triad, occurences):

    if (triad == '111D'):
        triad111D(currentGraph, occurences)

    elif (triad == "201"):
        triad201(currentGraph, occurences)

    elif (triad == "210"):
        triad210(currentGraph, occurences)

    elif (triad == "300"):
        triad300(currentGraph, occurences)

    elif (triad == "021D"):
        triad021D(currentGraph, occurences)

    elif (triad == "111U"):
        triad111U(currentGraph, occurences)

    elif (triad == "120D"):
        triad120D(currentGraph, occurences)

    elif (triad == "021U"):
        triad021U(currentGraph, occurences)

    elif (triad == "030T"):
        triad030T(currentGraph, occurences)

    elif (triad == "120U"):
        triad120U(currentGraph, occurences)

    elif (triad == "021C"):
        triad021C(currentGraph, occurences)

    elif (triad == "030C"):
        triad030C(currentGraph, occurences)

    else:
        triad120C(currentGraph, occurences)


def triad111D(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad201(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad210(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad300(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad021D(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad111U(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad120D(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad021U(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad030T(currentGraph, numberOfOccurences):

    # 1 to 2, 1 to 3, 3 to 2
    # Finds this type, number of occurences to reduce search time

    triadOptions = {}
    items = []

    for i in currentGraph.nodes():
        items = []
        counter = 0
        val = currentGraph.neighbors(i)

        for option in val:
            items.append(int(option))
            counter += 1


        if counter >= 2:

            triadOptions[int(i)] = items


    # Needs to go through list of nodes and neighbors, find those that are
    # Find those that go from 1 to 2, 1 to 3, 3 to 2
    # For each node in triadOptions
    # Assign one as value a, its connections as b and c. If b and c also connect



    triadFound = False
    print(triadOptions)
    aValue = None
    bValue = None
    cValue = None

    # avalue is value that goes to bvalue and cvalue
    # cvalue goes to bvalue

    # Currently not working ? Selecting wrong values
    # Need to make this work grr

    while triadFound == False:

        triadList = []

        for option in triadOptions: # Looking through each value (potentially A)

            for item in triadOptions[option]:

                triadList.append(item)

            for choice in triadList:

                if (choice in triadOptions and option in triadOptions[choice]):

                    aValue = option

                    cValue = choice

                for myChoice in triadList:

                    if (aValue != None) and (cValue != None) and (myChoice in triadOptions[aValue] and myChoice in triadOptions[cValue]):
                        bValue = myChoice


        if (aValue != None and bValue != None and cValue != None):
            triadFound = True

    print(aValue, bValue, cValue)
    new = nx.DiGraph()

    new.add_node(aValue)
    new.add_node(bValue)
    new.add_node(cValue)
    new.add_edge(aValue, bValue)
    new.add_edge(cValue, aValue)
    new.add_edge(cValue, bValue)

    plt.cla()
    nx.draw(new, pos = None, arrows=True, with_labels=True)
    plt.savefig('Triad Found')






def triad120U(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad021C(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad030C(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad120C(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time


g = nx.DiGraph()
gml = nx.read_gml('internet_routers-22july06.gml')

nx.draw(gml)


plt.savefig('example')
plt.cla()
currentGraph = nx.read_adjlist('ca-sandi_auths.mtx', create_using = nx.DiGraph())
nx.draw(currentGraph, pos = None, arrows=True, with_labels=True)
plt.savefig('mtxExample')

e = nx.triadic_census(currentGraph)
print(e)
plt.cla()
H = currentGraph.subgraph(['1', '58', '45'])
nx.draw(H, pos = None, arrows=True, with_labels=True)
plt.savefig('compare')

# Null triad = Type 003
# Dyadic Traids = Type 012 and 102
# Connected Triads = 111D, 201, 210, 300, 021D, 111U, 120D, 021U, 030T, 120U, 021C, 030C, 120C
triadsToFind = ['111D', '201', '210', '300', '021D', '111U', '120D', '021U', '030T', '120U', '021C', '030C', '120C']

for triad in e:

    print('\nTriad Type:', triad, 'Number Of Occurences:', e.get(triad))

    if (triad in triadsToFind) and (e.get(triad) != 0):
        findTriad(currentGraph, triad, e.get(triad))
