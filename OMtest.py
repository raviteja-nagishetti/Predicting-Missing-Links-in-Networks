import networkx as nx
from sklearn.metrics import roc_curve, auc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

graph =pd.read_csv('powerdata.csv')
train,test = train_test_split(graph,test_size=0.2,random_state=None)

#removing header and saving
graph.to_csv('graph_edges.csv',header=False,index=False)
train.to_csv('train_edges.csv', header=False,index=False)
test.to_csv('test_edges.csv', header=False, index=False)

g = nx.read_edgelist('graph_edges.csv',delimiter=',',nodetype=int)
train_graph=nx.read_edgelist('train_edges.csv',delimiter=',',nodetype=int)
test_graph=nx.read_edgelist('test_edges.csv',delimiter=',',nodetype=int)
    
#path = dict(nx.all_pairs_shortest_path_length(train_graph))
#print(nx.info(g))
#print(nx.info(train_graph))
#print(nx.info(test_graph))
'''pos=nx.spring_layout(train_graph)
nx.draw(train_graph,pos,node_color='#A0CBE2',edge_color='#00bb5e',width=1,edge_cmap=plt.cm.Blues,with_labels=True)
plt.show()'''
#pos=nx.spring_layout(test_graph)
#nx.draw(test_graph,pos,node_color='#A0CBE2',edge_color='#00bb5e',width=1,edge_cmap=plt.cm.Blues,with_labels=True)
#plt.show()
            
def Distance(i,j):
    try:
        return nx.shortest_path_length(train_graph,source =i,target=j)
    
    except KeyError:
        return 0;

def CNe(a,b):
    try:
        return len(set(train_graph[a]).union(set(train_graph[b])))
    except:
        return 0
    
def CN(a,b):
    try:
        if len(set(train_graph[a])) == 0  | len(set(train_graph[b])) == 0:
            return 0
        return len(set(train_graph[a]).intersection(set(train_graph[b])))
    except:
        return 0
    
def Score(a,b):
    try:
        if CN(a,b) == 0:
            return (1/Distance(a,b))  
        else:
            return (CN(a,b)+Distance(a,b))/(Distance(a,b)+1)
    except:
        return 0
    
#generating Missing edges
edges_in_g = dict()
for i in g.edges:
    edges_in_g[(i[0],i[1])] = 1;

length = len(test_graph.edges)
missing_edges = set([])
while (len(missing_edges)<length):
    a=np.random.randint(min(g.nodes), max(g.nodes))
    b=np.random.randint(min(g.nodes), max(g.nodes))
    tmp = edges_in_g.get((a,b),-1)
    if tmp == -1 and a!=b:
        missing_edges.add((a,b))              
    else:
        continue
                   

def OurMethod():
    test_edge_list = list(test_graph.edges)
    missing_edge_list = list(missing_edges)
    scores = []
    n1 = 0
    n2 = 0
    n = length
    i = 0
    while (i < length):
        score1 = Score(test_edge_list[i][0],test_edge_list[i][1])
        score2 = Score(missing_edge_list[i][0],missing_edge_list[i][1])
        
        #if score1 == 0 or score2 == 0:
         #   n = n - 1
        if score1 > score2:
            n1 = n1 + 1
        elif score1 == score2:
            n2 = n2 + 1
        i = i + 1

    #calculating AUC
    print(n1," ",n2," ",n)
    auc = (n1 + 0.5*n2)/n
    print("AUC : ",auc)
    
    

OurMethod()
