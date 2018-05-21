import node_preprocess
import networkx as nx
import csv
import matplotlib.pyplot as plt
import random

def getRightCore():
    result = {}
    with open ("./CoreNumbers") as f:
        csv_file = csv.reader(f, delimiter=':')
        for row in csv_file:
            result[row[0]] = row[1]

    return result

def getRightPeak():
    result = {}
    with open ("./test") as f:
        csv_file = csv.reader(f, delimiter=':')
        for row in csv_file:
            result[row[0]] = row[1]

    return result
def randomRemoveByPercent(c, p, amount):
    nodes_list = list(c.keys())
    removed_num = int(len(c.keys()) * amount)
    removed = {}
    for i in range(removed_num):
        ran = random.randint(0, len(c.keys()) - 1)
        while (ran in removed.keys()):
            ran = random.randint(0, len(c.keys()) - 1)

        removed[ran] = nodes_list[ran]
    for i in removed:
        del c[removed[i]]
        del p[removed[i]]

def generateGraphReducedByEdges(percent, number):
    for i in range(number):
        plt.figure()
        G = nx.Graph()
        preprocess = node_preprocess.node_preprocess('./grad_edges.txt', G)
        preprocess.getGraph()
        #preprocess.reducedByPercent(0.1)
        preprocess.reduceEdgeByPercent(percent)
        G_temp = preprocess.G.copy()
        core = preprocess.getCodeNum(G_temp.copy())
        peak = preprocess.getPeakNum()

        mountainList = []
        for x in range (0, 16):
            #preprocess.coreRemoveK(x, peak)
            count = 16-x
            G_temp = preprocess.k_mountain_helper(count, peak, G_temp)
        mountainDict = preprocess.mountainDict
        for x in range (0,16):
            tempList = []
            tempList = [key for key, value in mountainDict.items() if value[0] == x and key in core.keys()]
            tempList = sorted(tempList, key=lambda x: int(core[x]), reverse=True)

            mountainList.append(tempList)
        mountainList = list(reversed(mountainList))
        offset = 0
        for j in range(0,16):
            if (mountainList[j] == []):
                continue
            nodeList = [item+offset for item in range(len(mountainList[j]))]
            y_core = [int(core[x]) for x in mountainList[j]]
            y_peak = [int(peak[x]) for x in mountainList[j]]
            plt.plot(nodeList, y_core, 'b-')
            plt.plot(nodeList, y_peak, 'ro', markersize=2)
            plt.fill_between(nodeList, 0, y_core, color='xkcd:sky blue')
            offset += len(mountainList[j])
        print (offset)
        print (mountainDict)
        name = str(i+1) + "_" + str(int(percent*100)) + "_edges"
        plt.savefig(name)
        #plt.show()

generateGraphReducedByEdges(0.1, 10)