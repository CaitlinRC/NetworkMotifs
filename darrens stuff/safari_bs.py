# By Darren O'Callaghan

import networkx as nx
import tradic
import matplotlib.pyplot as plt


# g = nx.DiGraph(nx.krackhardt_kite_graph())
g = nx.DiGraph(nx.dorogovtsev_goltsev_mendes_graph(2))
pos = nx.spring_layout(g)
census, node_census = tradic.triadic_census(g)
nxCensus = nx.triadic_census(g)
print(nxCensus)
# print(node_census)


def removingZeroTriads(node_census):
    better_node_census = {}
    for node in node_census:
        better_node_census[node] = {}
    for node in node_census:
        for triad in node_census[node]:
            if node_census[node][triad] != 0:
                better_node_census[node].update({triad: node_census[node][triad]})

    return better_node_census


node_census = removingZeroTriads(node_census)
print(node_census)


def buildTriadNodeList(triadType):
    triadNodeList = []
    nonTriadNodeList = []
    for node in node_census:
        if triadType in node_census[node]:
            triadNodeList.append(node)
        else:
            nonTriadNodeList.append(node)
    return triadNodeList, nonTriadNodeList


# for node in node_census:
    # print('102' in node_census[node])
nodeList201, nonNodeList201 = buildTriadNodeList("102")

print("y ", nodeList201)
print("n ", nonNodeList201)
# nx.draw(g, pos=None, arrows=True, with_labels=True)
nx.draw(g, pos, nodelist=nodeList201, node_color='b', with_labels=True)

nx.draw(g, pos, nodelist=nonNodeList201, node_color='r', with_labels=True)

plt.show()

""" This isn't perfect because the census doesn't present
    repeats, therefore, when it comes to them being some
    being the start of a triad, they arn't concidered
    connected to a triad, because it has already been counted :-( """
