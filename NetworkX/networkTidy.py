import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_gml('karate.gml', label='id')
H = nx.to_directed(G)

print(nx.number_of_nodes(G), " nodes")
triads = nx.triadic_census(H)
print("Triad: size")

for i in triads:
    if (triads[i] != 0) and (i != '003') and (i != '012') and (i != '102'):
        print(i, " : ", triads[i])

print("-----------")
# ---------------------------------------------------------------------- #

def get_triangles(G):
    nodes = G.nodes()
    for n1 in nodes:
        neighbors1 = set(G[n1])
        for n2 in filter(lambda x: x > n1, nodes):
            neighbors2 = set(G[n2])
            common = neighbors1 & neighbors2
            for n3 in filter(lambda x: x > n2, common):
                yield n1, n2, n3

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
# The problem it has its that it doesnt find every single triangle existing.
# Only 186 triangles with triad code code('201') instead of all 393

trianglesList = []
for triangle in get_triangles(G):
    trianglesList.append(triangle)

print(len(trianglesList))
counter = 0

for triangle in trianglesList:
    triangleCode = TRICODE_TO_NAME[tricode(G, triangle[0], triangle[1], triangle[2])]
    # print(triangleCode)
    if triangleCode == '201':
        counter = counter + 1

print(counter)

