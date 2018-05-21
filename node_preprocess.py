import networkx as nx
import csv
import random

class node_preprocess:
    def __init__(self, fp, G):
        self.fp = fp
        self.G = G

    def getGraph(self):
        fp = self.fp
        G = self.G
        with open(fp) as file:
            csv_file = csv.reader(file, delimiter=',')
            for row in csv_file:
                # print (row)
                G.add_edge(row[0], row[1])
        self.mountainDict = {node:(0,0) for node in self.G.nodes()}
        return G
    def reducedByPercent(self, percent):
        removed_num = int(nx.number_of_nodes(self.G) * percent)
        c = list(self.G.nodes.keys())
        removed = {}
        for i in range(removed_num):
            ran = random.randint(0, len(c) - 1)
            while (ran in removed.keys()):
                ran = random.randint(0, len(c) - 1)

            removed[ran] = c[ran]
        self.G.remove_nodes_from(list(removed.values()))

    def reduceEdgeByPercent(self, percent):
        removed_num = int(nx.number_of_edges(self.G) * percent)
        c = list(self.G.edges())
        removed = {}
        for i in range(removed_num):
            ran = random.randint(0, len(c) - 1)
            while (ran in removed.keys()):
                ran = random.randint(0, len(c) - 1)

            removed[ran] = c[ran]
        self.G.remove_edges_from(list(removed.values()))

    def k_core(self, limit):
        G = self.G
        k_core = {}
        edge_core = {}
        count = 0
        num = nx.number_of_nodes(G)
        core = 0
        while (core < limit):
            k_core[core] = []
            edge_core[core] = []
            for node in G.__iter__():
                degree = G.degree(node)
                neighbors = G.neighbors(node)
                length = len([x for x in neighbors if G.degree(x) < core])
                difference = degree - length
                if (difference >= core):
                    k_core[core].append(node)
                    count += 1
                for node2 in neighbors:
                    edge_core[core].append(node, node2)

            core += 1
        return k_core, edge_core

    def k_core2(self, limit, G):
        G_local = G.copy()
        k_core = {}
        edge_core = {}
        count = 0
        num = nx.number_of_nodes(G_local)
        core = 0
        while (core < limit):
            k_core[core] = []
            self.clean_up(G_local, core)
            k_core[core] += G_local.nodes()
            core += 1
        return k_core

    def clean_up(self, G, k):
        num = nx.number_of_nodes(G)
        Done = False
        removed = []
        for node in G.__iter__():
            degree = G.degree(node)
            if (degree < k):
                removed.append(node)
                Done = True
        G.remove_nodes_from(removed)
        num = nx.number_of_nodes(G)
        if (Done):
            self.clean_up(G, k)
    def k_peak(self, limit):
        G = self.G.copy()
        k_core = self.k_core2(16, G)
        peak = 0
        k_peak = {}
        while (peak < limit-1):
            k_peak[peak] = []
            for node in G.__iter__():
                if (node == '1637'):
                    count = 0
                    pass
                degree = G.degree(node)
                neighbors = G.neighbors(node)
                length = len([x for x in neighbors if G.degree(x) < peak or x in k_core[peak + 1]])
                difference = degree - length
                if (difference > peak):

                    k_peak[peak].append(node)


            peak += 1
        k_peak[15] = k_core[15]

        return k_peak
    def k_peak2(self):
        G = self.G.copy()
        k_peak = {}
        while (len(G.nodes()) > 0):
            k_core = self.k_core2(16, G.copy())
            keys = [x for x in sorted(k_core, reverse=True) if k_core[x] != []]
            if(not keys[0] in k_peak):
                k_peak[keys[0]] = []
            k_peak[keys[0]]+=k_core[keys[0]]
            G.remove_nodes_from(k_core[keys[0]])

        return k_peak

    def getEdgeList(self, node):
        edge_list = []
        neighbors = self.G.neighbors(node)
        neighborsList = [x for x in neighbors]
        return neighborsList

    def coreRemoveK(self, k, peak):
        G = self.G.copy()
        G2 = self.G.copy()
        removed = [x for x in peak.keys() if int(peak[x]) >= k]
        G.remove_nodes_from(removed)
        core = self.k_core2(16, G)
        coreList = {}
        for i in core:
            for j in core[i]:
                coreList[j] = i

        removed = [x for x in peak.keys() if int(peak[x]) >= k+1]
        G2.remove_nodes_from(removed)
        core2 = self.k_core2(16, G2)

        coreList2 = {}
        for i in core2:
            for j in core2[i]:
                coreList2[j] = i
        return_list = []

        for x in coreList:

            if (x in coreList.keys() and x not in coreList2.keys()):
                difference = coreList[x]
                if (difference > self.mountainDict.get(x)[1]):
                    self.mountainDict[x] = (k, difference)
                    return_list.append(x)

            if (x in coreList2.keys() and coreList[x] < coreList2[x] ):
                difference = coreList2[x] - coreList[x]
                if (difference > self.mountainDict.get(x)[1]):
                    self.mountainDict[x] = (k, difference)
                    return_list.append(x)
        """return_list = sorted(return_list, key=lambda x:coreList[x], reverse=True)"""
    def k_mountain_helper(self, k, peak, G):
        G1 = G.copy()
        G2 = G.copy()
        removed = [x for x in peak.keys() if int(peak[x]) >= k]
        G2.remove_nodes_from(removed)
        core = self.k_core2(16, G1)
        coreList = {}
        for i in core:
            for j in core[i]:
                coreList[j] = i
        core2 = self.k_core2(16, G2)

        coreList2 = {}
        for i in core2:
            for j in core2[i]:
                coreList2[j] = i
        for x in coreList:

            if (x in coreList.keys() and x not in coreList2.keys()):
                difference = coreList[x]
                if (difference > self.mountainDict.get(x)[1]):
                    self.mountainDict[x] = (k, difference)


            if (x in coreList2.keys() and coreList[x] > coreList2[x] ):
                difference = coreList[x] - coreList2[x]
                if (difference > self.mountainDict.get(x)[1]):
                    self.mountainDict[x] = (k, difference)
        return G2

    def getCodeNum(self, G):
        k_core = self.k_core2(16, G.copy())

        result = {}

        for i in k_core:
            for j in k_core[i]:
                result[j] = i
        return result

    def getPeakNum(self):
        k_peak = self.k_peak2()

        result = {}

        for i in k_peak:
            for j in k_peak[i]:
                result[j] = i
        return result

"""
G = nx.Graph()
Gc = G.copy()
pre = node_preprocess('./grad_edges.txt', Gc)
pre.getGraph()
k_peak = pre.k_peak2()
"""