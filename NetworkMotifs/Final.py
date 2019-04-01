import networkx as nx
import matplotlib.pyplot as plt
import json
import os

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

G = nx.read_adjlist('Datasets/ca-sandi_auths.mtx', create_using=nx.DiGraph())    #Reading mtx
# G = nx.read_gml("football.gml",label='id')                            #Reading gml
G = nx.to_directed(G)

print("Is directed: ", nx.is_directed(G))
print(nx.number_of_nodes(G), " nodes")
triads = nx.triadic_census(G)
print("Triad: Occurences")

for i in triads:
    if (triads[i] != 0) and (i != '003') and (i != '012') and (i != '102'):
        print(i, " : ", triads[i])

print("-------------")

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


        # json.dump((triangle[0], triangle[1], triangle[2], triangleCode), json_file)
with open('triads.json', 'a') as json_file:
    json.dump(jsonList, json_file)
