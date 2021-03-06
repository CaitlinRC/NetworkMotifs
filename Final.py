import networkx as nx
import matplotlib.pyplot as plt
import json
import statistics
import os
import math
from pathlib import Path
import networkRandom

def calculateStatSignificance(countOfNormal, countOfRandom, randomSubset, normalTotal, randomTotal):
    # NEEDS TO RETURN Z SCORE

    stDev = statistics.stdev(randomSubset)
    meanRandom = countOfRandom / randomTotal


    return ((countOfNormal - meanRandom) / stDev)

def calculateSignificanceProfile(zScores): # write to json file

    normalisedZ = [float(i)/sum(zScores) for i in zScores]

    sumOfZ = sum(normalisedZ)

    divisor = sumOfZ ** 2

    final = math.sqrt(divisor)

    values = [x / final for x in normalisedZ]

    return values

def calculateDeltaValues(countOfNormal, countOfRandom, normalTotal, randomTotal):

    meanRandom = countOfRandom / randomTotal

    return ((countOfNormal - meanRandom) / (countOfNormal + meanRandom))


def subgraphRatioProfile(deltaValues): # write answers out into json file

    normalisedDelta = [float(i)/sum(deltaValues) for i in deltaValues]
    sumOfDelta = sum(deltaValues)
    divisor = sumOfDelta ** 2
    final = math.sqrt(divisor)

    values = [x / final for x in normalisedDelta]
    return values

def getting_Triangles(G):

    m = {v: i for i, v in enumerate(G)}
    for v in G:
        vnbrs = set(G.pred[v]) | set(G.succ[v])
        for u in vnbrs:
            if m[u] <= m[v]:
                continue
            neighbors = (vnbrs | set(G.succ[u]) | set(G.pred[u])) - {u, v}

            # Count connected triads.
            for w in neighbors:
                if m[u] < m[w] or (m[v] < m[w] < m[u] and
                                   v not in G.pred[w] and
                                   v not in G.succ[w]):
                    yield v, u, w


def tricode(G, v, u, w):

    combos = ((v, u, 1), (u, v, 2), (v, w, 4), (w, v, 8), (u, w, 16),
              (w, u, 32))
    return sum(x for u, v, x in combos if v in G[u])

TRICODES = (1, 2, 2, 3, 2, 4, 6, 8, 2, 6, 5, 7, 3, 8, 7, 11, 2, 6, 4, 8, 5, 9,
            9, 13, 6, 10, 9, 14, 7, 14, 12, 15, 2, 5, 6, 7, 6, 9, 10, 14, 4, 9,
            9, 12, 8, 13, 14, 15, 3, 7, 8, 11, 7, 12, 14, 15, 8, 14, 13, 15,
            11, 15, 15, 16)

#: important: it corresponds to the tricodes given in :data:`TRICODES`.
TRIAD_NAMES = ('003', '012', '102', '021D', '021U', '021C', '111D', '111U',
               '030T', '030C', '201', '120D', '120U', '120C', '210', '300')


#: A dictionary mapping triad code to triad name.
TRICODE_TO_NAME = {i: TRIAD_NAMES[code - 1] for i, code in enumerate(TRICODES)}

# ---------------------------------------------------------------------- #

# building menu system:
# Needs to be able to read in file name and choose appropriate networkx strategy
#FRONT END PLEASE HAND IN FILE NAME IN STRING FORMAT?

chosenFile = "Datasets/ca-sandi_auths.mtx" # this would be the filename handed in
#chosenFile = "Datasets/football.gml"
#chosenFile = "potato"

if Path(chosenFile).suffix == ".mtx":
    G = nx.read_adjlist(chosenFile, create_using=nx.DiGraph())    #Reading mtx

elif Path(chosenFile).suffix == ".gml": # reading gml
    G = nx.read_gml(chosenFile, label = "id")

else:
    print('Invalid File Type')
    exit()

G = nx.to_directed(G)
print(nx.info(G))
zScores = []
deltaValues = []
triadList = []


triads = nx.triadic_census(G)
print("Triad: Occurences")
triadTotal = 0

for i in triads:

    if (triads[i] != 0) and (i != '003') and (i != '012') and (i != '102'):
        print(i, " : ", triads[i])
        triadList.append(i)

    triadTotal += triads[i]


randGraph = networkRandom.runCode() # need to make this as a subgraph of all nodes of a specific triad
randTriads = nx.triadic_census(randGraph)
randTotal = 0
subgraphNodes = []
newRandGraph = None
trianglesList = []

for i in randTriads:
    randTotal += 1

for triangle in getting_Triangles(G):
    trianglesList.append(triangle)

for i in triads:

    if (triads[i] != 0) and (i != '003') and (i != '012') and (i != '102'):

        for j in randTriads:

            if i == j:

                for triangle in trianglesList:
                    triangleCode = TRICODE_TO_NAME[tricode(G, triangle[0], triangle[1], triangle[2])]

                    if triangleCode == i:
                        subgraphNodes.append(int(triangle[0]))
                        subgraphNodes.append(int(triangle[1]))
                        subgraphNodes.append(int(triangle[2]))



                subgraphNodes = set(subgraphNodes)
                newRandGraph = randGraph.subgraph(subgraphNodes)
                zScores.append(calculateStatSignificance(triads[i], randTriads[j], newRandGraph, triadTotal, randTotal))
                deltaValues.append(calculateDeltaValues(triads[i], randTriads[j], triadTotal, randTotal))

                subgraphNodes = []

sigProfile = calculateSignificanceProfile(zScores)
subgraphRatio = subgraphRatioProfile(deltaValues)

print(sigProfile)
print(subgraphRatio)
print("-------------")
print(triadList)



trianglesList = []
jsonList=[]

if os.path.exists('triads.json'):
    os.remove('triads.json')


for triangle in getting_Triangles(G):
    trianglesList.append(triangle)


for triangle in trianglesList:
    triangleCode = TRICODE_TO_NAME[tricode(G, triangle[0], triangle[1], triangle[2])]
    jsonList.append({'x':int(triangle[0]), 'y':int(triangle[1]), 'z':int(triangle[2]), 'id':triangleCode,
     'connections': [int(triangle[0]), int(triangle[1]), int(triangle[2])]})

with open('triads.json', 'w') as json_file:
    json.dump(jsonList, json_file)

if os.path.exists('stats.json'):
    os.remove('stats.json')

statList = []

for i in range(0, len(triadList)):

    statList.append(['Triad Type: ', triadList[i], 'Significance Profile: ', sigProfile[i], 'Subgraph Ratio Profile: ', subgraphRatio[i]])

with open('stats.json', 'w') as json_file:
    json.dump(statList, json_file)
