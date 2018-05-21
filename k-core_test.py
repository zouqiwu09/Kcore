import networkx as nx
import csv
import matplotlib.pyplot as plt


G = nx.Graph()
G_peak = nx.Graph()

core0 = []
core1 = []
core2 = []
core3 = []
core4 = []
core5 = []
core6 = []
edge_list1 = []
edge_list2 = []
edge_list3 = []
edge_list4 = []
edge_list5 = []
edge_list6 = []
k_core = {0:core0, 10:core1, 20:core2, 30:core3, 40:core4, 50:core5, 60:core6}
edge_list = {10:edge_list1, 20:edge_list2, 30:edge_list3, 40:edge_list4, 50:edge_list5, 60:edge_list6 }
with open ("./0.edges") as file:
    csv_file = csv.reader(file, delimiter = ' ')
    for row in csv_file:
        #print (row)
        G.add_edge(row[0], row[1])
core = 0
while (core <= 60):
    for node in G.__iter__():
        degree = G.degree(node)
        neighbors = G.neighbors(node)
        length = len([x for x in neighbors if G.degree(x) < core])
        difference = degree - length
        if(difference >= core):
            k_core[core].append(node)
        for node2 in neighbors:
            edge_list[core].append(node, node2)

    core += 10

pos = nx.spring_layout(G)
print (pos)
for l in k_core:
    print (k_core[l])
#nx.draw_networkx(G = G, pos = pos, node_color= 'r', node_size = 100)
nx.draw_networkx_nodes(G = G, node_color= 'y', nodelist= core0, node_size = 10, pos = pos)
nx.draw_networkx_nodes(G = G, node_color= 'r', nodelist= core1, node_size = 10, pos = pos)
nx.draw_networkx_nodes(G = G, node_color= 'b', nodelist= core2, node_size = 10, pos = pos)
nx.draw_networkx_nodes(G = G, node_color= 'g', nodelist= core3, node_size = 10, pos = pos)
nx.draw_networkx_edges(G = G, edge_list = edge_list1, pos = pos)
nx.draw_networkx_edges(G = G, edge_list = edge_list2, pos = pos)
nx.draw_networkx_edges(G = G, edge_list = edge_list3, pos = pos)
#plt.show(block = False)
plt.savefig("k-core.png")
peak0 = []
peak1 = []
peak2 = []
peak3 = []
peak4 = []
peak5 = []
peak6 = []
k_peak = {0:peak0, 10:peak1, 20:peak2, 30:peak3, 40:peak4, 50:peak5, 60:peak6}

peak = 0
while (peak <= 50):
    for node in G.__iter__():
        degree = G.degree(node)
        neighbors = G.neighbors(node)
        length = len([x for x in neighbors if G.degree(x) < peak or x in k_core[peak+10]])
        difference = degree - length
        if(difference >= peak):
            k_peak[peak].append(node)
        for node2 in neighbors:
            edge_list[peak].append(node, node2)

    peak += 10

for l in k_core:
    print (k_peak[l])
nx.draw_networkx_nodes(G = G, node_color= 'y', nodelist= peak0, node_size = 10, pos = pos)
nx.draw_networkx_nodes(G = G, node_color= 'r', nodelist= peak1, node_size = 10, pos = pos)
nx.draw_networkx_nodes(G = G, node_color= 'b', nodelist= peak2, node_size = 10, pos = pos)
nx.draw_networkx_nodes(G = G, node_color= 'g', nodelist= peak3, node_size = 10, pos = pos)
nx.draw_networkx_edges(G = G, edge_list = edge_list1, pos = pos)
nx.draw_networkx_edges(G = G, edge_list = edge_list2, pos = pos)
nx.draw_networkx_edges(G = G, edge_list = edge_list3, pos = pos)
#plt.show(block = False)
plt.savefig("k-peak.png")