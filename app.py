from flask import Flask,render_template,flash, request, redirect, url_for,session
from werkzeug.utils import secure_filename
app = Flask(__name__)
import networkx as nx
import os
import random
import math
import statistics
import json
ALLOWED_EXTENSIONS = ['json', 'gml', 'txt']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            if filename.rsplit('.', 1)[1].lower() == '.mtx':
                G = nx.read_adjlist(chosenFile, create_using=nx.DiGraph())
                nx.write_gml(G, 'graphFile.gml')  # THIS IS NOT THREAD SAFE. CAN IGNORE AS THEY WANT IT LOCALLY
                return redirect(url_for('uploaded'))
            if filename.rsplit('.', 1)[1].lower() == 'gml':
                G = nx.read_gml(file, label='id')
                nx.write_gml(G,'graphFile.gml') # THIS IS NOT THREAD SAFE. CAN IGNORE AS THEY WANT IT LOCALLY
                return redirect(url_for('uploaded'))
    return render_template('graphUpload.html', label='label')


@app.route('/uploaded')
def uploaded():
    g = nx.read_gml('graphFile.gml')
    print(g)
    nodes={}
    edges={}


    for x in g.node:
        nodes[x] = {'id':str(x)}
        if "label" in g.node[x]:
            print(f"label {g.node[x]['label']}")
            nodes[x]['label']=g.node[x]['label']
        else:
            nodes[x]['label'] = str(x)
    id=0
    for item in g.edges(data=True):
        edges[id]=item
        id+=1

    triads,sigStats, ratioStats = runTriads(g)
    # for triad in triads:
      #  print(triad)
    #print(stats)
    return render_template('graphDisplay.html', nodes=nodes, edges=edges, triads=str(triads),sigStats=sigStats, ratioStats=ratioStats)



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
def networkRandom(numNodes, Degree):
    numNodes = random.randint(1, 100)
    Degree = random.randint(1, numNodes)

    while ((numNodes * Degree) % 2 != 0):
        Degree = random.randint(1, numNodes)

    H = nx.random_regular_graph(Degree, numNodes, seed=None)
    G = H.to_directed()
    print(nx.info(G))


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
    jsonList = []

    if os.path.exists('randomTriads.json'):
        os.remove('randomTriads.json')

    for triangle in getting_Triangles(G):
        trianglesList.append(triangle)

    for triangle in trianglesList:
        triangle_code = TRICODE_TO_NAME[tricode(G, triangle[0], triangle[1], triangle[2])]
        jsonList.append({'x':int(triangle[0]), 'y':int(triangle[1]), 'z':int(triangle[2]), 'id':triangle_code,
         'connections': [int(triangle[0]), int(triangle[1]), int(triangle[2])]})


    with open('randomTriads.json', 'w') as json_file:
        json.dump(jsonList, json_file)

    return G
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

def runTriads(graph):
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


    G = nx.to_directed(graph)
    print(nx.info(G))
    zScores = []
    deltaValues = []
    triadList = []

    nodeCount= nx.number_of_nodes(G)
    edgeCount = nx.number_of_edges(G)
    triads = nx.triadic_census(G)
    print("Triad: Occurences")
    triadTotal = 0

    for i in triads:

        if (triads[i] != 0) and (i != '003') and (i != '012') and (i != '102'):
            print(i, " : ", triads[i])
            triadList.append(i)

        triadTotal += triads[i]

    rand_graph = networkRandom(nodeCount, edgeCount//nodeCount) # need to make this as a subgraph of all nodes of a specific triad
    rand_triads = nx.triadic_census(rand_graph)
    rand_total = 0
    subgraph_nodes = []
    newRandGraph = None
    trianglesList = []

    for i in rand_triads:
        rand_total += 1

    for triangle in getting_Triangles(G):
        trianglesList.append(triangle)

    for i in triads:

        if (triads[i] != 0) and (i != '003') and (i != '012') and (i != '102'):

            for j in rand_triads:

                if i == j:

                    for triangle in trianglesList:
                        triangleCode = TRICODE_TO_NAME[tricode(G, triangle[0], triangle[1], triangle[2])]

                        if triangleCode == i:
                            subgraph_nodes.append(int(triangle[0]))
                            subgraph_nodes.append(int(triangle[1]))
                            subgraph_nodes.append(int(triangle[2]))

                    subgraph_nodes = set(subgraph_nodes)
                    newRandGraph = rand_graph.subgraph(subgraph_nodes)
                    zScores.append(calculateStatSignificance(triads[i], rand_triads[j], newRandGraph, triadTotal, rand_total))
                    deltaValues.append(calculateDeltaValues(triads[i], rand_triads[j], triadTotal, rand_total))

                    subgraph_nodes = []

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



    sigList = []
    ratioList = []

    triadListIndex = 0
    for i in range(0, len(TRIAD_NAMES)):
        if(TRIAD_NAMES[i] in triadList):
            sigList.append([TRIAD_NAMES[i], sigProfile[triadListIndex]])
            ratioList.append([TRIAD_NAMES[i], subgraphRatio[triadListIndex]])
            triadListIndex += 1
        else:
            sigList.append([TRIAD_NAMES[i], 0]) 
            ratioList.append([TRIAD_NAMES[i], 0])
    #for i in range(0, len(triadList)):

        #ratioList.append(['Triad Type: ', triadList[i], 'Significance Profile: ', sigProfile[i], 'Subgraph Ratio Profile: ', subgraphRatio[i]])


    return jsonList, sigList, ratioList
#
# @app.route('/about/')
# def about():
#     return render_template('visPage.html')

if __name__ == "__main__":
    app.run(debug=True)
