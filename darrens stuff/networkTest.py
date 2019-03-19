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
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad120U(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad021C(currentGraph, numberOfOccurences):
    print("running")
    # Finds this type, number of occurences to reduce search time

def triad030C(currentGraph, numberOfOccurences):
    print("This triad: A -> B, B -> C, C -> A")

    # Finds this type, number of occurences to reduce search time

    """ Notes on this algorithm:
    1): Remove from concideration any node that doesnt have an outward edge (pointing away)
    2): 
	"""
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


# Null triad = Type 003
# Dyadic Traids = Type 012 and 102
# Connected Triads = 111D, 201, 210, 300, 021D, 111U, 120D, 021U, 030T, 120U, 021C, 030C, 120C
triadsToFind = ['111D', '201', '210', '300', '021D', '111U', '120D', '021U', '030T', '120U', '021C', '030C', '120C']

for triad in e:

    print('\nTriad Type:', triad, 'Number Of Occurences:', e.get(triad))

    if (triad in triadsToFind) and (e.get(triad) != 0):
        findTriad(currentGraph, triad, e.get(triad))
