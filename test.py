import node_preprocess
import networkx as nx
import csv
import matplotlib.pyplot as plt

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




G = nx.Graph()

preprocess = node_preprocess.node_preprocess('./grad_edges.txt', G)

preprocess.getGraph()

"""k_core, edge_core = preprocess.k_core(16)

result = {}

for node in G.__iter__():
    for i in k_core:
        for j in k_core[i]:
            result[j] = i
count = 0"""
result2 = getRightCore()
"""for i in result:
    if int(result[i]) != int(result2[i]):
        print (result[i], result2[i])
        count += 1
num = nx.number_of_nodes(G)
print ("Accurate rate: ", count/num)"""

k_core = preprocess.k_core2(16, G.copy())

result = {}

for i in k_core:
    for j in k_core[i]:
        result[j] = i
count = 0
for i in result:
    if int(result[i]) != int(result2[i]):
        print (result[i], result2[i])
        count += 1


num = nx.number_of_nodes(G)
print ("Accurate rate: ", 1 - count/num)

Gc = G.copy()
result2 = getRightPeak()
k_peak = preprocess.k_peak2()

result = {}
total = 0
for i in k_peak:
    for j in k_peak[i]:
        result[j] = i
        total+=1
count = 0

for i in result:
    if int(result[i]) != int(result2[i]):
        print ("node: ", i, result[i], result2[i])
        count += 1
num = nx.number_of_nodes(G)
print ("Accurate rate: ", 1 - count/num)
print ("Total nodes: ", total)

node = '5363'
G2 = nx.Graph()
edge_list = preprocess.getEdgeList(node)
edgeList = [(node, x) for x in edge_list]
G2.add_edges_from(edgeList)
pos = nx.spring_layout(G)
nx.draw(G2)
plt.show()




